"""Application interface."""

from __future__ import annotations

from pathlib import Path
from time import time
from typing import Any, Dict, List, Mapping, Optional, Sequence, Type, TypeVar, Union, cast

import yaml

from kelvin.sdk.datatype import Message
from kelvin.sdk.datatype.model import timestamper

from ...sdk.app.mapping_proxy import MappingProxy
from ...sdk.app.utils import build_messages, get_io, inflate, inflate_message
from ..context import ContextInterface

T = TypeVar("T", bound="ApplicationInterface")


class ApplicationInterface:
    """
    The Application Interface is the primary base class for all python
    applications and contains the methods that are publicly available to all
    application types.

    The application allows developers to create, delete, and use timers
    with arbitrary callback methods, emit/publish messages to the
    software bus, and access the current process time.

    """

    def __init__(self, context: ContextInterface) -> None:
        """Initialise application interface."""

        self._context = context

    def on_initialize(
        self,
        configuration: Mapping[str, Any],
        app_configuration: Mapping[str, Any],
        parameters: Optional[Union[Sequence[Message], Mapping[str, Message]]] = None,
    ) -> bool:
        """
        The on_initialize() method is called once at the initial creation of
        the class.

        The incoming configuration will typically include the default
        parameters and initial conditions necessary to initialize the
        particular application.

        Parameters
        ----------
        configuration : dict
            The configuration information for the application being executed.
        app_configuration : dict
            The complete application configuration for the application being executed.
        parameters : dict
            The optional parameters information for the application being executed.

        """

        return True  # pragma: no cover

    def on_parameter_change(
        self, parameter: Union[Sequence[Message], Mapping[str, Message]]
    ) -> bool:
        """
        The on_parameter_change() method is called every time the application's
        configuration is modified. This callback will be triggered once after
        initialize() and then once every time the configuration is modified.
        The incoming configuration will typically include the default
        parameters and initial conditions necessary to initialize the
        particular application.

        Parameters
        ----------
        parameter : dict
            The parameter information for the application being executed.

        """

        return True  # pragma: no cover

    def on_terminate(self) -> bool:
        """
        The on_terminate() method is called when the application is being
        terminated.

        This allows application to clean up resources that might have
        been allocated internally, cleanly close out logs, etc. to
        initialize the particular application.

        """

        return True  # pragma: no cover

    def get_process_time(self) -> float:
        """
        Returns the current time of the application.  This time should be used
        by applications for timestamping of messages.  This time will be the
        real wall time by default and the replay time when running in
        simulation mode.

        Returns
        -------
        float : The current process time in seconds.

        """

        return self._context.get_process_time()

    def get_real_time(self) -> float:
        """
        Returns the actual time of the system clock.  This time should be used
        by applications when the actual wall time is required.  This is
        typically used when timestamping sensor measures and computing
        latencies.

        Returns
        -------

        float : The current process time in seconds.

        """

        return self._context.get_real_time()

    def emit(self, data: Message) -> None:
        """
        Takes the incoming data and publishes the contents to the software bus.

        Parameters
        ----------

        data : :obj:`kelvin.sdk.datatype.Message`
            The data to be published on the software bus.

        """

        self._context.emit(data)

    def select(
        self, metric_name: str, start: float = 0.0, end: float = 0.0, limit: int = 1000
    ) -> List[Message]:
        """
        Get a list of metrics from the application storage.

        Accesses the application storage and returns a list of metrics for the specified metric name. The returned
        metrics will be filtered using the start and end dates specified and the number of desired results will be
        limited by the amount of the specified limit.

        Parameters
        ----------
        metric_name : str
            The name of the metric to be looked up in the application storage.
        start : :obj:`float`, optional
            Extract window start.
        end : :obj:`float`, optional
            Extract window end.
        limit : int, optional
            The maximum number of desired data points.

        Returns
        -------
        List: A list of metrics matching the specified filters.

        """

        return self._context.select(metric_name, (start, end), limit)

    def get_input_registry_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a dict with the registry map of the inputs.

        Returns
        -------
        Dict[str, Dict[str, Any]]: The registry map as a dict

        """

        return yaml.safe_load(self._context.get_input_registry_map())

    def get_output_registry_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a dict with the registry map of the outputs.

        Returns
        -------
        Dict[str, Dict[str, Any]]: The registry map as a dict

        """

        return yaml.safe_load(self._context.get_output_registry_map())

    def get_configuration_registry_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a dict with the registry map of the configuration.

        Returns
        -------
        Dict[str, Dict[str, Any]]: The registry map as a dict

        """

        return yaml.safe_load(self._context.get_configuration_registry_map())

    def get_parameter_registry_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a dict with the registry map of the parameters.

        Returns
        -------
        Dict[str, Dict[str, Any]]: The registry map as a dict

        """

        return yaml.safe_load(self._context.get_parameter_registry_map())

    @classmethod
    def core_init(
        cls: Type[T],
        configuration: Union[Path, str, Mapping[str, Any]] = "app.yaml",
        startup_time: Optional[float] = None,
        **kwargs: Any,
    ) -> T:
        """Initialise application from Core configuration for testing."""

        from ...sdk.app.context import Context
        from .data import DataApplication

        if isinstance(configuration, str):
            configuration = Path(configuration)

        if isinstance(configuration, Path):
            configuration = yaml.safe_load(configuration.expanduser().resolve().open("rt"))

        if not isinstance(configuration, Mapping):
            raise ValueError("Configuration must be a mapping")

        core_config = MappingProxy({**configuration}).get("app.kelvin", {})
        inputs, outputs, config, params = get_io(core_config)

        expanded = all(isinstance(v, Mapping) and "values" in v for v in config.values())

        if expanded:
            kelvin_app_config = inflate(
                (item["name"], item["value"])
                for item in config.pop("kelvin.app", {}).get("values", [])
            )
        else:
            kelvin_app_config = config.get("kelvin", {}).pop("app", {})

        environment_config = configuration.get("environment", {})
        info_config = configuration.get("info", {})
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

        with timestamper(lambda: int(cast(float, startup_time) * 1e9)):
            init_inputs = build_messages({k: v for k, v in inputs.items() if v.get("values")})
            init_configuration = cast(
                Dict[str, Any], build_messages(config) if expanded else config
            )
            init_configuration.setdefault("kelvin", {}).update(
                {"app": kelvin_app_config, "info": kelvin_info}
            )
            init_parameters = [inflate_message(x) for x in core_config.get("parameters", [])]

        input_registry_map = {
            name: {
                "name": name,
                "data_type": item["data_type"],
                "control_change": item.get("control_change", False),
                "selectors": item.get("sources", []),
            }
            for name, item in inputs.items()
        }
        output_registry_map = {
            name: {
                "name": name,
                "data_type": item["data_type"],
                "control_change": item.get("control_change", False),
                "selectors": item.get("targets", []),
            }
            for name, item in outputs.items()
        }
        configuration_registry_map = (
            {
                name: {
                    "name": name,
                    "data_type": item["data_type"],
                    "selectors": [],
                }
                for name, item in config.items()
            }
            if expanded
            else {}
        )
        parameter_registry_map = {
            name: {
                "name": name,
                "data_type": item["data_type"],
                "selectors": item.get("sources", []),
            }
            for name, item in params.items()
        }

        context = Context(
            epoch=startup_time,
            input_registry_map=input_registry_map,
            output_registry_map=output_registry_map,
            configuration_registry_map=configuration_registry_map,
            parameter_registry_map=parameter_registry_map,
        )

        app = cls(context=context, **kwargs)  # type: ignore
        app.on_initialize(init_configuration, configuration, init_parameters)
        if isinstance(app, DataApplication) and init_inputs:
            app.on_data([*init_inputs.values()])

        return app
