"""Types."""

from __future__ import annotations

import logging
from enum import IntEnum
from typing import Any, Callable, Dict, Generic, Iterator, List, Type, TypeVar

from pydantic import BaseConfig, Field, ValidationError, root_validator
from pydantic.generics import GenericModel
from pydantic.main import ErrorWrapper, ModelField
from typing_inspect import get_args

from kelvin.sdk.datatype import Model

T = TypeVar("T")


class TypedModel(GenericModel, Model, Generic[T]):
    """Typed model."""

    __slots__ = ("_type",)

    _type: T
    _TYPE_FIELD = "type"

    type: str = Field(
        ...,
        name="Type",
        description="Type.",
    )

    @root_validator(pre=True)
    def validate_type(cls: Type[TypedModel], values: Dict[str, Any]) -> Any:  # type: ignore
        """Validate type."""

        fields = cls.__fields__
        aliases = {x.alias: name for name, x in fields.items()}

        type_field = fields[cls._TYPE_FIELD]

        type_name = values.get(cls._TYPE_FIELD, type_field.default)
        if type_name is None:
            return values

        type_names = {*get_args(type_field.type_)}

        if type_name not in type_names:
            return values

        errors: List[ErrorWrapper] = []

        if type_name not in values:
            field_type = fields[aliases[type_name]].type_
            if any(x.required for x in field_type.__fields__.values()):
                errors += [ErrorWrapper(ValueError(f"{type_name!r} missing"), loc=(type_name,))]
            else:
                values[type_name] = {}

        for name in {*values} & type_names:
            if name == type_name:
                continue
            errors += [
                ErrorWrapper(ValueError(f"{name!r} doesn't match type {type_name!r}"), loc=(name,))
            ]

        if errors:
            raise ValidationError(errors, model=cls) from None  # type: ignore

        return values

    def __init__(self, **kwargs: Any) -> None:
        """Initialise typed-model."""

        super().__init__(**kwargs)

        aliases = {x.alias: name for name, x in self.__fields__.items()}

        object.__setattr__(self, "_type", self[aliases[self.type]])

    __iter__: Callable[[], Iterator[str]]  # type: ignore

    @property
    def _(self) -> T:
        """Selected type."""

        return self._type


class LogLevel(IntEnum):
    """Logging level."""

    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    INFO = logging.INFO
    ERROR = logging.ERROR
    TRACE = logging.ERROR

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> int:
        """Validate data."""

        if isinstance(value, int):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls.__members__[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value {value!r}") from None
