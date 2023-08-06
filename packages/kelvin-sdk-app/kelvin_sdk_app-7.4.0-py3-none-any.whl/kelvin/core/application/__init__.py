# isort: skip_file
"""Classic core application."""

__all__ = ["ApplicationInterface", "DataApplication", "PollerApplication"]

from .application import ApplicationInterface
from .data import DataApplication
from .poller import PollerApplication

# legacy name
DataModelApplication = DataApplication
