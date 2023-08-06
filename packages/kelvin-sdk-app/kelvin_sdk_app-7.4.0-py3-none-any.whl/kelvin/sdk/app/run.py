"""Run Applications."""

import json
import sys
from enum import Enum
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from time import time
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union, cast

import structlog

from kelvin.sdk.datatype import Message
from kelvin.sdk.datatype.model import timestamper
from kelvin.sdk.datatype.utils import snake_name
from kelvin.sdk.pubsub import PubSubClient, SyncConnection

from ...core.application import ApplicationInterface, DataApplication, PollerApplication
from ...core.context import ContextInterface
from .application import BaseApplication
from .logs import configure_logs
from .mapping_proxy import MappingProxy
from .types import LogLevel
from .utils import build_messages, default, get_io, inflate, inflate_message

logger = structlog.get_logger(__name__)
SYS_PATH = sys.path


class InterfaceType(str, Enum):
    """Application interface type."""

    DATA = "data"
    POLLER = "poller"

    def __str__(self) -> str:
        """Representation of value as string."""

        return str(self.value)  # pragma: no cover


class CoreClientContext(ContextInterface):
    """Core Client context."""

    def __init__(
        self,
        connection: SyncConnection,
        startup_time: float = 0.0,
        buffer: Optional[Sequence[Message]] = None,
    ) -> None:
        """Initialise Core Client Context."""

        core_config = MappingProxy(connection.config.app_config or {}).get("app.kelvin", {})

        self._connection = connection
        self.process_time = startup_time
        self.buffer: List[Message] = [*buffer] if buffer is not None else []
        self._outputs: List[Message] = []

        self._input_registry_map = {
            item["name"]: {
                "name": item["name"],
                "data_type": item["data_type"],
                "control_change": item.get("control_change", False),
                "selectors": item.get("sources", []),
            }
            for item in core_config.get("inputs", [])
        }
        self._output_registry_map = {
            item["name"]: {
                "name": item["name"],
                "data_type": item["data_type"],
                "control_change": item.get("control_change", False),
                "selectors": item.get("targets", []),
            }
            for item in core_config.get("outputs", [])
        }
        self._configuration_registry_map = (
            {
                item["name"]: {
                    "name": item["name"],
                    "data_type": item["data_type"],
                    "selectors": [],
                }
                for item in core_config.get("configuration", [])
            }
            if not isinstance(core_config.get("configuration"), Mapping)
            else {}
        )
        self._parameter_registry_map = {
            item["name"]: {
                "name": item["name"],
                "data_type": item["data_type"],
                "selectors": item.get("sources", []),
            }
            for item in core_config.get("parameters", [])
        }

    def get_process_time(self) -> float:
        """
        Returns the current time of the application.

        This time should be used by applications for timestamping of
        messages. This time will be the real wall time by default and
        the replay time when running in simulation mode.

        """

        return self.process_time

    def get_real_time(self) -> float:
        """
        Returns the actual time of the system clock.

        This time should be used by applications when the actual wall
        time is required.  This is typically used when timestamping
        sensor measures and computing latencies.

        """

        return time()

    def emit(self, output: Message) -> None:
        """Takes the incoming data and publishes the contents to the software
        bus."""

        self._outputs += [output]

    def get_outputs(self, clear: bool = True) -> List[Message]:
        """Get outputs."""

        outputs = self._outputs[:]
        if clear:
            self._outputs[:] = []

        return outputs

    def select(
        self,
        metric_name: str,
        window: Tuple[float, float] = (0.0, 0.0),
        limit: int = 1000,
    ) -> List[Message]:
        """Get a list of metrics from the application storage."""

        raise NotImplementedError

    def get_input_registry_map(self) -> str:
        """Get a dict with the registry map of the inputs."""

        return json.dumps(self._input_registry_map, default=default)

    def get_output_registry_map(self) -> str:
        """Get a dict with the registry map of the outputs."""

        return json.dumps(self._output_registry_map, default=default)

    def get_configuration_registry_map(self) -> str:
        """Get a dict with the registry map of the configuration."""

        return json.dumps(self._configuration_registry_map, default=default)

    def get_parameter_registry_map(self) -> str:
        """Get a dict with the registry map of the parameters."""

        return json.dumps(self._parameter_registry_map, default=default)

    # unsupported methods
    def create_timer(self, *args: Any, **kwargs: Any) -> str:
        raise NotImplementedError

    def delete_timer(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def get_timers(self) -> List[str]:
        raise NotImplementedError


def load_entry_point(entry_point: str, default_class_name: str = "App") -> Type:
    """Load class."""

    if ":" in entry_point:
        module_name, class_name = entry_point.rsplit(":", 1)
    else:
        module_name, class_name = entry_point, default_class_name

    try:
        sys.path = ["", *SYS_PATH]
        try:
            module = import_module(module_name)
        finally:
            sys.path = SYS_PATH
    except (ModuleNotFoundError, TypeError):
        path = Path(module_name).expanduser().resolve()

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
                raise ValueError(f"Unable to load module {module_name!r}")
            module = sys.modules[name] = module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
        else:
            raise ValueError(f"Module {module_name!r} not found")

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ValueError(f"Application class {class_name!r} not found in {module_name!r} module")


def run_app(
    entry_point: str,
    interface_type: Optional[InterfaceType] = None,
    broker_url: Optional[str] = None,
    configuration: Optional[Union[str, Path, Mapping[str, Any]]] = None,
    max_steps: Optional[int] = None,
    log_level: Optional[LogLevel] = None,
    startup_time: Optional[float] = None,
    **kwargs: Any,
) -> Any:
    """Run Kelvin SDK App."""

    app_class = load_entry_point(entry_point)

    if not isinstance(app_class, type):
        raise TypeError(f"Application class {app_class!r} is not a class")

    if not issubclass(app_class, ApplicationInterface):
        raise TypeError(
            "Application class {app_class.__name__!r} does not derive from 'kelvin.core.ApplicationInterface'"
        )

    if interface_type is not None:
        if interface_type not in {InterfaceType.DATA, InterfaceType.POLLER}:  # pragma: no cover
            raise ValueError(f"Unknown interface type: {interface_type}")
    elif issubclass(app_class, DataApplication):
        interface_type = InterfaceType.DATA
    elif issubclass(app_class, PollerApplication):
        interface_type = InterfaceType.POLLER
    else:
        raise ValueError(f"Unsupported interface type: {interface_type}")  # pragma: no cover

    kwargs = {"broker_url": broker_url, "app_config": configuration, **kwargs}
    client = PubSubClient(config={k: v for k, v in kwargs.items() if v is not None})

    main_config = MappingProxy(client.config.app_config or {})
    core_config = main_config.get("app.kelvin", {})
    inputs, outputs, config, params = get_io(core_config)

    expanded = all(isinstance(v, Mapping) and "values" in v for v in config.values())

    if log_level is None:
        log_level = LogLevel[core_config.get("logging_level", "INFO").upper()]
        configure_logs(default_level=log_level)

    if not core_config:
        logger.warning("No core-configuration provided. All inputs/outputs are unfiltered.")

    if expanded:
        kelvin_app_config = inflate(
            (item["name"], item["value"]) for item in config.pop("kelvin.app", {}).get("values", [])
        )
    else:
        kelvin_app_config = config.get("kelvin", {}).pop("app", {})

    environment_config = main_config.get("environment", {})
    info_config = main_config.get("info", {})
    kelvin_info = {
        "name": info_config.get("name"),
        "title": info_config.get("title"),
        "description": info_config.get("description"),
        "version": info_config.get("version"),
        "node_name": environment_config.get("node_name"),
        "workload_name": environment_config.get("workload_name"),
    }

    if startup_time is None:
        startup_time = time()

    with timestamper(lambda: 0):
        init_configuration = cast(Dict[str, Any], build_messages(config) if expanded else config)
        init_configuration.setdefault("kelvin", {}).update(
            {"app": kelvin_app_config, "info": kelvin_info}
        )
        init_inputs = [inflate_message(x) for x in core_config.get("inputs", []) if x.get("values")]
        init_parameters = [
            inflate_message(x) for x in core_config.get("parameters", []) if x.get("values")
        ]

    with client.connection(sync=True) as connection:
        context = CoreClientContext(connection, startup_time=startup_time, buffer=init_inputs)

        with timestamper(lambda: int(context.process_time * 1e9)):
            app = app_class(context=context)
            app.on_initialize(
                configuration=init_configuration,
                app_configuration=main_config,
                parameters=init_parameters,
            )

            delay = app.config.kelvin.app.delay if isinstance(app, BaseApplication) else 1.0

            trash: List[int]

            step = 0

            while True:
                step += 1
                if max_steps is not None and step > max_steps:
                    logger.info(f"Maximum number of steps reached ({max_steps})")
                    break

                messages: List[Message] = []
                parameters: List[Message] = []

                # pick up deferred messages
                if context.buffer:
                    messages += context.buffer
                    context.buffer[:] = []

                now = time()
                timeout = delay

                try:
                    while True:
                        result = connection.receive(timeout=timeout)
                        then = time()

                        if result is not None:
                            # update time from request
                            context.process_time = max(
                                result._.time_of_validity / 1e9,
                                context.process_time,
                            )
                            messages += [result]
                        else:
                            context.process_time = then

                        # gather messages until timeout met
                        timeout = max(delay - (then - now), 0.0)

                        if not timeout:
                            break

                    if core_config:
                        trash = []
                        for index, message in enumerate(messages):
                            name = message._.name

                            if name in inputs:
                                continue

                            if name in params:
                                trash += [index]
                                parameters += [message]
                                continue

                            if name in config:
                                trash += [index]
                                logger.warning(
                                    "Configuration can only be changed at initialisation",
                                    message_name=name,
                                )
                                continue

                            trash += [index]
                            logger.warning(
                                "Dropping unknown inbound message",
                                message_name=name,
                                message_type=message._.type,
                            )

                        # take out the trash
                        for offset, index in enumerate(trash):
                            del messages[index - offset]

                        if parameters:
                            app.on_parameter_change(parameters)

                    if interface_type == InterfaceType.DATA:
                        cast(DataApplication, app).on_data(messages)
                    elif interface_type == InterfaceType.POLLER:
                        cast(PollerApplication, app).on_poll()
                    else:  # pragma: no cover
                        raise ValueError(f"Unknown interface type: {interface_type}")

                    # get emitted messages
                    results = context.get_outputs()

                    if core_config:
                        trash = []
                        for index, message in enumerate(results):
                            name = message._.name
                            if name in outputs:
                                continue

                            trash += [index]
                            logger.warning(
                                "Dropping unknown outbound message",
                                message_name=name,
                                message_type=message._.type,
                            )

                        # take out the trash
                        for offset, index in enumerate(trash):
                            del results[index - offset]

                    connection.send(results)

                except KeyboardInterrupt:  # pragma: no cover
                    break
                except Exception:  # pragma: no cover
                    logger.exception("Unable to process application")

    # terminate the app
    logger.info("Terminating app")
    try:
        app.on_terminate()
    except Exception:  # pragma: no cover
        logger.exception("Error while terminating")

    logger.info("Finished.")

    return app
