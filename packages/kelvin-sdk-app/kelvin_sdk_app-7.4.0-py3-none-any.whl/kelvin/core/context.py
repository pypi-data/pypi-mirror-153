"""Core context base-class."""

from abc import ABC, abstractmethod
from typing import List, Tuple

from kelvin.sdk.datatype import Message


class ContextInterface(ABC):
    """Context abstract base-class."""

    @abstractmethod
    def get_process_time(self) -> float:
        """
        Returns the current time of the application.

        This time should be used by applications for timestamping of
        messages.  This time will be the real wall time by default and
        the replay time when running in simulation mode.

        """

    @abstractmethod
    def get_real_time(self) -> float:
        """
        Returns the actual time of the system clock.

        This time should be used by applications when the actual wall
        time is required.  This is typically used when timestamping
        sensor measures and computing latencies.

        """

    @abstractmethod
    def emit(self, output: Message) -> None:
        """
        Takes the incoming data and publishes the contents to the software bus.

        The emit can handle native data model objects and the python
        dictionary types.  Dictionary types get converted into data
        model objects before being published.

        """

    @abstractmethod
    def select(
        self, metric_name: str, window: Tuple[float, float] = (0.0, 0.0), limit: int = 1000
    ) -> List[Message]:
        """
        Get a list of metrics from the application storage.

        Accesses the application storage and returns a list of metrics
        for the specified metric name. The returned metrics will be
        filtered using the start and end dates specified and the number
        of desired results will be limited by the amount of the
        specified limit.

        """

    @abstractmethod
    def get_input_registry_map(self) -> str:
        """Get a dict with the registry map of the outputs."""

    @abstractmethod
    def get_output_registry_map(self) -> str:
        """Get a dict with the registry map of the outputs."""

    @abstractmethod
    def get_configuration_registry_map(self) -> str:
        """Get a dict with the registry map of the configuration."""

    @abstractmethod
    def get_parameter_registry_map(self) -> str:
        """Get a dict with the registry map of the parameters."""
