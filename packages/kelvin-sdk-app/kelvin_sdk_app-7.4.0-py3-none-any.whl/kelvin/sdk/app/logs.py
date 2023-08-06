"""Logging formatter."""

from __future__ import annotations

import json
import logging
import logging.config
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Union

import structlog

# defaults for some noisy loggers
DEFAULTS = {
    "boto3": logging.WARNING,
    "botocore": logging.WARNING,
    "matplotlib": logging.WARNING,
    "s3transfer": logging.WARNING,
    "oauth2client": logging.WARNING,
    "urllib3": logging.WARNING,
}

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATETIME_MICRO_FORMAT = DATETIME_FORMAT.replace("Z", ".%fZ")

logging.addLevelName(logging.DEBUG, "TRACE")


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder."""

    def default(self, x: Any) -> Any:
        """Return a JSON-serialisable object."""

        if isinstance(x, datetime):
            x = x.astimezone(timezone.utc)
            return x.strftime(DATETIME_MICRO_FORMAT if x.microsecond else DATETIME_FORMAT)

        if isinstance(x, date):
            return x.isoformat()

        if isinstance(x, Mapping):
            return {**x}

        if isinstance(x, Set):
            try:
                return sorted(x)
            except TypeError:
                return sorted(str(v) for v in x)

        if isinstance(x, Iterable):
            return [*x]

        if isinstance(x, Enum):
            return x.name

        return str(x)


def configure_logs(
    loggers: Optional[Union[Mapping[str, int], Sequence[str]]] = None,
    default_level: Union[int, str] = logging.DEBUG,
    json: bool = False,
    reset_root: bool = True,
    defaults: Optional[Mapping[str, int]] = None,
    colors: bool = False,
) -> Dict[str, Any]:
    """Configure logging and structlog."""

    if reset_root:
        # reset root-logger
        root = logging.getLogger()
        root.handlers[:] = []

    if isinstance(default_level, str):
        default_level = int(logging._nameToLevel.get(default_level.upper(), logging.INFO))

    if loggers is None:
        loggers = {"": default_level}
    elif isinstance(loggers, Mapping):
        loggers = {name: x if x is not None else default_level for name, x in loggers.items()}
    else:
        loggers = {name: default_level for name in loggers}

    if defaults is None:
        defaults = {**DEFAULTS}

    processors: List[Any] = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%S.%fZ", utc=True),
    ]

    if json:
        processor = structlog.processors.JSONRenderer(cls=JSONEncoder, default=None)  # type: ignore
    else:
        processor = structlog.dev.ConsoleRenderer(colors=colors)  # type: ignore

    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": processor,
                "foreign_pre_chain": processors,
            }
        },
        "handlers": {"handler": {"class": "logging.StreamHandler", "formatter": "formatter"}},
        "loggers": {
            name: {"level": level, "handlers": ["handler"], "propagate": False}
            for name, level in {**defaults, **loggers}.items()
        },
    }

    structlog_processors: List[Any] = [
        *processors,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]  # type: ignore

    logging.config.dictConfig(config)
    structlog.configure(
        processors=structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return {name: structlog.get_logger(name) for name in loggers}
