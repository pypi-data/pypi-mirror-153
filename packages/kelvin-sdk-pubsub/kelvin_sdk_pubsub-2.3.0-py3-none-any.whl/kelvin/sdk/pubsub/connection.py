"""Connections."""

from __future__ import annotations

import asyncio
import sys
from asyncio import Future, Lock
from asyncio import Queue as AsyncQueue
from asyncio import QueueEmpty, QueueFull, Task
from queue import Empty, Full, Queue
from random import random
from time import time
from types import TracebackType
from typing import Any, AsyncIterator, Dict, List, Optional, Sequence, Tuple, Type, TypeVar, Union
from uuid import uuid4

import orjson
import structlog
from asyncio_mqtt import Client as AsyncClient
from asyncio_mqtt import MqttError
from orjson import OPT_SORT_KEYS
from paho.mqtt.client import Client, MQTTMessage

from kelvin.sdk.datatype import Message
from kelvin.sdk.datatype.message import Endpoint

from .config import PubSubClientConfig, Selector
from .error import ConnectionError
from .utils import coalesce

if sys.version_info >= (3, 8):
    from functools import cached_property
else:  # pragma: no cover
    from cached_property import cached_property  # type: ignore

logger = structlog.get_logger(__name__)

E = TypeVar("E", bound=Exception)


class Connection:
    """Pub-Sub Connection."""

    _input_count: int = 0
    _output_count: int = 0
    _connect_count: int = 0

    config: PubSubClientConfig

    def __init__(self, config: PubSubClientConfig) -> None:
        """Initialise the connection."""

        self.config = config

    @property
    def stats(self) -> Dict[str, Any]:
        """Provide connection statistics."""

        return {
            "input_count": self._input_count,
            "output_count": self._output_count,
        }

    @cached_property
    def _storage_config(self) -> Tuple[str, bytes]:
        """Storage config."""

        config = self.config
        node_name, workload_name = config.node_name, config.workload_name
        storage_config = config.storage_config
        topic = f"config/{node_name}/edge-sync/storage/{workload_name}"

        if not storage_config:
            return topic, b""

        payload = {
            "node_name": node_name,
            "workload_name": workload_name,
            "timestamp": time(),
            "metrics": [
                {
                    "node_name": selector.node_name,
                    "workload_name": selector.workload_name,
                    "asset_name": selector.asset_name,
                    "metric_name": selector.name,
                    "data_type": data_type,
                    "access": access,
                    "storage": storage,
                }
                for selector, (access, storage, data_type) in sorted(storage_config.items())
            ],
        }

        return topic, orjson.dumps(payload, option=OPT_SORT_KEYS)

    def _make_messages(self, topic: str, payload: bytes) -> List[Message]:
        """Make messages."""

        logger.debug("Topic received", topic=topic)

        config = self.config

        message = Message.decode(payload)

        header = message._
        target = header.target

        node_name = (target.node_name if target else None) or ""
        workload_name = (target.workload_name if target else None) or ""
        asset_name = header.asset_name or ""
        name, data_type = header.name, header.type

        key = Selector(node_name, workload_name, asset_name, name)
        items = config.input_map.get(key)
        if items is None:
            logger.error("Unknown input", topic=topic, key=key)
            return []

        messages: List[Message] = []

        for item in items:
            _, input_name, input_data_type = item
            if input_data_type != data_type:
                logger.error(
                    f"Skipping data with unexpected data-type {data_type!r} (expected {input_data_type!r})",
                    topic=topic,
                )
                continue

            if input_name != name:
                message_ = message.copy()
                message_._.name = input_name
                messages += [message_]
            else:
                messages += [message]

            logger.debug("Input message", topic=topic, key=key, name=input_name)

        return messages

    def _make_payloads(self, message: Message) -> List[Tuple[str, bytes, bool]]:
        """Publish message."""

        config = self.config

        header = message._
        asset_name = coalesce(header.asset_name, "")
        name, data_type = header.name, header.type

        source, target = header.source, header.target

        if not (source and target and asset_name):
            # fill missing information in header
            message = message.copy()
            header = message._
            if not asset_name:
                asset_name = header.asset_name = coalesce(config.asset_name, "")
            if not source:
                source = header.source = Endpoint(
                    node_name=config.node_name,
                    workload_name=config.workload_name,
                )
            if not target:
                target = header.target = source.copy()

        node_name = coalesce(target.node_name, "")
        workload_name = coalesce(target.workload_name, "")

        key = Selector(node_name, workload_name, asset_name, name)
        logger.debug("Output message", key=key)

        items = config.output_map.get(key)
        if items is None:
            raise ValueError(f"Unknown output {key!r}") from None

        payloads: List[Tuple[str, bytes, bool]] = []

        for item in items:
            output_topic, output_name, output_data_type, retain, control_change = item
            if not control_change and output_data_type != data_type:
                raise ValueError(
                    f"Unexpected data-type {data_type!r} (expected {output_data_type})"
                ) from None

            if output_name != name:
                message_ = message.copy()
                message_._.name = output_name
                payload = message_.encode(False)
            else:
                payload = message.encode(False)

            logger.debug("Topic produced", key=key, topic=output_topic)
            payloads += [(output_topic, payload, retain)]

        return payloads


S = TypeVar("S", bound="SyncConnection", covariant=True)


class SyncConnection(Connection):
    """Synchronous Pub-Sub Connection."""

    _client: Optional[Client] = None
    _queue: Queue[Message]

    def __init__(self, config: PubSubClientConfig) -> None:
        """Initialise the connection."""

        super().__init__(config)

        self._queue = Queue(maxsize=self.config.max_items)

    def connect(self) -> None:
        """Open connection."""

        self._input_count = self._output_count = 0

        client = self._client
        if client is not None:
            try:
                client.disconnect()
            except Exception:
                pass

        config = self.config
        client = self._client = config.broker_url.get_sync_client(
            config.client_id or f"pubsub-{uuid4()}",
            config.username,
            config.password,
        )
        client.on_message = self._on_message

        topics = config.input_topics
        if topics:
            client.subscribe([(topic, config.qos) for topic in topics])

        if topics:
            topic_summary = "\n".join(f"  - {topic}" for topic in topics)
            logger.info(f"Subscribed to topics:\n{topic_summary}")

        client.loop_start()
        if not self._connect_count:
            self._send_storage_config()
        self._connect_count += 1

    def _send_storage_config(self) -> None:
        """Send storage configuration."""

        client = self._client
        if client is None:
            return

        topic, payload = self._storage_config
        if not payload:
            return

        client.publish(topic, payload, retain=True)

    def disconnect(self) -> None:
        """Close connection."""

        client = self._client
        if client is None:
            return

        self._client = None
        self._connect_count = 0

        try:
            client.disconnect()
        except Exception:
            pass
        client.on_message = None

        # drain queue
        queue = self._queue
        while True:
            try:
                queue.get_nowait()
                queue.task_done()
            except Empty:
                break

    def __enter__(self: S) -> S:
        """Enter the connection."""

        self.connect()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[E]],
        exc_value: Optional[E],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the connection."""

        self.disconnect()

    def _on_message(self, client: Client, userdata: Any, message: MQTTMessage) -> None:
        """Message handler."""

        topic, payload = message.topic, message.payload

        try:
            results = self._make_messages(topic, payload)
        except Exception:
            logger.exception("Unable to decode message", topic=topic)
            return

        queue = self._queue
        for result in results:
            try:
                queue.put_nowait(result)
                self._input_count += 1
            except Full:
                with queue.mutex:
                    if queue.full():
                        logger.warning("Queue full. Discarding oldest message", topic=topic)
                        queue.get_nowait()
                        queue.task_done()
                    queue.put_nowait(result)

    def send(self, message: Union[Message, Sequence[Message]]) -> None:
        """Send message."""

        client = self._client
        if client is None:
            return

        qos = self.config.qos

        messages = message if isinstance(message, Sequence) else [message]

        for message in messages:
            for topic, payload, retain in self._make_payloads(message):
                client.publish(topic, payload, qos=qos, retain=retain)
                self._output_count += 1

    def receive(self, timeout: Optional[float] = None) -> Optional[Message]:
        """Receive message."""

        if self._client is None:
            return None

        try:
            message = self._queue.get(timeout=timeout)
        except Empty:
            return None
        else:
            self._queue.task_done()
            return message


A = TypeVar("A", bound="AsyncConnection", covariant=True)


class AsyncConnection(Connection):
    """Asynchronous Pub-Sub Connection."""

    _client: AsyncClient
    _connecting: Lock
    _queue: AsyncQueue[Tuple[str, bytes, bool]]
    _send_task: Optional[Task] = None

    min_interval: float = 1.0
    max_interval: float = 32.0

    def __init__(self, config: PubSubClientConfig) -> None:
        """Initialise async connection."""

        super().__init__(config)

        config = self.config

        self._client = config.broker_url.get_async_client(
            config.client_id or f"pubsub-{uuid4()}",
            config.username,
            config.password,
        )

        self._connecting = Lock()
        self._queue = AsyncQueue(maxsize=self.config.max_items)

    async def connect(self, max_attempts: Optional[int] = None) -> None:
        """Connect."""

        client, config = self._client, self.config
        topics = config.input_topics

        connecting = self._connecting

        if connecting.locked():
            async with connecting:
                return

        async with connecting:
            interval, i = 0.0, 0
            while True:
                i += 1
                try:
                    await client.disconnect(timeout=0)
                except Exception:
                    pass

                # hack to allow reconnecting client later
                try:
                    connected, disconnected = client._connected, client._disconnected
                    client._connected, client._disconnected = Future(), Future()
                    tasks = asyncio.gather(connected, disconnected)
                    tasks.cancel()
                    await tasks
                except KeyboardInterrupt:
                    raise
                except BaseException:
                    pass

                try:
                    await client.connect()
                    if topics:
                        await client.subscribe([(topic, config.qos) for topic in topics])
                    if not self._connect_count:
                        await self._send_storage_config()
                except MqttError as e:
                    if max_attempts is not None and i >= max_attempts:
                        raise ConnectionError(f"Unable to connect to broker: {e}")
                    logger.info(f"Retrying connection in {interval} seconds (attempt {i})")
                    await asyncio.sleep(interval + random())  # nosec
                    interval = min(max(2.0 * interval, self.min_interval), self.max_interval)
                    continue
                else:
                    break

            if not self._connect_count:
                self._send_task = asyncio.create_task(self._send())
            self._connect_count += 1

        if topics:
            topic_summary = "\n".join(f"  - {topic}" for topic in topics)
            logger.info(f"Subscribed to topics:\n{topic_summary}")

    async def _send_storage_config(self) -> None:
        """Send storage configuration."""

        client = self._client

        topic, payload = self._storage_config
        if not payload:
            return

        await client.publish(topic, payload, retain=True)

    async def disconnect(self) -> None:
        """Close connection."""

        await asyncio.sleep(0.0)

        client = self._client

        connecting = self._connecting

        async with connecting:
            send_task, self._send_task = self._send_task, None

            if send_task is not None:
                send_task.cancel()
                try:
                    await send_task
                except KeyboardInterrupt:
                    raise
                except BaseException:
                    pass

            try:
                await client.disconnect()
            except Exception:
                pass

            self._connect_count = 0

        # drain queue
        queue = self._queue
        while True:
            try:
                queue.get_nowait()
                queue.task_done()
            except QueueEmpty:
                break

    async def __aenter__(self: A) -> A:
        """Enter the connection."""

        await self.connect()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[E]],
        exc_value: Optional[E],
        tb: Optional[TracebackType],
    ) -> None:
        """Exit the connection."""

        await self.disconnect()

    def send(self, message: Message) -> None:
        """Send message."""

        payloads = self._make_payloads(message)
        queue = self._queue

        for topic, payload, retain in payloads:
            try:
                queue.put_nowait((topic, payload, retain))
            except QueueFull:
                logger.warning("Queue full. Discarding oldest message", topic=topic)
                queue.get_nowait()
                queue.task_done()
                queue.put_nowait((topic, payload, retain))

    async def _send(self) -> None:
        """Send task."""

        client = self._client
        queue = self._queue
        qos = self.config.qos

        while True:
            topic, payload, retain = await queue.get()
            while True:
                try:
                    await client.publish(topic, payload, qos=qos, retain=retain)
                except Exception as e:
                    logger.error(f"Unable to send message: {e}")
                    await self.connect()
                else:
                    self._output_count += 1
                    break

    async def stream(self) -> AsyncIterator[Message]:
        """Receive message."""

        client = self._client

        while True:
            try:
                async with client.unfiltered_messages() as messages:
                    async for message in messages:  # pragma: no branch
                        topic, payload = message.topic, message.payload
                        try:
                            results = self._make_messages(topic, payload)
                            for result in results:
                                self._input_count += 1
                                yield result
                        except Exception:
                            logger.exception("Unable to decode message", topic=topic)
            except MqttError as e:
                logger.error(f"Unable to receive messages: {e}")
                await self.connect()
