"""Application Configuration."""

from __future__ import annotations

import sys
from functools import reduce, wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterator,
    List,
    Mapping,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    Type,
    Union,
)

from pydantic import Extra, Field, root_validator, validator

from kelvin.sdk.datatype import Message, Model

from .data import DataBuffer, DataStorage
from .mapping_proxy import MappingProxy
from .utils import DurationType, duration, topic_pattern

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter
else:
    PrettyPrinter = Any

if sys.version_info >= (3, 8):
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore

STORAGE_TYPES: Mapping[Optional[str], Optional[Type[DataStorage]]] = {
    None: None,
    "buffer": DataBuffer,
}


class Check(Model):
    """Data checks."""

    @validator("max_gap", "max_lag", pre=True, always=True)
    def duration_validator(cls, value: Optional[DurationType]) -> Optional[float]:
        """Validate duration fields."""

        return duration(value)

    min_count: Optional[int] = Field(None, description="Minimum value count", ge=0)
    max_gap: Optional[float] = Field(None, description="Maximum gap between values", ge=0.0)
    max_lag: Optional[float] = Field(None, description="Maximum lag since last value", ge=0.0)


class Limit(Model):
    """Output value limits."""

    @validator("frequency", "throttle", pre=True, always=True)
    def duration_validator(cls, value: Optional[DurationType]) -> Optional[float]:
        """Validate duration fields."""

        return duration(value)

    frequency: Optional[float] = Field(None, description="Minimum gap between last emit", ge=0.0)
    throttle: Optional[float] = Field(
        None, description="Minimum gap between last attempt to emit", ge=0.0
    )


class Topic(Model):
    """Storage topic."""

    _init: Optional[Callable[[Sequence[Message]], DataStorage]]
    _pattern: Pattern

    @validator("pattern", pre=True, always=True)
    def validate_pattern(cls, value: str, values: Dict[str, Any]) -> str:
        """Validate pattern field."""

        values["_pattern"] = topic_pattern(value) if isinstance(value, str) else value
        return value

    @root_validator(skip_on_failure=True)
    def validate_init(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Create init function."""

        pattern: str = values["pattern"]
        target: Optional[str] = values["target"]
        storage_type: Optional[str] = values["storage_type"]
        storage_config: Optional[Mapping[str, Any]] = values["storage_config"]

        init: Optional[Callable[[Sequence[Message]], DataStorage]]

        if target is not None:

            T = STORAGE_TYPES[storage_type]

            if T is not None:
                if storage_config is None:
                    storage_config = {}

                # try initialiser
                try:
                    T(**storage_config)
                except Exception as e:
                    raise TypeError(f"Invalid storage configuration: {e}")

                _T: Type[DataStorage] = T
                _storage_config: Mapping[str, Any] = storage_config

                def init(values: Sequence[Message]) -> DataStorage:
                    return _T(values, **_storage_config)

            else:
                if storage_config is not None:
                    raise TypeError(f"Non-storage topics cannot use config (config): {pattern}")
                init = None
        else:
            if storage_type is not None or storage_config is not None:
                raise TypeError(
                    f"Black-holed topics (empty target) cannot use storage (type/config): {pattern}"
                )
            init = None

        values["_init"] = init

        return values

    pattern: str
    target: Optional[str] = None
    final: bool = False
    storage_type: Optional[Literal["buffer"]] = None
    storage_config: Optional[Dict[str, Any]] = None

    @property
    def init(self) -> Optional[Callable[[Sequence[Message]], DataStorage]]:
        """Storage initialiser."""

        return self._init

    def match(self, name: str) -> bool:
        """Match name."""

        return self._pattern.match(name) is not None

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return (x for x in self.__dict__ if not x.startswith("_"))

    @wraps(Model._iter)
    def _iter(self, *args: Any, **kwargs: Any) -> Generator[Tuple[str, Any], None, None]:
        """Replace transformed with original value."""

        return ((k, v) for k, v in super()._iter(*args, **kwargs) if not k.startswith("_"))


class KelvinAppConfig(Model):
    """Kelvin SDK App config."""

    @validator("topics", pre=True, always=True)
    def validate_topics(cls, value: Mapping[str, Any]) -> Dict[str, Any]:
        """Validate topics field."""

        return {
            pattern: {"pattern": pattern, **x} if not isinstance(x, Topic) else x
            for pattern, x in value.items()
        }

    @validator("delay", "pre_fill", pre=True, always=True)
    def duration_validator(cls, value: Optional[DurationType]) -> Optional[float]:
        """Validate duration fields."""

        return duration(value)

    @validator("asset_getter", pre=True, always=True)
    def validate_asset_getter(cls, value: Optional[Union[str, List[str]]]) -> Optional[List[str]]:
        """Validate asset-getter field."""

        if value is None:
            return None

        if not isinstance(value, List):
            value = [value]

        return value

    delay: float = 1.0
    pre_fill: float = 0.0
    last_outputs: bool = False
    remove_duplicates: bool = True
    offset_timestamps: bool = False
    asset_getter: Optional[List[str]] = None

    checks: Dict[str, Check] = {}
    limits: Dict[str, Limit] = {}
    topics: Dict[str, Topic] = {}


class KelvinInfo(Model):
    """App Info."""

    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    node_name: Optional[str] = None
    workload_name: Optional[str] = None


class KelvinConfig(Model):
    """Kelvin configuration."""

    app: KelvinAppConfig = KelvinAppConfig()
    info: KelvinInfo = KelvinInfo()

    class Config(Model.Config):
        """Model config."""

        extra = Extra.allow


class ApplicationConfig(Model):
    """Application configuration base."""

    kelvin: KelvinConfig = KelvinConfig()

    class Config(Model.Config):
        """Model config."""

        arbitrary_types_allowed = True


class DefaultConfig(ApplicationConfig):
    """Default configuration."""

    class Config(ApplicationConfig.Config):
        """Model config."""

        extra = Extra.allow

    def __getattribute__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        result = super().__getattribute__(name)

        if isinstance(result, list):
            return [MappingProxy(x) if isinstance(x, dict) else x for x in result]

        if isinstance(result, dict):
            return MappingProxy(result)

        return result

    def __getitem__(self, name: str) -> Any:
        """Get item."""

        if "." not in name:
            try:
                return getattr(self, name)
            except AttributeError:
                raise KeyError(name) from None

        try:
            return reduce(lambda x, y: x[y], name.split("."), self)
        except KeyError:
            raise KeyError(name) from None

    def __setitem__(self, name: str, value: Any) -> Any:
        """Set item."""

        if "." not in name:
            return setattr(self, name, value)

        head, tail = name.rsplit(".", 1)
        if head not in self:
            self[head] = {}

        return setattr(self[head], tail, value)

    def __delitem__(self, name: str) -> Any:
        """Delete item."""

        if "." not in name:
            return delattr(self, name)

        head, tail = name.rsplit(".", 1)

        return delattr(self[head], tail)
