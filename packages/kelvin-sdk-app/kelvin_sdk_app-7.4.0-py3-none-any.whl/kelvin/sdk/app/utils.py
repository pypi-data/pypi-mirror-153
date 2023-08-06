"""Utility functions."""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timedelta, timezone
from functools import reduce, wraps
from importlib import import_module
from itertools import chain
from operator import itemgetter
from pathlib import Path
from typing import _GenericAlias  # type: ignore
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    get_type_hints,
    overload,
)
from warnings import warn

import yaml
from pydantic import BaseModel

from kelvin.sdk.client import Client
from kelvin.sdk.datatype import Message

if sys.version_info >= (3, 8):
    from importlib.metadata import Distribution, distributions
else:  # pragma: no cover
    from importlib_metadata import Distribution, distributions  # type: ignore

DurationType = Union[int, float, timedelta, Mapping[str, Union[float, int]]]
TimeType = Union[DurationType, datetime]

APP_CONFIG_PATH = Path("/opt/kelvin/app/app.yaml")
UPLOADER_KEY = "app.kelvin.uploader"

REPLACEMENTS = [
    (".", r"\."),
    ("*", r"([^.]+)"),
    (r"\.#", r"(\.[^.]+)*"),
    (r"#\.", r"([^.]+\.)*"),
    (r"#", r"([^.]+)(\.[^.]+)*"),
]


def topic_pattern(pattern: str) -> Pattern:
    """Create topic regular expression."""

    # just match the tail
    if pattern.isidentifier():
        pattern = f"#.{re.escape(pattern)}"

    pattern = reduce(lambda x, y: x.replace(*y), REPLACEMENTS, pattern)

    return re.compile(f"^{pattern}$")


def merge(
    x: MutableMapping[str, Any],
    *args: Optional[Mapping[str, Any]],
    ignore: Sequence[Tuple[str, ...]] = (),
) -> MutableMapping[str, Any]:
    """Merge dictionaries."""

    for arg in args:
        if arg is None:
            continue
        for k, v in arg.items():
            target = x.get(k, ...)
            if (
                target is ...
                or not (isinstance(target, Mapping) and isinstance(v, dict))
                or (k,) in ignore
            ):
                x[k] = v
            else:
                x[k] = merge({}, target, v, ignore=[x[1:] for x in ignore if x and x[0] == k])

    return x


def flatten(x: Mapping[str, Any]) -> Iterator[Tuple[str, Any]]:
    """Flatten nested mappings."""

    return (
        (k if not l else f"{k}.{l}", w)
        for k, v in x.items()
        for l, w in (flatten(v) if isinstance(v, Mapping) else [("", v)])
    )


def inflate(items: Iterable[Tuple[str, Any]], separator: str = ".") -> Dict[str, Any]:
    """Inflate flattened keys via separator into nested dictionary."""

    result: Dict[str, Any] = {}

    for key, value in sorted(items, key=itemgetter(0)):
        if separator not in key:
            head, tail = [], key
            root = result
        else:
            *head, tail = key.split(separator)
            root = reduce(lambda x, y: x.setdefault(y, {}), head, result)

        try:
            root[tail] = value
        except TypeError:
            raise ValueError(
                f"Unable to extend leaf value at {separator.join(head)!r} ({root!r}) to {key!r} ({value!r})"
            )

    return result


def gather(x: Dict[str, Any], key: str) -> Dict[str, Any]:
    """Gather keys from a nested structure."""

    values = x.pop(key, {})

    for v in [*values.values()]:
        values.update(gather(v, key))

    return values


def build_mapping(
    items: Union[Iterable[Mapping[str, Any]], Mapping[str, Any]],
    key: str = "name",
) -> Dict[str, Any]:
    """Build mapping by a designated field from a list of mappings."""

    if isinstance(items, Mapping):
        return {**items}

    return {cast(str, item[key]): {**item} for item in items}


def inflate_message(data: Mapping[str, Any]) -> Message:
    """Inflate single message."""

    return Message(
        **inflate(
            chain(
                [("_.name", data["name"]), ("_.type", data["data_type"])],
                ((item["name"], item["value"]) for item in data.get("values", [])),
            )
        ),
    )


def build_messages(setup: Mapping[str, Any]) -> Dict[str, Message]:
    """Build messages."""

    return {name: inflate_message(data) for name, data in setup.items()}


IO_SECTIONS = [
    "inputs",
    "outputs",
    "configuration",
    "parameters",
]


def get_io(config: Mapping[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], ...]:
    """Get IO from app configuration."""

    return (*(build_mapping(config.get(section, [])) for section in IO_SECTIONS),)


@overload
def duration(x: DurationType) -> float:
    """Get the duration in seconds."""


@overload
def duration(x: None) -> None:
    """Get the duration in seconds."""


def duration(x: Optional[DurationType]) -> Optional[float]:
    """Get the duration in seconds."""

    if isinstance(x, float) or x is None:
        return x

    if isinstance(x, int):
        return float(x)

    if isinstance(x, Mapping):
        x = timedelta(**x)

    if isinstance(x, timedelta):
        return x.total_seconds()

    raise TypeError(f"'{type(x).__name__}' has no duration")


def resolve_period(start: Optional[TimeType], end: Optional[TimeType]) -> Tuple[datetime, datetime]:
    """Resolve start and end for a period."""

    def fix(x: Optional[TimeType]) -> Union[datetime, timedelta]:
        if x is None:
            return timedelta(0)
        if isinstance(x, (datetime, timedelta)):
            return x
        if isinstance(x, Mapping):
            return timedelta(**x)
        return datetime.fromtimestamp(x, tz=timezone.utc)

    start, end = fix(start), fix(end)

    if isinstance(start, timedelta):
        if isinstance(end, timedelta):
            raise ValueError("Start or end must be absolute")
        start = end - start
    elif isinstance(end, timedelta):
        end = start + end

    return start, end


def get_distribution(name: str) -> Optional[Distribution]:
    """Get distribution from module name."""

    module = import_module(name)

    try:
        filename = module.__file__
    except AttributeError:
        return None

    if filename is None:
        return None

    path = Path(filename)

    for dist in distributions():
        if dist.files is None:
            continue  # pragma: no cover

        try:
            relative = path.relative_to(dist.locate_file(""))
        except ValueError:  # pragma: no cover
            continue

        if relative in dist.files:
            return dist

    return None


def deep_copy(x: Any) -> Any:
    """Deep copy for mutable containers."""

    if isinstance(x, MutableMapping):
        return {k: deep_copy(v) for k, v in x.items()}

    if isinstance(x, MutableSequence):
        return [deep_copy(v) for v in x]

    if isinstance(x, MutableSet):
        return {deep_copy(v) for v in x}

    return x


def field_info(T: Any) -> Dict[str, Any]:  # pragma: no cover
    """Derive field info from type."""

    return {
        name: S.__origin__
        if isinstance(S, _GenericAlias)
        else field_info(S)
        if isinstance(S, BaseModel)
        else S
        for name, S in get_type_hints(T).items()
        if not name.startswith("_")
    }


T = TypeVar("T")


def deprecated(message: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Deprecation decorator."""

    def outer(f: Callable[..., T]) -> Callable[..., T]:
        message_ = f"{f.__name__} is deprecated" if message is None else message

        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            warn(message_, DeprecationWarning)
            return f(*args, **kwargs)

        return wrapper

    return outer


def deep_get(data: Mapping[str, Any], key: str, default: Any = None) -> Any:
    """Get deep key."""

    return reduce(lambda x, y: x.get(y, default), key.split("."), data)


def get_client(
    config: Optional[Mapping[str, Any]] = None,
    env_prefix: str = "KELVIN",
    app_config_path: Path = APP_CONFIG_PATH,
) -> Client:
    """Get client."""

    config = {**config} if config is not None else {}

    if env_prefix:
        env_prefix += "_"

    url = os.environ.get(f"{env_prefix}URL")

    username = os.environ.get(f"{env_prefix}USERNAME")
    password = os.environ.get(f"{env_prefix}PASSWORD")

    client_id = os.environ.get(f"{env_prefix}CLIENT_ID")
    client_secret = os.environ.get(f"{env_prefix}CLIENT_SECRET")

    if (
        (username and password) is None and (client_id and client_secret) is None
    ) and app_config_path.is_file():
        app_config = yaml.safe_load(app_config_path.read_bytes())

        uploader = deep_get(app_config, UPLOADER_KEY, {})
        credentials = deep_get(uploader, "authentication.openid_client_credentials", {})

        url = uploader.get("host")
        client_id = credentials.get("client_id")
        client_secret = credentials.get("client_secret")
        username = client_id

    config.update(
        (k, v)
        for k, v in [
            ("url", url),
            ("username", username),
            ("client_id", client_id),
            ("client_secret", client_secret),
        ]
        if v is not None
    )

    return Client(config, password=password, use_keychain=False)


def default(x: Any) -> Any:
    """Lower data to a json-ready representation."""

    if isinstance(x, Mapping):
        return {**x}

    if isinstance(x, Collection):
        return [*x]

    return x


def to_rfc3339_timestamp(x: datetime) -> str:
    """Convert datetime to RFC-3339 timestamp (UTC)."""

    return x.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + "Z"


def from_rfc3339_timestamp(x: str) -> datetime:
    """Convert RFC-3339 timestamp to datetime (UTC)."""

    if x.endswith("Z"):
        x = f"{x[:-1]}+00:00"

    return datetime.fromisoformat(x).astimezone(timezone.utc)
