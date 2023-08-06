"""Kelvin SDK Application SDK."""

# legacy location
from ..sdk.app import ApplicationConfig, DataApplication, PollerApplication

__all__ = [
    "Application",
    "ApplicationConfig",
    "DataApplication",
    "PollerApplication",
]

Application = DataApplication
