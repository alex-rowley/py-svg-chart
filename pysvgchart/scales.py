from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime, date, timedelta
from typing import Any

import math

from .helpers import (
    get_date_or_time_ticks,
    get_logarithmic_ticks,
    get_numeric_ticks,
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


class LinearScale(Scale):
    lo: date | datetime | float | int
    hi: date | datetime | float | int
    size: float | int | timedelta

    def __init__(self, ticks, shift=False):
        if all(isinstance(tick, date) for tick in ticks):
            pass
        elif all(isinstance(tick, datetime) for tick in ticks):
            pass
        elif all(isinstance(tick, float | int) for tick in ticks):
            pass
        else:
            raise TypeError("LinearRange only supports date, datetime, float/int values")
        super().__init__(ticks)
        self.lo = min(ticks)
        self.hi = max(ticks)
        self.size = self.hi - self.lo
        if shift is False:
            self.shift = None
        elif isinstance(self.lo, date) and isinstance(shift, date):
            self.shift = (shift - self.lo) / self.size
        elif isinstance(self.lo, datetime) and isinstance(shift, datetime):
            self.shift = (shift - self.lo) / self.size
        elif isinstance(self.lo, float | int) and isinstance(shift, float | int):
            self.shift = (shift - self.lo) / self.size
        else:
            self.shift = None

    def __str__(self):
        return f"[{self.lo}...{self.hi}] {self.shift if self.shift else '(no shift)'}"

    def __repr__(self):
        return f"<{self.__class__.__name__} lo={self.lo} hi={self.hi} size={self.size} shift={self.shift}>"

    def get_lowest(self) -> date | datetime | float | int:
        return self.lo

    def value_to_fraction(self, value: date | datetime | float | int) -> float:
        fraction = (value - self.lo) / self.size
        return fraction - self.shift if self.shift else fraction


class LogarithmicScale(Scale):
    log_lo: float | int
    log_hi: float | int
    size: float | int

    def __init__(self, ticks, shift=False):
        if all(isinstance(tick, float | int) for tick in ticks):
            pass
        else:
            raise TypeError("LinearRange only supports date, datetime, float/int values")
        super().__init__(ticks)
        self.log_lo = math.log10(min(ticks))
        self.log_hi = math.log10(max(ticks))
        self.size = self.log_hi - self.log_lo
        if shift is False:
            self.shift = None
        elif isinstance(self.log_lo, float | int) and isinstance(shift, float | int):
            self.shift = (math.log10(shift) - self.log_lo) / self.size
        else:
            self.shift = None

    def __str__(self):
        return f"[{self.log_lo}...{self.log_hi}] {self.shift if self.shift else '(no shift)'}"

    def __repr__(self):
        return f"<{self.__class__.__name__} log_lo={self.log_lo} log_hi={self.log_hi} size={self.size} shift={self.shift}>"

    def get_lowest(self) -> date | datetime | float | int:
        return self.log_lo

    def value_to_fraction(self, value: date | datetime | float | int) -> float:
        fraction = (math.log10(value) - self.log_lo) / self.size
        print(f"DBG {value=} {math.log10(value)=} {fraction=}")
        return fraction - self.shift if self.shift else fraction


class MappingScale(Scale):
    """
    scale for non-numeric/non-linear values
    """

    def __init__(self, ticks: list) -> None:
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


def make_scale(
    values,
    max_ticks,
    min_value=None,
    max_value=None,
    include_zero=False,
    shift=False,
    min_unique_values=2,
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
    if values is None or not isinstance(values, Iterable) or len(set(values)) < min_unique_values:
        raise ValueError(
            "Values must be a non-empty iterable with at least %d unique elements.",
            min_unique_values,
        )
    # value types for which there is a ticks creator
    if all(isinstance(value, date) for value in values):
        ticks = get_date_or_time_ticks(
            values,
            max_ticks,
            min_value=min_value,
            max_value=max_value,
        )
        return LinearScale(ticks, shift=min(values) if shift is True else shift)
    if all(isinstance(value, datetime) for value in values):
        ticks = get_date_or_time_ticks(
            values,
            max_ticks,
            min_value=min_value,
            max_value=max_value,
        )
        return LinearScale(ticks, shift=min(values) if shift is True else shift)
    if all(isinstance(value, int | float) for value in values):
        ticks = get_numeric_ticks(
            values,
            max_ticks,
            min_value=min_value,
            max_value=max_value,
            include_zero=include_zero,
        )
        return LinearScale(ticks, shift=min(values) if shift is True else shift)
    # mixed value types or value type for which there's no ticks creator
    return MappingScale(list(values))


def make_categories_scale(
    values,
    max_ticks,
    min_value=None,
    max_value=None,
    include_zero=False,
    shift=False,
    min_unique_values=2,
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
    values,
    max_ticks,
    min_value=None,
    max_value=None,
    include_zero=False,
    shift=False,
    min_unique_values=2,
) -> Scale:
    if values is None or not isinstance(values, Iterable) or len(set(values)) < min_unique_values:
        raise ValueError(
            "Values must be a non-empty iterable with at least %d unique elements.",
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
