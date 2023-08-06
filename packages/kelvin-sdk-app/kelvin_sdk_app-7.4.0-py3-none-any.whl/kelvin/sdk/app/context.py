"""Context."""

from __future__ import annotations

import json
from bisect import bisect
from collections import defaultdict
from time import time
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Tuple

from kelvin.sdk.datatype import Message

from ...core.context import ContextInterface
from .data import DataBuffer
from .utils import default

if TYPE_CHECKING:
    from .application import BaseApplication
else:
    BaseApplication = Any


class Context(ContextInterface):
    """Fake context."""

    def __init__(
        self,
        app: Optional[BaseApplication] = None,
        epoch: float = 0.0,
        input_registry_map: Optional[Mapping[str, Dict[str, Any]]] = None,
        output_registry_map: Optional[Mapping[str, Dict[str, Any]]] = None,
        configuration_registry_map: Optional[Mapping[str, Dict[str, Any]]] = None,
        parameter_registry_map: Optional[Mapping[str, Dict[str, Any]]] = None,
        history: Optional[Mapping[str, Sequence[Message]]] = None,
    ) -> None:
        """Initialise context."""

        self._app = app
        self._outputs: List[Message] = []
        self._epoch = epoch
        self._process_time = epoch
        self._input_registry_map: Mapping[str, Mapping[str, Any]] = (
            input_registry_map if input_registry_map is not None else {}
        )
        self._output_registry_map: Mapping[str, Mapping[str, Any]] = (
            output_registry_map if output_registry_map is not None else {}
        )
        self._configuration_registry_map: Mapping[str, Mapping[str, Any]] = (
            configuration_registry_map if configuration_registry_map is not None else {}
        )
        self._parameter_registry_map: Mapping[str, Mapping[str, Any]] = (
            parameter_registry_map if parameter_registry_map is not None else {}
        )
        self._history: Dict[str, DataBuffer] = defaultdict(DataBuffer)
        if history is not None:
            for name, data in history.items():
                self._history[name] += data  # type: ignore

    def get_process_time(self) -> float:
        return self._process_time

    def get_real_time(self) -> float:
        return time() - self._epoch  # pragma: no cover

    def emit(self, output: Message) -> None:
        self._outputs += [output]
        self._history[output._.name] += [output]  # type: ignore

    def select(
        self, metric_name: str, window: Tuple[float, float] = (0.0, 0.0), limit: int = 1000
    ) -> List[Message]:
        """Get a list of metrics from the application storage."""

        data = self._history[metric_name]

        start, end = window

        reverse = start > end
        if reverse:
            start, end = end, start

        timestamps = data.timestamps
        left, right = bisect(timestamps, int(start * 1e9)), bisect(timestamps, int(end * 1e9))

        result = data[left:right]
        if reverse:
            result = result[::-1]

        return result[:limit]

    def get_input_registry_map(self) -> str:
        """Get a dict with the registry map of the inputs."""

        return json.dumps({k: {**v} for k, v in self._input_registry_map.items()}, default=default)

    def get_output_registry_map(self) -> str:
        """Get a dict with the registry map of the outputs."""

        return json.dumps({k: {**v} for k, v in self._output_registry_map.items()}, default=default)

    def get_configuration_registry_map(self) -> str:
        """Get a dict with the registry map of the configuration."""

        return json.dumps(
            {k: {**v} for k, v in self._configuration_registry_map.items()}, default=default
        )

    def get_parameter_registry_map(self) -> str:
        """Get a dict with the registry map of the parameters."""

        return json.dumps(
            {k: {**v} for k, v in self._parameter_registry_map.items()}, default=default
        )

    # custom methods
    def set_process_time(self, process_time: float) -> None:
        """Set process time (for testing only)."""

        self._process_time = process_time
        if self._app is not None:
            self._app._process(process_time)

    def get_outputs(self, clear: bool = True) -> List[Message]:
        """Get outputs."""

        outputs = self._outputs[:]
        if clear:
            self._outputs[:] = []

        return outputs
