from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from typing import Any

from .helpers import get_ticks


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

    def __init__(self, ticks):
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

    def __str__(self):
        return f"[{self.lo}...{self.hi}]"

    def __repr__(self):
        return f"<{self.__class__.__name__} lo={self.lo} hi={self.hi} size={self.size}>"

    def get_lowest(self) -> date | datetime | float | int:
        return self.lo

    def value_to_fraction(self, value: date | datetime | float | int) -> float:
        return (value - self.lo) / self.size


class MappingScale(Scale):

    def __init__(self, ticks: list) -> None:
        super().__init__(ticks)
        value_width = 1.0 / len(ticks)
        self.map = {
            value: (index + 0.5) * value_width
            for index, value in enumerate(ticks)
        }

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
    min_unique_values=2
) -> Scale:
    ticks = get_ticks(
        values=values,
        max_ticks=max_ticks,
        min_value=min_value,
        max_value=max_value,
        include_zero=include_zero,
        min_unique_values=min_unique_values,
    )
    if all(isinstance(tick, date) for tick in ticks):
        return LinearScale(ticks)
    if all(isinstance(tick, datetime) for tick in ticks):
        return LinearScale(ticks)
    if all(isinstance(tick, float | int) for tick in ticks):
        return LinearScale(ticks)
    return MappingScale(ticks)
