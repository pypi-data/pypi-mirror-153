"""Base Application."""

from __future__ import annotations

import heapq
import uuid
from abc import ABCMeta
from collections import ChainMap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Flag, IntEnum, auto
from functools import partial
from itertools import groupby, product
from operator import attrgetter, itemgetter
from random import choices
from string import ascii_lowercase, digits
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

import structlog
import yaml
from pkg_resources import working_set
from pydantic import ValidationError
from structlog import BoundLogger

from kelvin.sdk.client import Client
from kelvin.sdk.datatype import Message, make_message
from kelvin.sdk.datatype.utils import snake_name, to_rfc3339_timestamp

from ...core.application import ApplicationInterface
from ...core.application import DataApplication as _DataApplication
from ...core.application import PollerApplication as _PollerApplication
from ...core.context import ContextInterface
from .config import ApplicationConfig, Check, DefaultConfig, Limit, Topic
from .context import Context
from .data import DataBuffer, DataStorage
from .mapping_proxy import MappingProxy
from .utils import (
    DurationType,
    TimeType,
    get_client,
    get_distribution,
    merge,
    resolve_period,
    topic_pattern,
)

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter
    from pandas import DataFrame
else:
    PrettyPrinter = Any
    DataFrame = Any


class MessageSelector(NamedTuple):
    """Message selector."""

    node_name: str
    workload_name: str
    asset_name: str
    # name: str


class MessageInfo:
    """Message info."""

    name: str
    data_type: str
    control_change: bool
    selectors: Set[MessageSelector]

    def __init__(
        self,
        name: str,
        data_type: str,
        control_change: bool = False,
        selectors: Optional[Collection[Any]] = None,
    ) -> None:
        """Initialise message info."""

        self.name = name
        self.data_type = data_type
        self.control_change = control_change
        self.selectors: Set[MessageSelector] = {*[]}

        if selectors is None:
            return

        # expand selectors if necessary
        keys = [
            "node_names",
            "workload_names",
            "asset_names",
            # "names",  # not in use
        ]
        for selector in selectors:
            if isinstance(selector, Mapping):
                args = [selector.get(key) or [""] for key in keys]
                self.selectors |= {MessageSelector(*x) for x in product(*args)}
            else:
                self.selectors |= {MessageSelector(*selector)}

    def __eq__(self, x: Any) -> bool:
        """Determine if objects have the same values."""

        if not isinstance(x, MessageInfo):
            return False

        return vars(self) == vars(x)

    def __str__(self) -> str:
        """Return str(self)."""

        name = type(self).__name__

        return f"<{name}>({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})"

    def __repr__(self) -> str:
        """Return repr(self)."""

        return str(self)

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__

        with p.group(4, f"<{name}>(", ")"):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            for i, (k, v) in enumerate(vars(self).items()):
                if i:
                    p.text(",")
                    p.breakable()
                else:
                    p.breakable("")
                p.text(f"{k}=")
                p.pretty(v)


@dataclass(frozen=True)
class MessageInterface:
    """Application message interfaces."""

    inputs: Dict[str, MessageInfo] = field(default_factory=dict)
    outputs: Dict[str, MessageInfo] = field(default_factory=dict)
    configuration: Dict[str, MessageInfo] = field(default_factory=dict)
    parameters: Dict[str, MessageInfo] = field(default_factory=dict)


class DataStatus(Flag):
    """Data status."""

    OK = 0
    MISSING = auto()
    STALE = auto()
    LOW_COUNT = auto()
    LOW_FREQ = auto()


class AppStatus(IntEnum):
    """Application status."""

    NOT_INITIALIZED = 0
    INITIALIZED = auto()
    TERMINATED = auto()


def topic_key(x: Tuple[str, Any]) -> str:
    """Sort topics in order of specificity (* > #)."""

    k, _ = x

    # push dangling wildcards to end (#.* > #)
    if k.endswith("#"):
        k += "~"

    return k.replace("*", "~").replace("#", "~~")


class BaseApplicationMeta(ABCMeta):
    """Application metaclass."""

    def __new__(
        metacls: Type[BaseApplicationMeta],
        name: str,
        bases: Tuple[Type, ...],
        __dict__: Dict[str, Any],
    ) -> BaseApplicationMeta:
        """Create Application class."""

        parents: List[Type[BaseApplication]] = [
            T for T in bases if isinstance(T, BaseApplicationMeta)
        ]

        try:
            dist = get_distribution(__dict__["__module__"])
        except ModuleNotFoundError:  # pragma: no cover
            version = None
        else:
            version = dist.version if dist is not None else None

        try:
            checks = merge(
                {},
                *(T._checks for T in parents),
                {name: Check(**x) for name, x in __dict__.pop("CHECKS", {}).items()},
            )
            limits = merge(
                {},
                *(T._limits for T in parents),
                {name: Limit(**x) for name, x in __dict__.pop("LIMITS", {}).items()},
            )
            topics = merge(
                {},
                *(T._topics for T in parents),
                {
                    pattern: Topic(**{"pattern": pattern, **x})
                    for pattern, x in __dict__.pop("TOPICS", {}).items()
                },
            )
        except ValidationError as e:
            raise TypeError(e) from None

        source = __dict__.get("__annotations__", {}).get("config")
        if source is not None:
            T = __dict__["_config_type"] = (
                eval(source) if isinstance(source, str) else source  # nosec
            )
            if not isinstance(T, type) or not issubclass(T, ApplicationConfig):
                raise TypeError(f"{T.__name__!r} is not a subclass of 'ApplicationConfig'")

        __dict__.update(
            {
                "_name": snake_name(name),
                "_version": version,
                "_checks": {k: v for k, v in sorted(checks.items(), key=itemgetter(0))},
                "_limits": {k: v for k, v in sorted(limits.items(), key=itemgetter(0))},
                "_topics": {k: v for k, v in sorted(topics.items(), key=topic_key)},
            }
        )

        return cast(BaseApplicationMeta, super().__new__(metacls, name, bases, __dict__))


class State:
    """State for application."""

    PROTECTED = {"buffer", "last_message", "data", "buffer"}

    def __init__(self, asset_name: Optional[str] = None) -> None:
        """Initialise state."""

        self.asset_name = asset_name

        self.data = MappingProxy({}, name="data")
        self.params = MappingProxy({}, name="params")
        self.buffer: List[Tuple[Tuple[int, int], Message]] = []
        self.last_message: Dict[Tuple[str, str], Message] = {}
        self.callbacks: List[Tuple[float, str, float, int, Callable[..., None]]] = []

        self.last_process_time: float = 0.0
        self.input_count: int = 0
        self.output_count: int = 0

    def reset(self) -> None:
        """Reset application."""

        self.data.clear()
        self.buffer.clear()
        self.last_message.clear()
        self.last_process_time = 0.0
        self.input_count = self.output_count = 0

    @property
    def timestamps(self) -> Dict[Tuple[str, str], int]:
        """Get last time of validity of received/emitted messages."""

        return {k: v._.time_of_validity for k, v in self.last_message.items()}

    @property
    def last_time_of_validity(self) -> int:
        """Get time of validity of last-received message."""

        return max(self.timestamps.values(), default=0)

    def __str__(self) -> str:
        """Return str(self)."""

        name = type(self).__name__

        return f"<{name}>({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})"

    def __repr__(self) -> str:
        """Return repr(self)."""

        return str(self)

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__

        with p.group(4, f"<{name}>(", ")"):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            for i, (k, v) in enumerate(vars(self).items()):
                if i:
                    p.text(",")
                    p.breakable()
                else:
                    p.breakable("")
                p.text(f"{k}=")
                p.pretty(v)


class BaseApplication(ApplicationInterface, metaclass=BaseApplicationMeta):
    """
    Base Application.

    Parameters
    ----------
    context : :obj:`ContextInterface`
        Application context containing the methods bound to the application implementation (C++)
    configuration : :obj:`dict`, optional
        Optional initial configuration
    startup_time: :obj:`float`, optional
        Optional startup time

    """

    config: ApplicationConfig

    # inputs to metaclass
    CHECKS: Mapping[str, Mapping[str, Any]] = {}
    LIMITS: Mapping[str, Mapping[str, Any]] = {}
    TOPICS: Mapping[str, Mapping[str, Any]] = {"#": {"target": "{name}"}}

    # outputs of metaclass
    _name: str
    _version: str
    _checks: Mapping[str, Check]
    _limits: Mapping[str, Limit]
    _topics: Mapping[str, Topic]
    _app_configuration: Mapping[str, Any]
    _asset_properties: Mapping[str, Any]
    _client: Optional[Client] = None
    _config_type: Type[ApplicationConfig]

    # internals
    __asset_name: Optional[str] = None
    __states: Dict[Optional[str], State]
    __status = AppStatus.NOT_INITIALIZED

    def __new__(cls, *args: Any, **kwargs: Any) -> BaseApplication:
        """Initialise application internals."""

        obj = super().__new__(cls)

        obj._app_configuration = {}
        obj._asset_properties = {}
        obj.__states = {}
        obj.__logger = structlog.get_logger(cls._name)
        try:
            obj.config = cls._config_type()
        except ValueError:
            # fall back to basic config until initial config arrives
            obj.config = ApplicationConfig()

        return obj

    def __init__(
        self,
        context: Optional[ContextInterface] = None,
        startup_time: Optional[float] = None,
        configuration: Optional[Mapping[str, Any]] = None,
        app_configuration: Optional[Mapping[str, Any]] = None,
        parameters: Optional[Union[Sequence[Message], Mapping[str, Message]]] = None,
    ) -> None:
        """Initialise application."""

        if context is None:
            context = Context(self)

        if startup_time is None:
            startup_time = context.get_process_time()
        elif isinstance(context, Context):  # pragma: no cover
            context.set_process_time(startup_time)

        super().__init__(context)

        self.__startup_time = startup_time
        self.__interface = MessageInterface(
            inputs=self._convert_registry_map(self.get_input_registry_map()),
            outputs=self._convert_registry_map(self.get_output_registry_map()),
            configuration=self._convert_registry_map(self.get_configuration_registry_map()),
            parameters=self._convert_registry_map(self.get_parameter_registry_map()),
        )

        if configuration is not None or parameters is not None:
            self.on_initialize(
                configuration=configuration or {},
                app_configuration=app_configuration or {},
                parameters=parameters or {},
            )

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_") or name in {"config"} or name in super().__dir__():
            return super().__getattribute__(name)  # pragma: no cover

        return getattr(self.state, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Get attribute."""

        if name.startswith("_") or name in {"config"} or name in super().__dir__():
            return super().__setattr__(name, value)

        if name in State.PROTECTED:
            raise AttributeError(f"State attribute {name!r} is not writable")

        return setattr(self.state, name, value)

    @property
    def app_configuration(self) -> Mapping[str, Any]:
        """App configuration."""

        return self._app_configuration

    @property
    def asset_properties(self) -> MappingProxy:
        """Asset Properties."""

        asset_name = self.__asset_name

        if asset_name is not None:
            data = self._asset_properties.get(asset_name)
            if data is not None:
                data = {**data}
            else:
                data = {}
        else:
            data = {}

        return MappingProxy(data)

    @property
    def name(self) -> str:
        """App name."""

        return self._name

    @property
    def version(self) -> Optional[str]:
        """App version."""

        return self._version

    @property
    def status(self) -> AppStatus:
        """App status."""

        return self.__status

    @property
    def topics(self) -> Mapping[str, Topic]:
        """Data topics."""

        return ChainMap(self.config.kelvin.app.topics, self._topics)

    @property
    def checks(self) -> Mapping[str, Check]:
        """Data checks."""

        return ChainMap(self.config.kelvin.app.checks, self._checks)

    @property
    def limits(self) -> Mapping[str, Limit]:
        """Data limits."""

        return ChainMap(self.config.kelvin.app.limits, self._limits)

    @property
    def logger(self) -> BoundLogger:
        """App logger."""

        return self.__logger.bind(
            asset_name=self.__asset_name, last_process_time=self.last_process_time
        )

    @property
    def startup_time(self) -> float:
        """Startup Time."""

        return self.__startup_time

    @property
    def asset_name(self) -> Optional[str]:
        """Asset ID."""

        return self.__asset_name

    @asset_name.setter
    def asset_name(self, value: Optional[str]) -> None:
        """Asset ID."""

        self.__asset_name = value

    @property
    def state(self) -> State:
        """Startup Time."""

        try:
            state = self.__states[self.__asset_name]
        except KeyError:
            state = self.__states[self.__asset_name] = State(asset_name=self.__asset_name)

        return state

    @property
    def data(self) -> MappingProxy:
        """Data."""

        return self.state.data

    @property
    def params(self) -> MappingProxy:
        """Parameters."""

        return self.state.params

    @property
    def last_process_time(self) -> float:
        """Last Process Time."""

        state = self.__states.get(self.__asset_name)

        return state.last_process_time if state is not None else 0.0

    @property
    def input_count(self) -> int:
        """Get number of inputs received."""

        state = self.__states.get(self.__asset_name)

        return state.input_count if state is not None else 0

    @property
    def output_count(self) -> int:
        """Get number of outputs produced."""

        state = self.__states.get(self.__asset_name)

        return state.output_count if state is not None else 0

    @property
    def timestamps(self) -> Dict[Tuple[str, str], int]:
        """Get last time of validity of received/emitted messages."""

        state = self.__states.get(self.__asset_name)

        return state.timestamps if state is not None else {}

    @property
    def last_time_of_validity(self) -> int:
        """Get time of validity of last-received message."""

        state = self.__states.get(self.__asset_name)

        return state.last_time_of_validity if state is not None else 0

    def get_asset_properties(self, asset_name: str) -> Dict[str, Any]:
        """
        When provided with a specific asset, yield its properties, if existent.

        Parameters
        ----------
        asset_name: str
            the specified asset

        Returns
        -------
        A dictionary containing the asset properties of the specified asset.

        """

        return self._asset_properties.get(asset_name) or {}

    def add_topic(
        self,
        pattern: str,
        target: Optional[str] = None,
        storage_type: Optional[str] = None,
        storage_config: Optional[Mapping[str, Any]] = None,
        reprocess: bool = False,
    ) -> None:
        """Register a topic."""

        topic = Topic(
            pattern=pattern, target=target, storage_type=storage_type, storage_config=storage_config
        )
        topics = ChainMap({pattern: topic}, self._topics)

        self._topics = {k: v for k, v in sorted(topics.items(), key=topic_key)}

        if not reprocess:
            return

        for asset_name in self.__states:
            self.__asset_name = asset_name
            self.reprocess_messages()

    def remove_topic(self, pattern: str, reprocess: bool = True) -> None:
        """Unregister a topic."""

        self._topics = {
            k: v for k, v in sorted(self._topics.items(), key=topic_key) if k != pattern
        }

        if not reprocess:
            return

        for asset_name in self.__states:
            self.__asset_name = asset_name
            self.reprocess_messages()

    def add_check(
        self,
        name: str,
        min_count: Optional[int] = None,
        max_gap: Optional[DurationType] = None,
        max_lag: Optional[DurationType] = None,
    ) -> None:
        """Register a check."""

        checks = ChainMap(
            {name: Check(min_count=min_count, max_gap=max_gap, max_lag=max_lag)}, self._checks
        )

        self._checks = {k: v for k, v in sorted(checks.items())}

    def remove_check(self, name: str) -> None:
        """Unregister a check."""

        self._checks = {k: v for k, v in sorted(self._checks.items()) if k != name}

    def add_limit(
        self,
        name: str,
        frequency: Optional[DurationType] = None,
        throttle: Optional[DurationType] = None,
    ) -> None:
        """Register a limit."""

        limits = ChainMap({name: Limit(frequency=frequency, throttle=throttle)}, self._limits)

        self._limits = {k: v for k, v in sorted(limits.items())}

    def remove_limit(self, name: str) -> None:
        """Unregister a limit."""

        self._limits = {k: v for k, v in sorted(self._limits.items()) if k != name}

    def reset(self) -> None:
        """Reset application."""

        self.state.reset()

    def on_initialize(
        self,
        configuration: Mapping[str, Any],
        app_configuration: Optional[Mapping[str, Any]] = None,
        parameters: Optional[Union[Sequence[Message], Mapping[str, Message]]] = None,
    ) -> bool:
        """Initialise application with configuration."""

        self.logger.debug(
            "on_initialize",
            name=self._name,
            version=self._version,
            class_name=type(self).__name__,
            packages={
                key: version
                for key, version in sorted(
                    (x.key, x.version) for x in working_set if x.key.startswith("kelvin-")
                )
            },
        )

        if not type(self.config) is self._config_type:
            self.config = self._config_type(**configuration)
        else:
            self.config.update(configuration)

        if parameters is not None:
            self.on_parameter_change(parameters)

        if self.config.kelvin.app.asset_getter is None:
            # TODO: per-asset select

            state = self.state

            if self.config.kelvin.app.last_outputs:
                last_message = {
                    (message._.name, message._.type): message
                    for name, message_info in self.interface.outputs.items()
                    for message in self.select(name, self.__startup_time, 1e-6, limit=1)
                    if message._.type == message_info.data_type
                }
                state.last_message.update(last_message)

            pre_fill = self.config.kelvin.app.pre_fill
            names = [*self.interface.inputs]

            if pre_fill and names and self.__startup_time > 0:
                self.logger.info("Pre-filling data", pre_fill=pre_fill, names=names)
                start, end = max(self.__startup_time - pre_fill, 0), self.__startup_time
                limit = 1 << 16
                for name in self.interface.inputs:
                    self.process_messages(self.select(name, start, end, limit=limit))

        self._app_configuration = MappingProxy(
            {**app_configuration} if app_configuration is not None else {}
        )
        self._asset_properties = {
            x["name"]: x.get("properties", {})
            for x in self._app_configuration.get("app.kelvin.assets", [])
        }

        self.init()

        self.__status = AppStatus.INITIALIZED

        return True

    def _partition_messages(
        self, data: Sequence[Message]
    ) -> Iterable[Tuple[Optional[str], Iterable[Message]]]:
        """Collate data by asset-id getter."""

        data = sorted(data, key=attrgetter("_.time_of_validity"))

        asset_getter = self.config.kelvin.app.asset_getter
        if asset_getter is None:
            return [(None, data)]

        getter = cast(Callable[[Message], str], attrgetter(*asset_getter))

        return groupby(sorted(data, key=lambda x: getter(x) or ""), key=getter)

    def on_parameter_change(
        self, parameters: Union[Sequence[Message], Mapping[str, Message]]
    ) -> bool:
        """Update application with new parameters."""

        self.logger.debug("on_parameter_change")

        if not parameters:
            return False

        if isinstance(parameters, Mapping):
            parameters = [*parameters.values()]

        for asset_name, messages in self._partition_messages(parameters):
            self.__asset_name = asset_name
            updates: Dict[str, Tuple[Any, Any]] = {}
            params = MappingProxy({**self.state.params})
            for message in messages:
                self.state.params[message._.name] = message

            for name, new in self.state.params.flatten(deep=True):
                old = params.get(name)
                if old != new:
                    updates[name] = (old, new)

            if updates:
                self.accept_params(updates)

        return True

    def emit_value(
        self,
        name: str,
        value: Any,
        asset_name: Optional[str] = None,
        time_of_validity: Optional[int] = None,
        type: str = "object",
    ) -> Message:
        """Emit an arbitrary value."""
        return self.make_message(
            type,
            value=value,
            _name=name,
            _asset_name=asset_name,
            _time_of_validity=time_of_validity,
            emit=True,
        )

    def emit(self, data: Union[Message, Sequence[Message]]) -> None:
        """Takes the incoming data and publishes the contents to the software
        bus."""

        if not isinstance(data, Sequence):
            data = [data]

        for message in data:
            key = message_name, message_type = message._.name, message._.type
            if not message_name:
                self.logger.warning("Emitted messages require a name", message_type=message_type)
                continue

            limit = self.limits.get(message_name)
            if limit is not None:
                throttle, frequency = limit.throttle or 0.0, limit.frequency or 0.0
                last_message = self.state.last_message.get(key)
                if last_message is not None:
                    lag = (
                        max(message._.time_of_validity - last_message._.time_of_validity, 0.0) / 1e9
                    )

                    if lag < throttle:
                        # update last known
                        self.state.last_message[key] = message
                    if lag < max(throttle, frequency):
                        continue

            self.state.output_count += 1
            self.state.last_message[key] = message

            super().emit(message)

    def on_terminate(self) -> bool:
        """
        ``on_terminate`` is called when the application is being terminated.

        This allows application to clean up resources that might have
        been allocated internally, cleanly close out logs, etc. to
        initialize the particular application.

        """

        self.logger.debug("on_terminate")

        self.__status = AppStatus.TERMINATED

        return True

    def select(
        self,
        name: str,
        start: Optional[TimeType] = None,
        end: Optional[TimeType] = None,
        limit: int = 1000,
    ) -> List[Message]:
        """
        Get a list of metrics from the application storage.

        Accesses the application storage and returns a list of metrics for the specified metric name. The returned
        metrics will be filtered using the start and end dates specified and the number of desired results will be
        limited by the amount of the specified limit.

        Parameters
        ----------
        name : :obj:`str`
            The name of the metric to be looked up in the application storage.
        start : :obj:`float`, :obj:`datetime`, :obj:`timedelta`, optional
            Extract window start.
        end : :obj:`float`, :obj:`datetime`, :obj:`timedelta`, optional
            Extract window end.
        limit : :obj:`int`
            The maximum number of desired data points.

        """

        start, end = resolve_period(start, end)

        return super().select(name, start.timestamp(), end.timestamp(), limit)

    @property
    def process_time(self) -> float:
        """Process time."""

        return self.get_process_time()

    def push_buffer(self, message: Message, expiry: Optional[int] = None) -> None:
        """Push value into buffer."""

        if expiry is None:
            expiry = message._.time_of_validity

        heapq.heappush(self.state.buffer, ((expiry, id(message)), message))

    def pop_buffer(self, cutoff: Optional[float] = None) -> Optional[Message]:
        """Pop value from buffer."""

        if not self.state.buffer:
            return None

        if cutoff is None:
            cutoff = int(self.state.last_process_time * 1e9)

        (expiry, _), message = heapq.heappop(self.state.buffer)

        if expiry > cutoff:
            self.push_buffer(message, expiry)
            return None

        return message

    def _pop_messages(self, cutoff: Optional[float] = None) -> List[Message]:
        """Pop messages past cutoff."""

        data: List[Message] = []

        while True:
            x = self.pop_buffer()
            if x is None:
                break
            data += [x]

        return data

    def process_messages(
        self, data: Optional[Sequence[Message]] = None, check: bool = True
    ) -> List[Message]:
        """Process data."""

        if data is None:
            data = self._pop_messages()

        remove_duplicates = self.config.kelvin.app.remove_duplicates

        result: List[Message] = []

        for message in data:
            key = (message._.name, message._.type)
            last_message = self.state.last_message.get(key)

            if check:
                if remove_duplicates and last_message == message:
                    continue

                self.state.last_message[key] = message
                self.state.input_count += 1

            result += [message]

            try:
                self.store(message)
            except Exception:  # pragma: no cover
                self.logger.exception(
                    "Unable to store message",
                    message_name=message._.name,
                    message_type=message._.type,
                )

        cutoff = int(self.state.last_process_time * 1e9)

        # clean up buffers
        for k, v in self.state.data.flatten():
            if isinstance(v, DataBuffer):
                v.cleanup(cutoff)

        return result

    def reprocess_messages(self) -> None:
        """Rebuild data structure."""

        if not self.input_count:
            return

        data = [
            message
            for _, messages in self.state.data.flatten()
            for message in (messages if isinstance(messages, DataBuffer) else [messages])
        ]
        self.state.data.clear()
        self.process_messages(sorted(data, key=attrgetter("_.time_of_validity")), check=False)

    def _process(self, last_process_time: float) -> None:
        """Process all assets."""

        for asset_name in self.__states:
            self.__asset_name = asset_name
            if not self.config.kelvin.app.offset_timestamps:
                self.state.last_process_time = last_process_time
            try:
                data = self.process_messages()
                self.process_data(data)
                self.process()
            except Exception:  # pragma: no cover
                self.logger.exception("Failed to process data")

            self.process_callbacks(last_process_time)

    def accept_params(self, updates: Mapping[str, Tuple[Any, Any]]) -> None:
        """Override this to implement accepting new parameters."""

        ...

    def init(self) -> None:
        """Override this to implement initialisation of application."""

        ...

    def process_data(self, data: Sequence[Message]) -> None:
        """Override this to implement logic of application."""

        ...

    def process(self) -> None:
        """Override this to implement logic of application."""

        ...

    def make_message(
        self,
        _type: Optional[str] = None,
        _name: Optional[str] = None,
        _time_of_validity: Optional[Union[int, float]] = None,
        _source: Optional[Mapping[str, Optional[str]]] = None,
        _target: Optional[Mapping[str, Optional[str]]] = None,
        _asset_name: Optional[str] = None,
        emit: bool = False,
        store: bool = False,
        **kwargs: Any,
    ) -> Message:
        """
        Create a message object.

        Parameters
        ----------
        _type : str, optional
            Message type (e.g. ``raw.float32``, ``kelvin.beam_pump``)
        _name : str, optional
            Message name
        _time_of_validity : int, optional
            Time of validity in nano-seconds
        _source : dict, optional
            Message source
        _target : dict, optional
            Message target
        _asset_name : str, optional
            Asset name
        emit : bool, optional
            Emit the message
        store : bool, optional
            Store the message
        **kwargs:
            Additional properties for message (e.g. ``value`` for raw types)

        """

        _type, _name = _type or kwargs.pop("type", None), _name or kwargs.pop("name", None)

        if _name is None:
            raise ValueError("No message name") from None

        interface = self.interface

        try:
            message_info = interface.outputs[_name]
        except KeyError:
            raise ValueError(f"Unknown message {_name!r}") from None

        type_ = message_info.data_type
        if _type is None:
            _type = type_
        elif _type != type_:
            raise ValueError(
                f"Message type {_type!r} differs from expected type {type_!r} for {_name!r}"
            ) from None

        if _type is None:
            raise ValueError(f"Message type unknown for {_name!r}") from None

        if _time_of_validity is None:
            _time_of_validity = int(self.last_process_time * 1e9)

        info = self.config.kelvin.get("info", {})

        asset_name = self.__asset_name or ""

        if _source is None:
            _source = {}

        source_node_name = _source.get("node_name") or info.get("node_name") or ""
        source_workload_name = _source.get("workload_name") or info.get("workload_name") or ""

        if _target is None:
            _target = {}

        node_name = _target.get("node_name") or ""
        workload_name = _target.get("workload_name") or ""

        query = (node_name, workload_name, _asset_name or asset_name or "")
        defaults = (source_node_name, source_workload_name, asset_name)

        selectors = message_info.selectors
        if selectors:
            matches = [
                selector
                for selector in selectors
                if all(x == y or not (x and y) for x, y in zip(selector, query))
            ]
            n = len(matches)
            if n == 1:
                # single match
                selector, *_ = matches
                node_name, workload_name, _asset_name = [
                    x or y or z for x, y, z in zip(selector, query, defaults)
                ]
            elif not n:
                raise ValueError(f"Message target {'/'.join(query)!r} not supported") from None
            else:
                raise ValueError(f"Ambiguous target {'/'.join(query)!r}") from None
        else:
            node_name, workload_name, _asset_name = [x or y for x, y in zip(query, defaults)]

        _source = {"node_name": source_node_name, "workload_name": source_workload_name}
        _target = {"node_name": node_name, "workload_name": workload_name}

        message = cast(
            Message,
            make_message(
                _type,
                _name,
                _time_of_validity,
                _source=_source,
                _target=_target,
                _asset_name=_asset_name,
                **kwargs,
            ),
        )

        if emit:
            self.emit(message)

        if store:
            self.store(message)

        return message

    def make_control_change(
        self,
        _name: str,
        _expiration: Union[int, float],
        _timeout: Optional[int] = None,
        _retries: Optional[int] = None,
        _target: Optional[Mapping[str, Optional[str]]] = None,
        _asset_name: Optional[str] = None,
        _type: Optional[str] = None,
        emit: bool = False,
        store: bool = False,
        **kwargs: Any,
    ) -> Message:
        """
        Create a control change message object.

        Parameters
        ----------
        _name : str
            Message name
        _expiration : int, float, optional
            control change expiration in seconds
        _timeout : int, optional
            control change timeout in seconds
        _retries : int, optional
            control change number of retries
        _target : dict, optional
            Message target
        _asset_name : str, optional
            Asset name
        _type : str, optional
            Message type (e.g. ``raw.float32``, ``kelvin.beam_pump``)
        emit : bool, optional
            Emit the message
        store : bool, optional
            Store the message
        **kwargs:
            Additional properties for message (e.g. ``value`` for raw types)

        """

        # keep backwards compatibility of _value arg
        if "_value" in kwargs:
            kwargs["value"] = kwargs.pop("_value")

        _type, _name = _type or kwargs.pop("type", None), _name or kwargs.pop("name", None)

        if _name is None:
            raise ValueError("No message name") from None

        interface = self.interface

        try:
            message_info = interface.outputs[_name]
        except KeyError:
            raise ValueError(f"Unknown message {_name!r}") from None

        if not message_info.control_change:
            raise ValueError(f"Message {_name!r} is not a control change") from None

        type_ = message_info.data_type
        if _type is None:
            _type = type_
        elif _type != type_:
            raise ValueError(
                f"Message type {_type!r} differs from expected type {type_!r} for {_name!r}"
            ) from None

        if _type is None:
            raise ValueError(f"Message type unknown for {_name!r}") from None

        info = self.config.kelvin.get("info", {})

        asset_name = self.__asset_name or ""

        source_node_name = info.get("node_name", "")
        source_workload_name = info.get("workload_name", "")

        if _target is None:
            _target = {}

        node_name = _target.get("node_name") or ""
        workload_name = _target.get("workload_name") or ""

        query = (node_name, workload_name, _asset_name or asset_name or "")
        defaults = (source_node_name, source_workload_name, asset_name)

        selectors = message_info.selectors
        if selectors:
            matches = [
                selector
                for selector in selectors
                if all(x == y or not (x and y) for x, y in zip(selector, query))
            ]
            n = len(matches)
            if n == 1:
                # single match
                selector, *_ = matches
                node_name, workload_name, _asset_name = [
                    x or y or z for x, y, z in zip(selector, query, defaults)
                ]
            elif not n:
                raise ValueError(f"Message target {'/'.join(query)!r} not supported") from None
            else:
                raise ValueError(f"Ambiguous target {'/'.join(query)!r}") from None
        else:
            node_name, workload_name, _asset_name = [x or y for x, y in zip(query, defaults)]

        _source = {"node_name": source_node_name, "workload_name": source_workload_name}
        _type = "kelvin.control_change"
        _time_of_validity = int(self.last_process_time * 1e9)
        expiration_date_datetime = datetime.fromtimestamp(
            (self.last_process_time + _expiration), timezone.utc
        )
        expiration_date = to_rfc3339_timestamp(expiration_date_datetime)
        msg_uuid = str(uuid.uuid1())

        message = cast(
            Message,
            make_message(
                _type,
                _name,
                _time_of_validity,
                _source=_source,
                expiration_date=expiration_date,
                timeout=_timeout,
                retries=_retries,
                _target=_target,
                _asset_name=_asset_name,
                _id=msg_uuid,
                _trace_id=msg_uuid,
                payload=kwargs,
            ),
        )

        if emit:
            self.emit(message)

        if store:
            self.store(message)

        return message

    def _targets(
        self, message: Message
    ) -> Dict[str, Tuple[str, Optional[Callable[[Sequence[Message]], DataStorage]]]]:
        """
        Find targets for message in topic.

        Parameters
        ----------
        message : :obj:`Message`
            Message to store

        """

        targets: Dict[
            str,
            Tuple[
                str,
                Optional[Callable[[Sequence[Message]], DataStorage]],
            ],
        ] = {}

        final = False

        # find topic(s) among matchers
        for pattern, topic in self.topics.items():
            if final:
                break
            if not topic.match(f"{message._.type}.{message._.name}"):
                continue

            target = topic.target
            final = topic.final

            if target is None:
                # stop here - return any earlier matches
                break

            if "{" in target:
                try:
                    target = target.format_map(ChainMap(message, message._))
                except Exception:
                    self.logger.exception("Invalid topic target", pattern=pattern, target=target)
                    continue

            if target in targets:
                continue

            targets[target] = (pattern, topic.init)

        return targets

    def store(self, message: Message, target: Optional[str] = None) -> List[str]:
        """
        Store messages in data.

        Parameters
        ----------
        message : :obj:`Message`
            Message to store
        target : :obj:`str`, optional
            Optional target override

        """

        if target is None:
            targets = self._targets(message)
        else:
            targets = {target: (target, None)}

        if not targets:
            self.logger.warning(
                "Unmatched message", message_name=message._.name, message_type=message._.type
            )
            return []

        result: List[str] = []

        for target, (pattern, init) in targets.items():
            try:
                self._store(message, target, init)
            except Exception:
                self.logger.exception(
                    "Unable to store message",
                    message_name=message._.name,
                    message_type=message._.type,
                    pattern=pattern,
                    target=target,
                )
                continue
            else:
                result += [target]

        return result

    def _store(
        self,
        message: Message,
        target: str,
        init: Optional[Callable[[Sequence[Message]], DataStorage]] = None,
    ) -> bool:
        """Store message in specific target."""

        # store single value
        if init is None:
            self.state.data[target] = message
        else:
            data = self.state.data.get(target)
            if data is not None:
                data += [message]
            else:
                self.state.data[target] = init([message])

        return True

    @property
    def frame(self) -> DataFrame:
        """Get a dataframe."""

        from pandas import DataFrame, DatetimeIndex

        data = {
            (*k.split("."),) if "." in k else k: v.series()
            for k, v in self.state.data.flatten()
            if isinstance(v, DataBuffer)
        }

        if not data:
            return DataFrame(index=DatetimeIndex([], name="time", tz="UTC"))

        return DataFrame(data)

    @property
    def data_status(self) -> Dict[str, DataStatus]:
        """Check if data is ready."""

        status: Dict[str, DataStatus] = {}

        timestamp = self.state.last_process_time

        for name, check in self.checks.items():
            if "#" in name or "*" in name:
                pattern = topic_pattern(name)
                names = [x for x in self.interface.inputs if pattern.match(x)]
            else:
                names = [name]

            for name in names:
                value = self.state.data.get(name)

                if value is None or not value:
                    status[name] = DataStatus.MISSING
                    continue

                if isinstance(value, DataBuffer):
                    min_count = check.min_count
                    if min_count is not None and len(value) < min_count:
                        status[name] = DataStatus.LOW_COUNT

                    max_gap = check.max_gap
                    if max_gap is not None:
                        timestamps = value.timestamps
                        for x, y in zip(timestamps[:-1], timestamps[1:]):
                            if y - x > max_gap * 1e9:
                                status[name] = DataStatus.LOW_FREQ
                                break

                    value = value[-1]

                max_lag = check.max_lag
                if max_lag is not None and value._.time_of_validity / 1e9 < timestamp - max_lag:
                    status[name] = DataStatus.STALE

        return status

    @property
    def context(self) -> ContextInterface:
        """Context."""

        return self._context

    def __str__(self) -> str:
        """Return str(self)."""

        name = type(self).__name__

        return f"<{name}>(state={self.state})"

    def __repr__(self) -> str:
        """Return repr(self)."""

        return str(self)

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*super().__dir__(), *vars(self.state)]

    def _pretty_items(self) -> List[Tuple[str, Any]]:
        """Pretty print items."""

        return [("config", self.config), ("state", self.state)]

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__

        with p.group(4, f"<{name}>(", ")"):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            for i, (k, v) in enumerate(self._pretty_items()):
                if i:
                    p.text(",")
                    p.breakable()
                else:
                    p.breakable("")
                p.text(f"{k}=")
                p.pretty(v)

    @staticmethod
    def _load_config(config: Union[str, Mapping[str, Any]]) -> Dict[str, Any]:
        """Load configuration."""

        return yaml.safe_load(config) if isinstance(config, str) else config  # pragma: no cover

    @staticmethod
    def _convert_registry_map(
        registry_map: Mapping[str, Mapping[str, Any]]
    ) -> Dict[str, MessageInfo]:
        return {name: MessageInfo(**config) for name, config in registry_map.items()}

    @property
    def interface(self) -> MessageInterface:
        """Interface information."""

        return self.__interface

    @property
    def client(self) -> Client:
        """API client."""

        if self._client is not None:
            return self._client

        client = self._client = get_client()

        return client

    def process_callbacks(self, process_time: Optional[float] = None) -> None:
        """Process callbacks."""

        if process_time is None:
            process_time = self.process_time

        callbacks = self.state.callbacks

        while callbacks:
            timestamp, name, period, count, callback = heapq.heappop(callbacks)
            if timestamp > process_time:
                heapq.heappush(callbacks, (timestamp, name, period, count, callback))
                break

            try:
                callback()
            except Exception:  # pragma: no cover
                self.logger.exception("Failed to process callback")

            if count > 0:
                count -= 1

            if count:
                heapq.heappush(callbacks, (timestamp + period, name, period, count, callback))

    def create_timer(
        self,
        callback: Callable[..., None],
        period: float,
        name: Optional[str] = None,
        count: int = 1,
        start: float = 0.0,
        kwargs: Optional[Mapping[str, Any]] = None,
    ) -> Optional[str]:
        """
        Take the incoming callback and period and registers it with the
        application.

        The callback will get triggered at the incoming period. The timer can
        be assigned a name, the number of times to be called, whether data
        should be aligned, and when the timer should be started.

        Parameters
        ----------
        callback : callable
            The callback to be attached to the application event loop
        period : float
            The time in seconds that the callback should be triggered on
        name : str, optional
            The name to be associated with the timer (default: a name will be generated)
        count : int, optional
            The number of times the callback should be triggered before being removed from
            the event loop. (default: 1)
        start : float, optional
            The delay in seconds that should be applied to start time of the
            timer (default: no delay)
        kwargs : dict, optional
            Optional arguments for callback

        Returns
        -------
        str
            The name of the created timer.

        """

        if name is not None:
            if any(name == x for _, x, *_ in self.state.callbacks):
                self.logger.warning("Timer already exists", timer_name=name)
                return None
        else:
            name = "".join(choices(ascii_lowercase + digits, k=8))

        if kwargs is not None:
            callback = partial(callback, **kwargs)

        item = (self.process_time + start + period, name, period, count, callback)
        heapq.heappush(self.state.callbacks, item)

        return name

    def delete_timer(self, name: str) -> None:
        """
        Takes the incoming timer name and removes it from the event loop.

        Parameters
        ----------
        name : str
            The name of the timer to be removed from the event loop.

        """

        n = len(self.state.callbacks)

        for i, (_, x, *_) in enumerate(reversed(self.state.callbacks), 1):
            if x == name:
                del self.state.callbacks[n - i]
                return

        self.logger.warning("No timer found", timer_name=name)

    def get_timers(self) -> Set[str]:
        """
        Get a listing of the timers that are registered with the event loop.

        Returns
        -------
        list
            The timers currently registered with the event loop.

        """

        return {name for _, name, *_ in self.state.callbacks}


class DataApplication(BaseApplication, _DataApplication):
    """Data Application."""

    config: DefaultConfig

    def on_data(self, data: Sequence[Message]) -> None:
        """Process data."""

        last_process_time = self.process_time

        self.logger.debug("on_data")

        if data:
            for asset_name, messages in self._partition_messages(data):
                self.asset_name = asset_name
                if self.config.kelvin.app.offset_timestamps:
                    messages = [*messages]
                    last_timestamp = messages[-1]._.time_of_validity / 1e9
                    if last_timestamp > self.state.last_process_time:
                        self.state.last_process_time = last_timestamp
                for message in messages:
                    try:
                        self.push_buffer(message)
                    except Exception:  # pragma: no cover
                        self.logger.exception(
                            "Failed to process message",
                            message_name=message._.name,
                            message_type=message._.type,
                        )

        self._process(last_process_time)

    def on_data_timeout(self, timeout: float) -> None:
        """
        The callback that is triggered when the application has not received
        within the configured timeout period.

        Parameters
        ----------

        timeout : :obj:`float`
            The time when the timeout was triggered.

        """

        last_process_time = self.process_time

        self.logger.debug("on_data_timeout")

        self._process(last_process_time)


class PollerApplication(BaseApplication, _PollerApplication):
    """
    Poller Application.

    Parameters
    ----------
    context : :obj:`ContextInterface`
        Application context containing the methods bound to the application implementation (C++)
    name : :obj:`str`, optional
        Optional application name
    configuration : :obj:`dict`, optional
        Optional initial configuration
    data : :obj:`list`, optional
        Optional initial data

    """

    config: DefaultConfig

    def on_poll(self) -> None:
        """Triggered when there is data available for the application to
        process."""

        last_process_time = self.state.last_process_time = self.process_time

        self.logger.debug("on_poll")

        self._process(last_process_time)
