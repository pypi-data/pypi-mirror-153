"""Mapping Proxy."""

# TODO:
# - add callback for saving changes

from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING, Any, Iterator, List, Mapping, MutableMapping, Optional, Set, Tuple

from pydantic import BaseModel

from .utils import flatten

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter
else:
    PrettyPrinter = Any


class MappingProxy(MutableMapping[str, Any]):
    """Attribute access proxy."""

    __slots__ = ("_data", "_name")

    _data: MutableMapping[str, Any]
    _name: Optional[str]

    def __init__(self, data: MutableMapping[str, Any], name: Optional[str] = None) -> None:
        """Initialise mapping proxy."""

        if isinstance(data, MappingProxy):
            data = data._data

        if not isinstance(data, MutableMapping):
            raise TypeError("data must be a mutable mapping")

        self._data = data
        self._name = name

    def __getitem__(self, name: str) -> Any:
        """Get item."""

        if "." in name and name not in self._data:
            result = reduce(lambda x, y: x[y], name.split("."), self)
        else:
            result = self._data[name]

        if isinstance(result, list):
            return [
                type(self)(x)
                if isinstance(x, MutableMapping) and not isinstance(x, BaseModel)
                else x
                for x in result
            ]

        if isinstance(result, MutableMapping) and not isinstance(result, BaseModel):
            return type(self)(result)

        return result

    def __setitem__(self, name: str, value: Any) -> Any:
        """Set item."""

        if "." in name and name not in self._data:
            head, tail = name.split(".", 1)
            if head not in self._data:
                self._data[head] = {}
            data = self[head]
        else:
            data, tail = self._data, name

        data[tail] = value

    def __delitem__(self, name: str) -> None:
        """Delete item."""

        if "." in name and name not in self._data:
            head, tail = name.split(".", 1)
            data = self._data[head]
        else:
            data, tail = self._data, name

        del data[tail]

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            return self[name]
        except KeyError:
            if self._name is not None:
                raise AttributeError(f"{self._name} has no attribute {name!r}") from None
            return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute."""

        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name: str) -> None:
        """Delete attribute."""

        if name.startswith("_"):
            super().__delattr__(name)
        else:
            try:
                del self[name]
            except KeyError:
                return super().__delattr__(name)

    def __len__(self) -> int:
        """Length of mapping."""

        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        """Get iterator."""

        return iter(self._data)

    def __eq__(self, obj: Any) -> bool:
        """Determine if objects have the same key/values."""

        if not isinstance(obj, Mapping):
            return False

        if not isinstance(obj, MappingProxy):
            obj = MappingProxy({**obj})

        seen: Set[str] = {*()}

        for k, v in self.flatten(deep=True):
            try:
                if v != obj.get(k, ...):
                    return False
            except TypeError:  # pragma: no cover
                return False
            seen |= {k}

        # check for extra keys
        for k, v in obj.flatten(deep=True):
            if k not in seen:
                return False

        return True

    def __str__(self) -> str:
        """String representation."""

        return repr(self)

    def __repr__(self) -> str:
        """String representation."""

        if self._name is not None:
            return f"<{self._name}>({', '.join(f'{k}={v!r}' for k, v in self._data.items())})"

        return f"{type(self).__name__}({self._data!r})"

    @classmethod
    def _repr_pretty_mapping_(cls, obj: Mapping, p: PrettyPrinter, cycle: bool) -> None:
        """Default pretty representation for generic mapping types."""

        name: Optional[str] = getattr(obj, "_name", None)

        if name is not None:
            left, right = (f"<{name}>(", ")")
            key = "{k}="
        else:
            left, right = ("{", "}")
            key = "{k!r}: "

        with p.group(4, left, right):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            for i, (k, v) in enumerate(sorted(obj.items())):
                if i:
                    p.text(",")
                    p.breakable()
                else:
                    p.breakable("")
                p.text(key.format(k=k))
                if isinstance(v, Mapping) and not isinstance(v, BaseModel):
                    cls._repr_pretty_mapping_(v, p, cycle)
                else:
                    p.pretty(v)

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        self._repr_pretty_mapping_(self, p, cycle)

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*iter(self), *super().__dir__()]

    def flatten(self, deep: bool = False) -> Iterator[Tuple[str, Any]]:
        """Get items."""

        return (
            (k if not l else f"{k}.{l}", w)
            for k, v in self.items()
            for l, w in (
                v.flatten(deep=deep)
                if isinstance(v, MappingProxy)
                else flatten(v)
                if deep and isinstance(v, Mapping)
                else [("", v)]
            )
        )
