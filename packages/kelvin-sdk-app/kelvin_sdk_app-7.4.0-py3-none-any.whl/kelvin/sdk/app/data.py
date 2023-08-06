"""Data buffer."""

from __future__ import annotations

from abc import abstractmethod
from bisect import bisect
from operator import attrgetter
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from kelvin.sdk.datatype import Message

from .utils import DurationType, duration

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter
    from pandas import Series
else:
    PrettyPrinter = Any
    Series = Any

T = TypeVar("T", bound="DataStorage")


class DataStorage(MutableSequence[Message]):
    """Generic storage base-class."""

    @abstractmethod
    def __init__(self, data: Sequence[Message], **kwargs: Any) -> None:
        """Initialise storage."""

    def __iadd__(self: T, x: Iterable[Message]) -> T:
        return cast(T, super().__iadd__(x))


class DataBuffer(DataStorage):
    """
    Data time-series buffer.

    Parameters
    ----------
    data : :obj:`list`, optional
        Initial values
    window : :obj:`float`, :obj:`int`, :obj:`timedelta` or :obj:`dict`, optional
        Size of rolling window (time-based)
    count : :obj:`int`, optional
        Size of rolling window (count-based)
    getter : :obj:`Callable`, :obj:`str` or :obj:`list`, optional
        Optional getter function to get value from resource value
    delta : :obj:`Callable`, :obj:`str` or :obj:`list`, optional
        Store deltas in value (via getter), keeping the timestamp of the leading edge of the change
    trim : :obj:`bool`, optional
        Strictly trim the data to the window, otherwise keep the previous value outside of the window
    cache : :obj:`bool`, optional
        Cache generated pandas :obj:`Series`

    """

    DISTANT_PAST = float("-inf")
    FAR_FUTURE = float("inf")

    def __init__(
        self,
        data: Optional[Sequence[Message]] = None,
        window: Optional[DurationType] = None,
        count: Optional[int] = None,
        getter: Optional[Union[Callable[[Message], Any], str, Sequence[str]]] = None,
        delta: Optional[Union[Callable[[Message], Any], str, Sequence[str]]] = None,
        trim: bool = True,
        cache: bool = True,
    ) -> None:
        """Initialise buffer."""

        self._window = int(cast(float, duration(window)) * 1e9) if window is not None else None
        if getter is not None and not callable(getter):
            if isinstance(getter, str):
                getter = (getter,)
            getter = cast(Callable[[Message], Any], attrgetter(*getter))
        self._count: Optional[int] = count
        self._getter: Optional[Callable[[Message], Any]] = getter

        self._timestamps: List[int] = []
        self._values: List[Message] = []

        if delta is not None and not callable(delta):
            if isinstance(delta, str):
                delta = (delta,)
            delta = cast(Callable[[Message], Any], attrgetter(*delta))
        self._delta: Optional[Callable[[Message], Any]] = delta
        self._trim = trim
        self._cache = cache

        self._series = None
        self._marker = self.FAR_FUTURE
        self._clean: Tuple[Optional[int], Optional[int]] = (-1, -1)

        if data is not None:
            for value in data:
                self.append(value)

    @property
    def values(self) -> List[Message]:
        """Buffer values."""

        return self._values

    @property
    def timestamps(self) -> List[int]:
        """Buffer timestamps."""

        return self._timestamps

    def get(self, timestamp: int, default: Any = None) -> Any:
        """Get value with default, optionally at a given timestamp."""

        i = bisect(self._timestamps, timestamp)

        if not i:
            return default

        return self._values[i - 1]

    @overload
    def __getitem__(self, index: int) -> Message:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[Message]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Message, List[Message]]:
        """Get value."""

        return self._values[index]

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""

        return [getattr(x, name) for x in self._values]

    def __delitem__(self, index: int) -> None:  # type: ignore
        """Delete value at index."""

        self._clean = (-1, -1)

        self._truncate_cache(self._timestamps[index])

        del self._timestamps[index], self._values[index]

    def __setitem__(self, index: Optional[int], value: Message) -> None:  # type: ignore
        """Set item at timestamp."""

        self._clean = (-1, -1)

        timestamp = index if index is not None else value._.time_of_validity

        n = len(self._timestamps)

        if n:
            # find insertion point
            i = bisect(self._timestamps, timestamp)

            if 0 < i <= n and timestamp == self._timestamps[i - 1]:
                # overwrite existing value
                self._values[i - 1] = value
            elif (
                self._delta is not None
                and 0 < i <= n
                and self._delta(value) == self._delta(self._values[i - 1])
            ):
                # keep earlier timestamp, adopt latest value
                if timestamp > self._values[i - 1]._.time_of_validity:
                    self._values[i - 1] = value
            elif (
                self._delta is not None
                and 0 <= i < n
                and self._delta(value) == self._delta(self._values[i])
            ):
                # adopt earlier timestamp, keep latest value
                self._timestamps[i] = timestamp
            else:
                self._timestamps[:i] += [timestamp]
                self._values[:i] += [value]

            if self._window is not None or self._count is not None:
                self.cleanup()
        else:
            # first value
            self._timestamps[:], self._values[:] = [timestamp], [value]

        self._truncate_cache(timestamp)

    def _truncate_cache(self, timestamp: int) -> None:
        """Truncate cache."""

        from pandas import Timedelta, Timestamp

        if not self._cache:
            return

        self._marker = min(self._marker, timestamp)
        cutoff = Timestamp(timestamp, tz="UTC") - Timedelta(1)
        if self._series is not None and not self._series.empty and cutoff < self._series.index[-1]:
            self._series = self._series[:cutoff]

    def __iter__(self) -> Iterator[Any]:
        """Return iterator."""

        return iter(self._values)

    def __len__(self) -> int:
        """Length of buffer."""

        return len(self._timestamps)

    def __str__(self) -> str:
        """Return str(self)."""

        return str(self.series())

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        extra = [x for x in dir(self._values[0]) if not x.startswith("_")] if self._values else []

        return [*super().__dir__(), *extra]

    def __repr__(self) -> str:
        """Return repr(self)."""

        return f"{type(self).__name__}(window={self._window}, count={self._count}, data={self._values!r})"

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__

        with p.group(4, f"{name}(", ")"):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            p.breakable("")
            p.text("window=")
            p.pretty(self._window)
            p.text(",")
            p.breakable()
            p.text("count=")
            p.pretty(self._count)
            p.text(",")
            p.breakable()
            with p.group(4, "data=[", "]"):
                for i, (t, v) in enumerate(zip(self._timestamps, self._values)):
                    if i:
                        p.text(",")
                        p.breakable()
                    else:
                        p.breakable("")
                    p.pretty((t, v))

    def insert(self, timestamp: Optional[int], value: Message) -> None:
        """Insert value at index."""

        self[timestamp] = value

    def append(self, value: Message) -> None:
        """Append value at index."""

        self[None] = value

    def clear(self) -> None:
        """Clear buffer."""

        super().clear()

        self._series = None
        self._marker = self.FAR_FUTURE
        self._clean = (-1, -1)

    def cleanup(
        self,
        timestamp: Optional[int] = None,
        right: Optional[int] = None,
    ) -> Tuple[Sequence[int], Sequence[Message]]:
        """Trim all series to left of window relative to timestamp and return
        trimmed data."""

        from pandas import Timedelta, Timestamp

        clean = (timestamp, right)

        # bail out if already cleaned for this window
        if clean == self._clean:
            return [], []

        self._clean = clean

        n = len(self._timestamps)

        if not n:
            return [], []

        if right is None and self._window is not None:
            if timestamp is None:
                timestamp = self._timestamps[-1]

            right = timestamp - self._window

        if right is not None:
            j = bisect(self._timestamps, right)
            if not self._trim:
                # keep last out of bounds value
                j -= 1
        else:
            j = 0

        if self._count is not None and self._count < n - j:
            j = n - self._count

        if j > 0:
            if self._cache:
                marker = self._timestamps[j - 1]
                self._marker = max(self._marker, marker)
                cutoff = Timestamp(marker, tz="UTC") + Timedelta(1)
                if (
                    self._series is not None
                    and not self._series.empty
                    and cutoff > self._series.index[0]
                ):
                    self._series = self._series[cutoff:]

            result = (self._timestamps[:j], self._values[:j])
            self._timestamps[:j], self._values[:j] = [], []
            return result

        return [], []

    def series(self) -> Series:
        """Convert buffer to series."""

        from pandas import DatetimeIndex, Series, Timedelta, Timestamp, concat, to_datetime

        if self._cache:
            if self._marker == self.FAR_FUTURE:
                if self._series is None:
                    self._series = Series(
                        index=DatetimeIndex([], name="time", tz="UTC"), dtype=object
                    )
                return self._series

            i = max(bisect(self._timestamps, self._marker) - 1, 0)
            values, index = self._values[i:], self._timestamps[i:]
        else:
            values, index = self._values, self._timestamps

        index = to_datetime(index, unit="ns", utc=True)

        if self._getter is not None:
            values = [*map(self._getter, values)]

        series = Series(values, index, dtype=object if not values else None)

        if not self._cache:
            return series

        cutoff = Timestamp(self._marker, tz="UTC") - Timedelta(1)
        self._marker = self.FAR_FUTURE

        if self._series is not None:
            self._series = concat([self._series[:cutoff], series])
        else:
            self._series = series

        return self._series
