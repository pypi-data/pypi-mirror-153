"""Kelvin Pub-Sub Client Configuration."""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from itertools import groupby, product
from pathlib import Path
from typing import (
    Any,
    Collection,
    DefaultDict,
    Dict,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    cast,
)

import yaml
from pydantic import BaseSettings, Field, ValidationError, root_validator, validator
from pydantic.main import ErrorWrapper, ModelField

from kelvin.sdk.datatype import Model

from .types import QOS, Access, DNSName, DottedName, MQTTUrl, Storage
from .utils import deep_get

if sys.version_info >= (3, 8):
    from functools import cached_property
else:  # pragma: no cover
    from cached_property import cached_property  # type: ignore

DEFAULT_MQTT_HOST = "kelvin-mqtt-broker.app"
WILDCARD = "+"
SELECTORS = [
    "node_names",
    "workload_names",
    "asset_names",
    "names",
]
IO_FIELDS = {
    "inputs": "sources",
    "outputs": "targets",
}
ENV_FIELDS = {
    "node_name": ["KELVIN_NODE_NAME", "KELVIN_ACP_NAME"],
    "workload_name": ["KELVIN_WORKLOAD_NAME"],
}


class Selector(NamedTuple):
    """Selector."""

    node_name: str
    workload_name: str
    asset_name: str
    name: str

    def __repr__(self) -> str:
        """Return repr(str)."""

        return f"({', '.join(f'{k}={v!r}' for k, v in zip(self._fields, self))})"

    def __hash__(self) -> int:
        """Overriding __hash__ to only include asset and name, this way we can get custom dict key comparison"""

        return hash((self.asset_name, self.name))

    def __eq__(self, other: Any) -> bool:
        """Overriding __eq__ to always match empty nodes and empty workloads"""

        if not isinstance(other, Selector):
            return False
        node_equal = self.node_name == "" or self.node_name == other.node_name
        workload_equal = self.workload_name == "" or self.workload_name == other.workload_name
        asset_equal = self.asset_name == other.asset_name
        name_equal = self.name == other.name
        return node_equal and workload_equal and asset_equal and name_equal


class Metric(Model):
    """Metric info."""

    class Config(Model.Config):
        """Pydantic config."""

        keep_untouched = (cached_property,)

    @validator(*SELECTORS, pre=True, always=True)
    def validate_selectors(cls, value: Any) -> Any:
        """Validate selectors."""

        if isinstance(value, (str, bytes)):
            return value

        if not isinstance(value, Collection) or isinstance(value, Mapping):
            return value

        if not all(isinstance(x, str) for x in value):
            return value

        # wildcard
        if "" in value:
            return []

        return sorted(value)

    node_names: Set[DNSName] = Field(
        {*[]},
        title="Node Names",
        description="Node names.",
    )
    workload_names: Set[DNSName] = Field(
        {*[]},
        title="Workload Names",
        description="Workload names.",
    )
    asset_names: Set[DottedName] = Field(
        {*[]},
        title="Asset Names",
        description="Asset names.",
    )
    names: Set[DottedName] = Field(
        {*[]},
        title="Names",
        description="Names.",
    )

    def match(self, x: Mapping[str, str]) -> bool:
        """Check if mapping matches metric info."""

        return all(x.get(k) in v for k, v in self.__dict__.items() if k in SELECTORS)

    @cached_property
    def combinations(self) -> Set[Selector]:
        """Field combinations."""

        return {*product(*(sorted(getattr(self, field)) or [""] for field in SELECTORS))}


class IO(Model):
    """IO."""

    class Config(Model.Config):
        """Pydantic config."""

        keep_untouched = (cached_property,)

    name: DottedName = Field(
        ...,
        title="Name",
        description="Name.",
    )
    data_type: DottedName = Field(
        ...,
        title="Data Type",
        description="Data type.",
    )
    control_change: bool = Field(
        False, title="Control Change", description="Specifies if the output is a control change"
    )
    metrics: List[Metric] = Field(
        [{}],
        title="Metrics",
        description="Metrics.",
    )

    @cached_property
    def combinations(self) -> Set[Selector]:
        """Field combinations."""

        return {x for metric in self.metrics for x in metric.combinations}


class Input(IO):
    """Input."""


class Output(IO):
    """Output."""

    storage: Storage = Field(
        Storage.NODE_CLOUD,
        title="Storage",
        description="Storage type.",
    )
    retain: bool = Field(
        False,
        title="Retain",
        description="Retain messages on broker.",
    )


class PubSubClientConfig(BaseSettings, Model):
    """Kelvin Pub-Sub Client Configuration."""

    class Config(BaseSettings.Config, Model.Config):
        """Pydantic configuration."""

        keep_untouched = (cached_property,)
        env_prefix = "KELVIN_PUBSUB_CLIENT__"

    broker_url: MQTTUrl = Field(
        f"mqtt://{DEFAULT_MQTT_HOST}",
        title="Kelvin Broker URI",
        description="Kelvin Broker URI. e.g. mqtt://localhost:1883",
    )
    client_id: Optional[str] = Field(
        None,
        title="Client ID",
        description="Client ID.",
    )
    username: Optional[str] = Field(
        None,
        title="Username",
        description="Broker username.",
    )
    password: Optional[str] = Field(
        None,
        title="Password",
        description="Broker password.",
    )
    sync: bool = Field(
        True,
        title="Default Connection",
        description="Default connection type: sync/async",
    )
    qos: QOS = Field(
        QOS.AT_MOST_ONCE,
        title="Quality of Service",
        description="Quality of service for message delivery.",
    )
    max_items: int = Field(
        1024,
        title="Max Items",
        description="Maximum number of items to hold in sync receive queue.",
        ge=0,
    )

    @root_validator(pre=True)
    def validate_app_config(cls, values: Dict[str, Any]) -> Any:
        """Validate app configuration field and fill missing client configuration."""

        root_config = values.get("app_config")
        if root_config is None:
            return values

        if isinstance(root_config, str):
            root_config = Path(root_config.strip()).expanduser().resolve()
            if not root_config.exists():
                raise ValueError(f"App configuration file {str(root_config)} not found") from None
            if not root_config.is_file():
                raise ValueError(f"Invalid app configuration file {str(root_config)}") from None

        if isinstance(root_config, Mapping):
            pass
        elif isinstance(root_config, Path):
            root_config = values["app_config"] = yaml.safe_load(root_config.read_text())
        else:
            raise ValueError(
                f"Invalid app configuration type {type(root_config).__name__!r}"
            ) from None

        environment_config = root_config.get("environment", {})

        for name in ["node_name", "workload_name"]:
            if name not in values and name in environment_config:
                values[name] = environment_config[name]

        app_type = root_config.get("app", {}).get("type")
        if app_type is None:
            raise ValueError("Missing app type") from None
        if not isinstance(app_type, str):
            raise TypeError(f"Invalid app type {type(app_type).__name__!r}") from None

        app_config = deep_get(root_config, f"app.{app_type}", {})

        if app_type == "kelvin":
            if "global" not in values and "global" in app_config:
                defaults = app_config["global"] or {}
                values["metric_defaults"] = {k: v for k, v in defaults.items() if k in SELECTORS}

            for name in IO_FIELDS:
                if name not in values and name in app_config:
                    keys = ["name", "data_type", "control_change", IO_FIELDS[name]]
                    default_opts: Dict[str, Any] = {}
                    if name == "outputs":
                        keys += ["storage", "retain"]
                        default_opts["retain"] = False
                    values[name] = [
                        {**default_opts, **{key: x[key] for key in keys if key in x}}
                        for x in app_config[name]
                    ]

        elif app_type == "bridge":
            inputs: List[Dict[str, Any]] = []
            outputs: List[Dict[str, Any]] = []

            def key(x: Mapping[str, Any]) -> Tuple[str, str, str, str, bool]:
                return (
                    x["name"],
                    x["data_type"],
                    x.get("access", "RO"),
                    x.get("storage", "node-and-cloud"),
                    x.get("retain", True),
                )

            metric_groups = groupby(sorted(app_config.get("metrics_map", []), key=key), key=key)

            for (name, data_type, access, storage, retain), entries in metric_groups:
                item = {
                    "name": name,
                    "data_type": data_type,
                    "metrics": [{"asset_names": [x["asset_name"] for x in entries]}],
                }

                if access == "RW":
                    inputs += [{**item, "control_change": True}]

                item.update({"storage": storage, "retain": retain})

                outputs += [item]

            if "inputs" not in values and inputs:
                values["inputs"] = inputs
            if "outputs" not in values and outputs:
                values["outputs"] = outputs

        else:
            raise ValueError(f"Invalid app type {app_type!r}") from None

        if "broker_url" not in values and "mqtt" in app_config:
            mqtt_config = app_config["mqtt"]
            ip = mqtt_config.get("ip")
            if ip is not None:
                port = mqtt_config.get("port")
                if "://" in ip:
                    transport, _, host = ip.partition("://")
                    if transport == "tcp":
                        scheme = "mqtt"
                    elif transport == "ssl":
                        scheme = "mqtts"
                    else:
                        raise ValueError(f"Unsupported transport {transport!r}") from None
                else:
                    host = ip
                    scheme = "mqtt"

                broker_url = f"{scheme}://{host}"
                if port:
                    broker_url = f"{broker_url}:{port}"

                values["broker_url"] = broker_url

            credentials = deep_get(mqtt_config, "authentication.credentials", {})
            if credentials:
                values["username"] = credentials.get("username")
                values["password"] = credentials.get("password")

        return values

    app_config: Optional[Dict[str, Any]] = Field(
        None,
        title="Application Configuration",
        description="Application configuration.",
    )

    @root_validator(pre=True)
    def validate_env(cls, values: Dict[str, Any]) -> Any:
        """Validate environment fields."""

        for name, sources in ENV_FIELDS.items():
            value = values.get(name)
            if value is not None:
                continue
            for source in sources:
                try:
                    values[name] = os.environ[source]
                except KeyError:
                    continue
                else:
                    break

        return values

    node_name: DNSName = Field(
        ...,
        title="ACP Name",
        description="ACP name.",
    )
    workload_name: DNSName = Field(
        ...,
        title="Workload Name",
        description="Workload name.",
    )

    asset_name: Optional[DottedName] = Field(
        None,
        title="Asset Name",
        description="Asset name.",
    )
    metric_defaults: Metric = Field(
        {},
        title="Metric Defaults",
        description="Metric defaults.",
    )

    @validator(*IO_FIELDS, pre=True, always=True)
    def validate_io(cls, value: Any, values: Dict[str, Any], field: ModelField) -> Any:
        """Validate IO."""

        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            return value

        names: Set[str] = {*[]}
        errors: List[ErrorWrapper] = []

        metric_defaults = values.get("metric_defaults", {})

        value = [*value]  # don't mutate original
        for i, x in enumerate(value):
            if not isinstance(x, Mapping):
                continue

            x = value[i] = {**x}  # don't mutate original

            name = x.get("name")
            if not isinstance(name, str):
                continue

            if name not in names:
                names |= {name}
            else:
                errors += [ErrorWrapper(ValueError(f"Name {name!r} must be unique"), loc=(i,))]

            metrics = x.get("metrics", ...)
            if metrics is ...:
                field_name = IO_FIELDS[field.name]
                if field_name in x:
                    metrics = x.pop(field_name)
                else:
                    metrics = None

            if not metrics:
                metrics = [{}]

            # apply defaults
            x["metrics"] = [{**metric_defaults, **metric} for metric in metrics]

        if errors:
            raise ValidationError(errors, model=cast(Type[PubSubClientConfig], cls)) from None

        return value

    inputs: List[Input] = Field(
        [],
        title="Inputs",
        description="Message inputs.",
    )
    outputs: List[Output] = Field(
        [],
        title="Outputs",
        description="Message outputs.",
    )

    def _expand_selector(self, selector: Selector) -> Tuple[str, str, str, str]:
        """Expand selector and set defaults."""

        node_name, workload_name, asset_name, name = selector

        return (
            node_name or self.node_name,
            workload_name or self.workload_name,
            asset_name or self.asset_name or "",
            name,
        )

    @cached_property
    def input_map(self) -> Dict[Selector, List[Tuple[str, str, str]]]:
        """Input map."""
        result: DefaultDict[Selector, Set[Tuple[str, str, str]]] = defaultdict(set)

        for io in self.inputs:
            for selector in io.combinations:
                node_name, workload_name, asset_name, name = selector
                if not name:
                    name = io.name

                if io.control_change:
                    topic_type = "input"
                    levels = [self.node_name, self.workload_name, asset_name, name]
                else:
                    topic_type = "output"
                    node = node_name or self.node_name if workload_name else ""
                    levels = [node, workload_name, asset_name, name]

                key = Selector(*levels)
                path = "/".join(str(x) or WILDCARD for x in levels)
                result[key] |= {(f"{topic_type}/{path}", io.name, io.data_type)}

        return {k: sorted(v) for k, v in sorted(result.items())}

    @cached_property
    def input_topics(self) -> List[str]:
        """Input topics."""

        return sorted({topic for x in self.input_map.values() for topic, *_ in x})

    @cached_property
    def output_map(self) -> Dict[Selector, List[Tuple[str, str, str, bool, bool]]]:
        """Output map."""

        result: DefaultDict[Selector, Set[Tuple[str, str, str, bool, bool]]] = defaultdict(set)

        source = (self.node_name, self.workload_name)

        for io in self.outputs:
            for selector in io.combinations:
                node_name, workload_name, asset_name, name = self._expand_selector(selector)
                if not name:
                    name = io.name

                key = Selector(node_name, workload_name, asset_name, io.name)
                if io.control_change:
                    topic_type = "control"
                    levels = [self.node_name, asset_name, name]
                elif (node_name, workload_name) == source:
                    topic_type = "output"
                    levels = [self.node_name, self.workload_name, asset_name, name]
                else:
                    topic_type = "input"
                    levels = [node_name, workload_name, asset_name, name]

                path = "/".join(str(x) or WILDCARD for x in levels)
                result[key] |= {
                    (f"{topic_type}/{path}", name, io.data_type, io.retain, io.control_change)
                }

        return {k: sorted(v) for k, v in sorted(result.items())}

    @cached_property
    def output_topics(self) -> List[str]:
        """Output topics."""

        return sorted({topic for x in self.output_map.values() for topic, *_ in x})

    @cached_property
    def storage_config(self) -> Dict[Selector, Tuple[Access, Storage, DottedName]]:
        """Storage configuration."""

        result: Dict[Selector, Tuple[Access, Storage, DottedName]] = {}

        source = (self.node_name, self.workload_name)
        for output in self.outputs:
            for selector in output.combinations:
                node_name, workload_name, asset_name, name = self._expand_selector(selector)
                if (node_name, workload_name) != source or output.control_change:
                    continue

                key = Selector(node_name, workload_name, asset_name, name or output.name)
                result[key] = (Access.RO, output.storage, output.data_type)
        # promote to RW if item is both input and output
        for input in self.inputs:
            for selector in input.combinations:
                node_name, workload_name, asset_name, name = self._expand_selector(selector)
                if not input.control_change:
                    continue

                key = Selector(node_name, workload_name, asset_name, name or input.name)
                access = Access.RW if key in result else Access.WO
                _, storage, data_type = result.pop(
                    key, (input.name, Storage.NODE_CLOUD, input.data_type)
                )
                result[key] = (access, storage, data_type)

        return result

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return iter(self.__dict__)
