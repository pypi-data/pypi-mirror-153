"""Bridge Toolkit."""

from __future__ import annotations

import asyncio
import re
import sys
from asyncio import CancelledError, Queue, Task
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from random import random
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import structlog
from pydantic import Extra, Field, StrictStr
from pydantic.generics import GenericModel
from typing_inspect import get_args, get_generic_bases

from kelvin.sdk.datatype import Message, Model
from kelvin.sdk.datatype.utils import snake_name
from kelvin.sdk.pubsub import PubSubClient
from kelvin.sdk.pubsub.types import Access, DottedName, Storage

from .types import LogLevel, TypedModel
from .utils import deep_get

if sys.version_info >= (3, 8):
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore

logger = structlog.get_logger(__name__)

SYS_PATH = sys.path

T = TypeVar("T", bound="Bridge")


class BridgeError(Exception):
    """General bridge error."""


class AuthenticationType(Model):
    """Authentication type."""


class CredentialsType(AuthenticationType):
    """Credentials type."""

    username: str
    password: str


class Authentication(TypedModel[AuthenticationType]):
    """Authentication."""

    type: Literal["credentials"]
    credentials: Optional[CredentialsType] = None


class LanguageType(Model):
    """Language type."""


class EntryPoint(StrictStr):
    """Entry-point."""

    regex = re.compile(r"^([^:]+):(\w+)$")


class PythonLanguageType(LanguageType):
    """Python language-type."""

    entry_point: EntryPoint = Field(
        ...,
        title="Entry Point",
        description="Entry point.",
    )
    requirements: Optional[str] = Field(
        "requirements.txt",
        title="Requirements",
        description="Package requirements",
    )
    version: Optional[Literal["3.7", "3.8", "3.9"]] = Field(
        None,
        title="Python Version",
        description="Python version.",
    )


class Language(TypedModel[LanguageType]):
    """Language."""

    type: Literal["python"] = Field(
        "python",
        title="Language Type",
        description="Language type.",
    )
    python: Optional[PythonLanguageType] = None


class Images(Model):
    """Images."""

    runner: Optional[str] = Field(
        None,
        title="Runner Image",
        description="Runner image.",
    )
    builder: Optional[str] = Field(
        None,
        title="Builder Image",
        description="Builder image.",
    )


class MQTT(Model):
    """Broker configuration."""

    ip: str
    port: int
    authentication: Optional[Authentication]


class BridgeConfiguration(Model):
    """Bridge Configuration."""


class MetricConfiguration(Model):
    """Metric Configuration."""


B = TypeVar("B", bound=BridgeConfiguration)
M = TypeVar("M", bound=MetricConfiguration)


class MetricMap(GenericModel, Model, Generic[M]):
    """Metric Map."""

    class Config:
        """Pydantic configuration."""

        validate_all = True

    name: str = Field(
        ...,
        title="Name",
        description="Name.",
    )
    data_type: DottedName = Field(
        ...,
        title="Data Type",
        description="Data type.",
    )
    access: Access = Field(
        ...,
        title="Access",
        description="Access level.",
    )
    storage: Storage = Field(
        Storage.NODE_CLOUD,
        title="Storage",
        description="Storage type.",
    )
    asset_name: Optional[DottedName] = Field(
        ...,
        title="Asset Name",
        description="Asset name.",
    )
    configuration: M = Field(
        {},
        title="Configuration",
        description="Additional configuration.",
    )

    __iter__: Callable[[], Iterator[str]]  # type: ignore


class Version(StrictStr):
    """Version."""

    regex = re.compile(
        f"^([0-9]+)\\.([0-9]+)\\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?(?:\\+[0-9A-Za-z-]+)?$"
    )


class DataType(Model):
    """Data Type."""

    name: DottedName = Field(
        ...,
        title="Data Type Name",
        description="Data-type name.",
    )
    version: Version = Field(
        ...,
        title="Data Type Version",
        description="Data Type version.",
    )
    path: Optional[str] = Field(
        None,
        title="Data Type Path",
        description="Data Type path.",
    )


class Configuration(GenericModel, Model, Generic[B, M]):
    """Configuration."""

    class Config:
        """Pydantic configuration."""

        validate_all = True

    protocol: Optional[str] = Field(
        None,
        title="Protocol",
        description="Protocol name.",
    )
    images: Optional[Images] = Field(
        None,
        title="Kelvin Application Images",
        description="Image configuration for building a Kelvin application.",
    )
    system_packages: Optional[List[str]] = Field(
        None,
        title="System Packages",
        description="Packages to install into image.",
    )
    data_types: Optional[List[DataType]] = Field(
        None,
        title="Data Types",
        description="Data Types that the Kelvin application can use as input/output messages.",
    )
    language: Optional[Language] = Field(
        None,
        title="Language Type",
        description="Language type.",
    )
    mqtt: Optional[MQTT] = Field(
        None,
        title="MQTT",
        description="MQTT configurations",
    )
    configuration: B = Field(
        {},
        title="Configuration",
        description="Configuration.",
    )
    logging_level: Optional[LogLevel] = Field(
        LogLevel.INFO,
        title="Logging Level",
        description="Logging level.",
    )
    metrics_map: List[MetricMap[M]] = Field(
        default_factory=list,
        title="Metrics Map",
        description="Metrics map.",
    )

    __iter__: Callable[[], Iterator[str]]  # type: ignore


class DefaultBridgeConfiguration(BridgeConfiguration):
    """Default bridge configuration."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.allow


class DefaultMetricConfiguration(MetricConfiguration):
    """Default metric configuration."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.allow


C = TypeVar("C", bound=Configuration)
S = TypeVar("S", bound="Bridge", covariant=True)


class BridgeMeta(type):
    """Bridge metaclass."""

    _config_cls: Type[Configuration]

    def __new__(
        metacls: Type[BridgeMeta],
        name: str,
        bases: Tuple[Type, ...],
        __dict__: Dict[str, Any],
    ) -> BridgeMeta:
        """Create Bridge class."""

        if __dict__["__module__"] != __name__ and not {*__dict__} & {"reader", "writer"}:
            raise TypeError("No reader or writer specified for bridge class {name!r}")

        cls = super().__new__(metacls, name, bases, __dict__)

        config_cls = get_args(get_generic_bases(cls)[0])[0]

        if config_cls is C:
            config_cls = Configuration[DefaultBridgeConfiguration, DefaultMetricConfiguration]
        elif not issubclass(config_cls, Configuration):
            raise TypeError(f"Invalid configuration class {config_cls.__name__!r}")

        cls._config_cls = config_cls

        return cls


class Bridge(Generic[C], metaclass=BridgeMeta):
    """Bridge."""

    config: C
    _config_cls: Type[C]

    _pubsub_client: PubSubClient
    _inbound_messages: Queue[Message]
    _outbound_messages: Queue[Message]

    def __init__(
        self,
        app_config: Optional[Union[Path, str, Mapping[str, Any]]] = None,
    ) -> None:
        """Initialise bridge."""

        self._pubsub_client = PubSubClient(app_config=app_config)
        self._inbound_messages = Queue()
        self._outbound_messages = Queue()

        self.config = self._config_cls.parse_obj(
            deep_get(self._pubsub_client.config.app_config or {}, "app.bridge", {})
        )

    async def init(self) -> None:
        """Initialise bridge resources prior to running."""

    async def stop(self) -> None:
        """Stop bridge."""

    async def reader(self, messages: Queue[Message]) -> None:
        """Process inbound messages."""

    async def writer(self, messages: Queue[Message]) -> None:
        """Process outbound messages."""

    async def _client_task(self) -> None:
        """Client task."""

        interval, min_interval, max_interval = 0.0, 1.0, 32.0

        client = self._pubsub_client

        while True:
            tasks: List[Task] = []
            try:
                async with client.connection(sync=False) as connection:
                    interval = 0.0

                    if client.config.output_topics and self.reader is not Bridge.reader:

                        async def _reader() -> None:
                            while True:
                                message = await self._inbound_messages.get()
                                try:
                                    connection.send(message)
                                except CancelledError:
                                    break
                                except Exception:
                                    logger.exception("Failed to publish message", message=message)

                        tasks += [asyncio.create_task(_reader())]

                    if client.config.input_topics and self.writer is not Bridge.writer:

                        async def _writer() -> None:
                            async for message in connection.stream():
                                await self._outbound_messages.put(message)

                        tasks += [asyncio.create_task(_writer())]

                    await asyncio.gather(*tasks)

            except CancelledError:
                break
            except Exception as e:
                logger.error(f"Pub-sub error: {e}")
                logger.info(f"Retrying pub-sub in {interval} seconds")
                await asyncio.sleep(interval + random())  # nosec
                interval = min(max(2.0 * interval, min_interval), max_interval)
            finally:
                for task in tasks:
                    task.cancel()
                pending = {*tasks}
                while pending:
                    _, pending = await asyncio.wait(pending)

    async def _run(self) -> None:
        """Run bridge."""

        interval, min_interval, max_interval = 0.0, 1.0, 32.0

        while True:
            try:
                await self.init()
            except BridgeError as e:
                logger.error(f"Unable to initialise bridge: {e}")
                logger.info(f"Retrying initialisation in {interval} seconds")
                await asyncio.sleep(interval + random())  # nosec
                interval = min(max(2.0 * interval, min_interval), max_interval)
                continue
            except Exception:
                logger.exception("Unexpected error")
                raise SystemExit()

            interval = 0.0

            tasks: List[Task] = []
            try:
                if self.reader is not Bridge.reader:
                    tasks += [asyncio.create_task(self.reader(self._inbound_messages))]
                if self.writer is not Bridge.writer:
                    tasks += [asyncio.create_task(self.writer(self._outbound_messages))]

                await asyncio.gather(*tasks)

            except CancelledError:
                break
            except BridgeError as e:
                logger.error(f"Bridge error: {e}")
            except Exception:
                logger.exception("Unexpected error")
            finally:
                try:
                    await self.stop()
                except Exception:
                    logger.exception("Error while stopping bridge")
                for task in tasks:
                    task.cancel()
                pending = {*tasks}
                while pending:
                    _, pending = await asyncio.wait(pending)

    def run(self) -> None:
        """Run bridge."""

        loop = asyncio.get_event_loop()

        client_task = loop.create_task(self._client_task())
        task = loop.create_task(self._run())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            client_task.cancel()
            task.cancel()
            try:
                loop.run_until_complete(asyncio.gather(client_task, task))
            except BaseException:
                pass
        finally:
            logger.info("Finished")

    @classmethod
    def from_entry_point(
        cls,
        entry_point: str,
        app_config: Optional[Union[Path, str, Mapping[str, Any]]] = None,
        **kwargs: Any,
    ) -> Bridge:
        """Load bridge from class name."""

        module_name, class_name = entry_point.rsplit(":", 1)

        if isinstance(app_config, Path):
            app_config = app_config.expanduser().resolve()

        try:
            sys.path = ["", *SYS_PATH]

            if isinstance(app_config, Path):
                sys.path.insert(0, str(app_config.parent))

            try:
                module = import_module(module_name)
            finally:
                sys.path = SYS_PATH
        except ModuleNotFoundError:
            path = Path(module_name).expanduser()
            if isinstance(app_config, Path) and not path.exists() and not path.is_absolute():
                path = app_config.parent / path
            else:
                path = path.resolve()

            if path.exists():
                if path.is_dir():
                    filename = path / "__init__.py"
                    if filename.exists():
                        path = filename
            elif not path.suffix:
                filename = path.with_suffix(".py")
                if filename.exists():
                    path = filename

            if path.exists():
                name = path.parent.stem if path.name == "__init__.py" else path.stem
                spec = spec_from_file_location(snake_name(name), path)
                if spec is None:
                    raise BridgeError(f"Unable to load module {module_name!r}")
                module = sys.modules[name] = module_from_spec(spec)
                spec.loader.exec_module(module)  # type: ignore
            else:
                raise BridgeError(f"Module {module_name!r} not found")

        try:
            result = getattr(module, class_name)
        except AttributeError:
            raise BridgeError(f"Bridge class {class_name!r} not found in {module_name!r} module")

        if not isinstance(result, type) or not issubclass(result, Bridge):
            raise BridgeError(f"{entry_point!r} is not a bridge class")

        return result(app_config=app_config, **kwargs)  # type: ignore
