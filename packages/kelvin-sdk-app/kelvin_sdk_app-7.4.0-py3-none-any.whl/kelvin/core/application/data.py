"""Data Application base-class."""

from abc import abstractmethod
from typing import Sequence

from kelvin.sdk.datatype import Message

from .application import ApplicationInterface


class DataApplication(ApplicationInterface):
    """Data application."""

    @abstractmethod
    def on_data(self, data: Sequence[Message]) -> None:
        """
        The callback that is triggered when there is data available for the
        application to process. The incoming data will be a sequence of data
        model objects.

        Parameters
        ----------
        data : list
            The data being supplied to the executing application.
            The MessageInterface type can be set to a derived type like Float, PlungerLift, etc
            in you application by specifiying that type in the method declaration.

        """

    def on_data_timeout(self, timeout: float) -> None:
        """
        The callback that is triggered when the application has not received
        within the configured timeout period.

        Parameters
        ----------
        timeout : :obj:`float`
            The time when the timeout was triggered.

        """
