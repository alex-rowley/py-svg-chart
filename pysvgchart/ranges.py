from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta


class Range(ABC):

    @abstractmethod
    def value_to_fraction(self, value):
        """
        proportion of range where the value is positioned: [lo; hi] -> [0.0; 1.0]
        NOTE outside [0.0; 1.0] means the value is outside the range.
        """
        ...


class LinearRange(Range):
    lo: date | datetime | float | int
    hi: date | datetime | float | int
    size: float | int | timedelta

    def __init__(self, values):
        if all(isinstance(value, date) for value in values):
            pass
        elif all(isinstance(value, datetime) for value in values):
            pass
        elif all(isinstance(value, float | int) for value in values):
            pass
        else:
            raise TypeError("LinearRange only supports date, datetime, float/int values")
        self.lo = min(values)
        self.hi = max(values)
        self.size = self.hi - self.lo

    def value_to_fraction(self, value: date | datetime | float | int) -> float:
        return (value - self.lo) / self.size


class MappingRange(Range):

    def __init__(self, values: list) -> None:
        value_width = 1.0 / len(values)
        self.map = {
            value: (index + 0.5) * value_width
            for index, value in enumerate(values)
        }

    def value_to_fraction(self, value) -> float:
        return self.map.get(value)


def make_range(values: list[float | int | datetime | date | str]) -> Range:
    if all(isinstance(value, date) for value in values):
        return LinearRange(values)
    if all(isinstance(value, datetime) for value in values):
        return LinearRange(values)
    if all(isinstance(value, float | int) for value in values):
        return LinearRange(values)
    return MappingRange(values)
