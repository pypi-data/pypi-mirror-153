"""Kelvin Pub-Sub Client."""

from __future__ import annotations

import sys
from typing import Any, Mapping, Optional, Union, cast, overload

from .config import PubSubClientConfig
from .connection import AsyncConnection, Connection, SyncConnection

if sys.version_info >= (3, 8):
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore


class PubSubClient:
    """Kelvin Pub-Sub Client."""

    def __init__(
        self, config: Union[Optional[PubSubClientConfig], Mapping[str, Any]] = None, **kwargs: Any
    ) -> None:
        """Initialise Kelvin Pub-Sub Client."""

        if config is None:
            config = PubSubClientConfig(**kwargs)
        elif isinstance(config, PubSubClientConfig):
            config = config.copy(deep=True)
            for name, value in kwargs.items():
                setattr(config, name, value)
        elif isinstance(config, Mapping):
            config = PubSubClientConfig.parse_obj({**config, **kwargs})
        else:
            raise TypeError(f"Invalid config type {type(config).__name__!r}")

        self._config = cast(PubSubClientConfig, config)

    @property
    def config(self) -> PubSubClientConfig:
        """Pub-Sub client configuration."""

        return self._config

    @overload
    def connection(self, sync: Literal[True], **kwargs: Any) -> SyncConnection:
        ...

    @overload
    def connection(self, sync: Literal[False], **kwargs: Any) -> AsyncConnection:
        ...

    @overload
    def connection(self, sync: Literal[None] = None, **kwargs: Any) -> Connection:
        ...

    def connection(self, sync: Optional[bool] = None, **kwargs: Any) -> Connection:
        """Connect client to server."""

        config = self.config

        if sync is None:
            sync = config.sync

        cls = SyncConnection if sync else AsyncConnection

        return cls(config, **kwargs)  # type: ignore
