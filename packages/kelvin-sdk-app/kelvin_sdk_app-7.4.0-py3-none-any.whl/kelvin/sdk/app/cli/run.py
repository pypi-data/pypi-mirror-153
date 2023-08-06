"""Run Applications."""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import indent
from typing import Optional

import click
import structlog
import yaml
from click.exceptions import Exit

from ..bridge import Bridge, BridgeError, Language
from ..logs import configure_logs
from ..run import InterfaceType, run_app
from ..types import LogLevel
from ..utils import deep_get
from .main import main

logger = structlog.get_logger(__name__)


@main.group()
def run() -> None:
    """Run Applications and Servers."""


@run.command()
@click.option(
    "--interface-type",
    "-i",
    type=click.Choice([*InterfaceType]),
    required=False,
    help="Interface type",
)
@click.option("--broker-url", "-b", type=click.STRING, required=False, help="Broker URL")
@click.option("--configuration", "-c", type=click.STRING, required=False, help="App configuration")
@click.option(
    "--log-level",
    "-l",
    type=click.Choice([x.name for x in LogLevel]),
    default=None,
    callback=lambda _, __, x: LogLevel[x] if x is not None else None,
    help="Logging level",
)
@click.option("--max-steps", "-m", type=click.INT, required=False, help="Maximum number of steps")
@click.argument("entry_point", nargs=1, type=click.STRING)
def app(
    interface_type: Optional[InterfaceType],
    broker_url: Optional[str],
    configuration: Optional[str],
    log_level: Optional[LogLevel],
    max_steps: Optional[int],
    entry_point: str,
) -> None:
    """Run Kelvin SDK Applications."""

    if log_level is not None:
        configure_logs(default_level=log_level)

    try:
        run_app(entry_point, interface_type, broker_url, configuration, max_steps, log_level)
    except Exception as e:  # pragma: no cover
        logger.exception("Failed")
        click.echo(f"Unable to run app: {e}", err=True)
        raise Exit(1)


@run.command()
@click.option(
    "--configuration", "-c", type=click.STRING, required=True, help="Bridge configuration."
)
@click.option(
    "--log-level",
    "-l",
    type=click.Choice([x.name for x in LogLevel]),
    default=None,
    callback=lambda _, __, x: LogLevel[x] if x is not None else None,
    help="Logging level",
)
@click.argument("entry_point", nargs=1, required=False, type=click.STRING)
def bridge(
    configuration: str,
    log_level: Optional[LogLevel],
    entry_point: Optional[str],
) -> None:
    """Process files."""

    app_config = Path(configuration).expanduser().resolve()
    if not app_config.exists():
        click.echo(f"Configuration file {str(app_config)!r} does not exist", err=True)
        raise Exit(1)

    if entry_point is None:
        try:
            data = yaml.safe_load(app_config.read_bytes())
        except Exception:
            click.echo(f"Configuration file {str(app_config)!r} is invalid", err=True)
            raise Exit(1)

        try:
            language = Language.parse_obj(deep_get(data, "app.bridge.language", {}))
        except Exception as e:
            click.echo(f"Configuration file {str(app_config)!r}:\n{indent(str(e), '  ')}", err=True)
            raise Exit(1)

        if language.python is None:
            click.echo("Unable to determine entry-point from configuration", err=True)
            raise Exit(1)

        entry_point = language.python.entry_point

    try:
        bridge = Bridge.from_entry_point(entry_point, app_config=app_config)
    except BridgeError as e:
        click.echo(f"Failed to load bridge {entry_point!r}:\n{indent(str(e), '  ')}", err=True)
        raise Exit(1)
    except Exception:
        logger.exception("Failed to load bridge")
        raise Exit(1)

    if log_level is None:
        log_level = bridge.config.logging_level

    configure_logs(default_level=log_level, colors=sys.stdout.isatty())

    try:
        bridge.run()
    except Exception as e:
        click.echo(f"Failed to run bridge:\n{indent(str(e), '  ')}", err=True)
        logger.exception("Failed")
        raise Exit(1)
