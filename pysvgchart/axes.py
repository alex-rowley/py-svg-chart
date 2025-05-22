from __future__ import annotations

from .helpers import simple_limits, get_limits, collapse_element_list
from .ranges import make_range
from .shapes import Shape, Text, Line


class Axis(Shape):
    """
    axis of a graph
    """
    default_axis_styles = {'stroke': '#2e2e2c'}
    limits_function = staticmethod(get_limits)

    def __init__(
            self,
            x_position,
            y_position,
            data_points,
            axis_length,
            label_format,
            max_ticks=10,
            axis_styles=None,
            tick_length=5,
            min_value=None,
            max_value=None,
            include_zero=False,
            shift=False,
            min_unique_values=2,
    ):
        super().__init__(x_position, y_position)
        self.data_points = data_points
        self.length = axis_length
        self.limits = self.limits_function(
            values=data_points,
            max_ticks=max_ticks,
            min_value=min_value,
            max_value=max_value,
            include_zero=include_zero,
            min_unique_values=min_unique_values,
        )
        self.range = make_range(self.limits)
        self.label_format = label_format
        self.axis_line = None
        self.tick_lines, self.tick_texts, self.grid_lines = [], [], []
        _ = (axis_styles, tick_length)
        # if shift is True, use the gap that would be created between the graph and the axis
        lo = self.range.get_lowest() if shift is True else None
        self.shift = (min(self.data_points) - lo) if lo is not None else shift

    def proportion_of_range(self, value):
        return self.range.value_to_fraction(value - self.shift if self.shift else value)

    def get_element_list(self):
        return collapse_element_list([self.axis_line], self.tick_lines, self.tick_texts, self.grid_lines)

    def get_positions(self, values):
        return []


class XAxis(Axis):
    """
    x-axis of a graph
    """
    default_tick_text_styles = {'text-anchor': 'middle', 'dominant-baseline': 'hanging'}

    def __init__(
            self,
            x_position,
            y_position,
            data_points,
            axis_length,
            label_format,
            max_ticks=10,
            axis_styles=None,
            tick_length=5,
            min_value=None,
            max_value=None,
            include_zero=False,
            shift=False,
    ):
        super().__init__(
            x_position=x_position,
            y_position=y_position,
            data_points=data_points,
            axis_length=axis_length,
            label_format=label_format,
            max_ticks=max_ticks,
            axis_styles=axis_styles,
            tick_length=tick_length,
            min_value=min_value,
            max_value=max_value,
            include_zero=include_zero,
            shift=shift,
            min_unique_values=2,  # at least two unique values needed on the x-axis to create a meaningful graph
        )
        styles = axis_styles or self.default_axis_styles.copy()
        self.axis_line = Line(x_position=self.position.x, y_position=self.position.y, width=axis_length, height=0, styles=styles)
        limit_positions = self.get_positions(self.limits)

        for m, p in zip(self.limits, limit_positions):
            if p is None:  # shifted out of the visible range
                continue
            self.tick_lines.append(Line(x_position=p, width=0, y_position=self.position.y, height=tick_length, styles=styles))
            self.tick_texts.append(Text(x_position=p, y_position=self.position.y + 2 * tick_length, content=label_format(m), styles=self.default_tick_text_styles.copy()))

    def get_positions(self, values):
        proportions_of_range = [
            self.proportion_of_range(value)
            for value in values
        ]
        return [
            self.position.x + prop * self.length if 0.0 <= prop <= 1.0 else None
            for prop in proportions_of_range
        ]


class YAxis(Axis):
    """
    x-axis of a graph
    """
    default_tick_text_styles = {'text-anchor': 'end', 'dominant-baseline': 'middle'}
    default_sec_tick_text_styles = {'text-anchor': 'start', 'dominant-baseline': 'middle'}

    def __init__(
            self,
            x_position,
            y_position,
            data_points,
            axis_length,
            label_format,
            max_ticks=10,
            axis_styles=None,
            tick_length=5,
            min_value=None,
            max_value=None,
            include_zero=False,
            shift=False,
            secondary=False,
    ):
        super().__init__(
            x_position=x_position,
            y_position=y_position,
            data_points=data_points,
            axis_length=axis_length,
            label_format=label_format,
            max_ticks=max_ticks,
            axis_styles=axis_styles,
            tick_length=tick_length,
            min_value=min_value,
            max_value=max_value,
            include_zero=include_zero,
            shift=shift,
            min_unique_values=1,  # one unique value is sufficient for the y-axis
        )
        styles = axis_styles or self.default_axis_styles.copy()
        self.axis_line = Line(x_position=self.position.x, y_position=self.position.y, width=0, height=axis_length, styles=styles)
        limit_positions = self.get_positions(self.limits)

        for m, p in zip(self.limits, limit_positions):
            if p is None:  # shifted out of the visible range
                continue
            if secondary:
                self.tick_lines.append(Line(x_position=self.position.x, width=tick_length, y_position=p, height=0, styles=styles))
                self.tick_texts.append(Text(x_position=self.position.x + 2 * tick_length, y_position=p, content=label_format(m), styles=self.default_sec_tick_text_styles.copy()))
            else:
                self.tick_lines.append(Line(x_position=self.position.x - tick_length, width=tick_length, y_position=p, height=0, styles=styles))
                self.tick_texts.append(Text(x_position=self.position.x - 2 * tick_length, y_position=p, content=label_format(m), styles=self.default_tick_text_styles.copy()))

    def get_positions(self, values):
        proportions_of_range = [
            1 - self.proportion_of_range(value)
            for value in values
        ]
        return [
            self.position.y + prop * self.length if 0.0 <= prop <= 1.0 else None
            for prop in proportions_of_range
        ]


class SimpleXAxis(XAxis):
    """
    x-axis of a graph with evenly spaced x values
    """

    limits_function = staticmethod(simple_limits)

    def get_positions(self, values):
        if values is None:
            return None

        return [
            self.position.x + (index + 1 / 2) * self.length / len(values)
            for index in range(len(values))
        ]
