"""Poller Application base-class."""

from abc import abstractmethod

from .application import ApplicationInterface


class PollerApplication(ApplicationInterface):
    """Poller application."""

    @abstractmethod
    def on_poll(self) -> None:
        """The callback that is triggered when there is data available for the
        model to process."""
