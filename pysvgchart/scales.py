from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from typing import Any

import math

from .helpers import (
    get_date_or_time_ticks,
    get_logarithmic_ticks,
    get_numeric_ticks,
)
from .shared import (
    dates_sequence,
    datetimes_sequence,
    number,
    numbers_sequence,
)


class Scale(ABC):
    """
    base class for scales
    """

    def __init__(self, ticks: Any):
        self.ticks = ticks

    @abstractmethod
    def get_lowest(self) -> Any:
        """
        get lowest value iff meaningful, None otherwise
        """
        ...

    @abstractmethod
    def value_to_fraction(self, value) -> float:
        """
        proportion of the scale where the value is positioned: [lo; hi] -> [0.0; 1.0]
        NOTE outside [0.0; 1.0] means the value is outside the scale.
        """
        ...


class MappedLinearScale(Scale):
    """
    mapped linear scale - evenly spaced mapped value scale
    """

    lo: date | datetime | number
    hi: date | datetime | number
    size: timedelta | number

    def __init__(
        self,
        ticks: dates_sequence | datetimes_sequence | numbers_sequence,
        shift: bool | date | datetime | number = False,
    ):
        if all(isinstance(tick, date) for tick in ticks):
            pass
        elif all(isinstance(tick, datetime) for tick in ticks):
            pass
        elif all(isinstance(tick, number) for tick in ticks):
            pass
        else:
            raise TypeError("LinearScale only supports date, datetime, float/int values")
        super().__init__(ticks)
        self.lo = self.map_value(min(ticks))
        self.hi = self.map_value(max(ticks))
        self.size = self.hi - self.lo  # type: ignore[operator]
        if shift is False:
            self.shift = None
        elif isinstance(self.lo, date) and isinstance(shift, date):
            self.shift = (self.map_value(shift) - self.lo) / self.size  # type: ignore[operator]
        elif isinstance(self.lo, datetime) and isinstance(shift, datetime):
            self.shift = (self.map_value(shift) - self.lo) / self.size  # type: ignore[operator]
        elif isinstance(self.lo, number) and isinstance(shift, number):
            self.shift = (self.map_value(shift) - self.lo) / self.size  # type: ignore[operator]
        else:
            self.shift = None

    def __str__(self):
        return f"[{self.lo}...{self.hi}] {self.shift if self.shift else '(no shift)'}"

    def __repr__(self):
        return f"<{self.__class__.__name__} lo={self.lo} hi={self.hi} size={self.size} shift={self.shift}>"

    def get_lowest(self) -> date | datetime | number:
        return self.lo

    def value_to_fraction(self, value: date | datetime | number) -> float:
        fraction = (self.map_value(value) - self.lo) / self.size  # type: ignore[operator]
        return fraction - self.shift if self.shift else fraction  # type: ignore[operator, return-value]

    @staticmethod
    @abstractmethod
    def map_value(value: date | datetime | number) -> date | datetime | number: ...


class LinearScale(MappedLinearScale):
    """
    linear scale - values unchanged in mapping
    """

    @staticmethod
    def map_value(value: date | datetime | number) -> date | datetime | number:
        """
        values unchanged in mapping
        """
        return value


class LogarithmicScale(MappedLinearScale):
    """
    logarithmic scale - log10 to map values
    """

    def __init__(
        self,
        ticks: numbers_sequence,
        shift: bool | number = False,
    ):
        if not all(isinstance(tick, number) for tick in ticks):
            raise TypeError("LogarithmicScale only supports float/int values")
        super().__init__(ticks, shift)

    @staticmethod
    def map_value(value: number) -> number:  # type: ignore[override]
        """
        values unchanged in mapping
        """
        return math.log10(value)


class MappingScale(Scale):
    """
    scale for non-numeric values
    """

    def __init__(self, ticks: list | tuple):
        super().__init__(ticks)
        value_width = 1.0 / len(ticks)
        self.map = {value: (index + 0.5) * value_width for index, value in enumerate(ticks)}

    def __str__(self):
        return f"""[{", ".join(f"{tick}" for tick in self.ticks)}]"""

    def __repr__(self):
        return f"""<{self.__class__.__name__} [{", ".join(f"{tick}" for tick in self.ticks)}]>"""

    def get_lowest(self) -> None:
        return None

    def value_to_fraction(self, value) -> float:
        return self.map.get(value, -1.0)


def make_categories_scale(
    values: list | tuple,
    max_ticks: int,
    min_value: Any = None,
    max_value: Any = None,
    include_zero: bool = False,
    shift: bool = False,
    min_unique_values: int = 2,
) -> Scale:
    """
    make a categories scale for a series of values

    :param values: actual values
    :param max_ticks: maximum number of ticks on the scale
    :param min_value: optional minimum value to include on the scale
    :param max_value: optional maximum value to include on the scale
    :param include_zero: whether to include zero on the scale
    :param shift: optional shift for the scale
    :param min_unique_values: minimum number of unique values required
    """
    _ignore = max_ticks, min_value, max_value, include_zero, shift, min_unique_values
    return MappingScale(list(values))


def make_logarithmic_scale(
    values: numbers_sequence,
    max_ticks: int,
    min_value: number | None = None,
    max_value: number | None = None,
    include_zero: bool = False,
    shift: bool = False,
    min_unique_values: int = 2,
) -> Scale:
    if (
        values is None
        or not isinstance(values, list | tuple)
        or len(set(values)) < min_unique_values
    ):
        raise ValueError(
            "Values must be non-empty with at least %d unique elements.",
            min_unique_values,
        )
    if all(isinstance(value, int | float) for value in values):
        ticks = get_logarithmic_ticks(
            values,
            max_ticks,
            min_value=min_value,
            max_value=max_value,
            include_zero=include_zero,
        )
        return LogarithmicScale(ticks, shift=min(values) if shift is True else shift)
    # mixed value types or value type for which there's no ticks creator
    return MappingScale(list(values))


def make_linear_scale(
    values: dates_sequence | datetimes_sequence | numbers_sequence,
    max_ticks: int,
    min_value: date | datetime | number | None = None,
    max_value: date | datetime | number | None = None,
    include_zero: bool = False,
    shift: bool = False,
    min_unique_values: int = 2,
) -> Scale:
    """
    make a scale for a series of values

    :param values: actual values
    :param max_ticks: maximum number of ticks on the scale
    :param min_value: optional minimum value to include on the scale
    :param max_value: optional maximum value to include on the scale
    :param include_zero: whether to include zero on the scale
    :param shift: optional shift for the scale
    :param min_unique_values: minimum number of unique values required
    """
    if (
        values is None
        or not isinstance(values, list | tuple)
        or len(set(values)) < min_unique_values
    ):
        raise ValueError(
            "Values must be non-empty with at least %d unique elements.",
            min_unique_values,
        )
    # value types for which there is a ticks creator
    ticks : dates_sequence | datetimes_sequence | numbers_sequence
    if all(isinstance(value, date) for value in values):
        ticks = get_date_or_time_ticks(
            values,  # type: ignore[arg-type]
            max_ticks,
            min_value=min_value,  # type: ignore[arg-type]
            max_value=max_value,  # type: ignore[arg-type]
        )
        return LinearScale(ticks, shift=min(values) if shift is True else shift)
    if all(isinstance(value, datetime) for value in values):
        ticks = get_date_or_time_ticks(
            values,  # type: ignore[arg-type]
            max_ticks,
            min_value=min_value,  # type: ignore[arg-type]
            max_value=max_value,  # type: ignore[arg-type]
        )
        return LinearScale(ticks, shift=min(values) if shift is True else shift)
    if all(isinstance(value, int | float) for value in values):
        ticks = get_numeric_ticks(
            values,  # type: ignore[arg-type]
            max_ticks,
            min_value=min_value,  # type: ignore[arg-type]
            max_value=max_value,  # type: ignore[arg-type]
            include_zero=include_zero,
        )
        return LinearScale(ticks, shift=min(values) if shift is True else shift)
    # mixed value types or value type for which there's no ticks creator
    return MappingScale(list(values))
