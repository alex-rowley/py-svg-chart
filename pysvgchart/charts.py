"""
Chart classes - the main entry points for creating SVG charts.

This module contains all chart types available in pysvgchart:
- LineChart / SimpleLineChart: Line plots for time series and trends
- BarChart: Vertical bar charts for category comparisons
- HorizontalBarChart: Horizontal bars (useful for long category names)
- NormalisedBarChart: 100% stacked bars for part-of-whole comparisons
- ScatterChart: Scatter plots for correlation/distribution
- DonutChart: Pie/donut charts for proportions

Class Hierarchy:
    Chart (ABC)
    ├── CartesianChart
    │   ├── VerticalChart -> LineChart, BarChart, ScatterChart, NormalisedBarChart
    │   └── HorizontalChart -> HorizontalBarChart
    └── DonutChart

Typical usage:
    import pysvgchart as psc

    chart = psc.SimpleLineChart(
        x_values=[1, 2, 3],
        y_values=[[10, 20, 15]],
        y_names=['Sales']
    )
    chart.add_legend()
    svg = chart.render()

Series constructors (internal):
    - line_series_constructor: Creates LineSeries from data
    - bar_series_constructor: Creates vertical BarSeries
    - horizontal_bar_series_constructor: Creates horizontal BarSeries
    - normalised_bar_series_constructor: Creates 100% stacked bars
    - scatter_series_constructor: Creates ScatterSeries
"""
from abc import ABC, abstractmethod
from collections.abc import Callable
from itertools import zip_longest, cycle
from typing import Any

from .axes import Axis, XAxis, YAxis, CategoryYAxis
from .helpers import collapse_element_list, default_format
from .legends import BarLegend, Legend, LineLegend, ScatterLegend, DonutLegend
from .scales import make_categories_scale, make_logarithmic_scale, make_linear_scale
from .series import BarSeries, DonutSegment, LineSeries, ScatterSeries, Series
from .shapes import Circle, Group, Line, Point
from .shared import named_styles, number, numbers_sequence, style_def
from .styles import render_all_styles


def no_series_constructor(
        x_values: list | tuple,
        y_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
        x_axis: Axis,
        y_axis: Axis,
        series_names: list[str],
        bar_width: number,
        bar_gap: number,
) -> dict[str, Series]:
    _ignore = x_axis, y_axis, bar_width, bar_gap
    if len(y_values) != len(series_names):
        raise ValueError("y_values and series_names must have the same length")
    if not all(len(y_value) == len(x_values) for y_value in y_values):
        raise ValueError("y_values must all have the same length as x_values")
    return {name: Series(x_values[0], y_value[0]) for name, y_value in zip(series_names, y_values)}


def line_series_constructor(
        x_values: list | tuple,
        y_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
        x_axis: Axis,
        y_axis: Axis,
        series_names: list[str],
        bar_width: number,
        bar_gap: number,
) -> dict[str, Series]:
    _ignore = bar_width, bar_gap
    if len(y_values) != len(series_names):
        raise ValueError("y_values and series_names must have the same length")
    if not all(len(y_value) == len(x_values) for y_value in y_values):
        raise ValueError("y_values must all have the same length as x_values")
    return {
        name: LineSeries(
            points=[
                Point(x=x, y=y)  # type: ignore[arg-type]
                for x, y in zip(x_axis.get_positions(x_values), y_axis.get_positions(y_value))
            ],
            x_values=x_values,
            y_values=y_value,  # type: ignore[arg-type]
        )
        for name, y_value in zip(series_names, y_values)
    }


def bar_series_constructor(
        x_values: list | tuple,
        y_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
        x_axis: Axis,
        y_axis: Axis,
        series_names: list[str],
        bar_width: number,
        bar_gap: number,
) -> dict[str, Series]:
    if len(y_values) != len(series_names):
        raise ValueError("y_values and series_names must have the same length")
    if not all(len(y_value) == len(x_values) for y_value in y_values):
        raise ValueError("y_values must all have the same length as x_values")
    no_series = len(series_names)
    bar_span = bar_width + bar_gap
    bar_shift = bar_span * (no_series - 1) / 2
    return {
        name: BarSeries(
            points=[
                Point(x=x + bar_nr * bar_span - bar_shift, y=y)  # type: ignore[arg-type, operator]
                for x, y in zip(x_axis.get_positions(x_values), y_axis.get_positions(y_value))
            ],
            x_values=x_values,
            y_values=y_value,  # type: ignore[arg-type]
            bar_heights=[
                y_axis.position.y + y_axis.length - y if y is not None else 0
                for y in y_axis.get_positions(y_value)
            ],
            bar_width=bar_width,
        )
        for bar_nr, name, y_value in zip(range(no_series), series_names, y_values)
    }


def normalised_bar_series_constructor(
        x_values: list | tuple,
        y_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
        x_axis: Axis,
        y_axis: Axis,
        series_names: list[str],
        bar_width: number,
        bar_gap: number,
) -> dict[str, Series]:
    _ignore = bar_gap
    if len(y_values) < 1:
        raise ValueError("y_values should not be empty")
    if len(y_values) != len(series_names):
        raise ValueError("y_values and series_names must have the same length")
    if not all(len(y_value) == len(x_values) for y_value in y_values):
        raise ValueError("y_values must all have the same length as x_values")
    rtn: dict[str, Series] = {}
    prev_cumulative_scaled_y_values = [0] * len(y_values[0])
    total_values = [sum(y) for y in zip(*y_values)]
    x_positions = x_axis.get_positions(x_values)
    for name, y_value in zip(series_names, y_values):
        cumulative_scaled_y_values = [
            min(a + b / t, 1.0) if t != 0 else a
            for a, b, t in zip(prev_cumulative_scaled_y_values, y_value, total_values)
        ]
        prev_scaled_positions = y_axis.get_positions(prev_cumulative_scaled_y_values)
        scaled_positions = y_axis.get_positions(cumulative_scaled_y_values)
        rtn[name] = BarSeries(
            points=[Point(x=x, y=y) for x, y in zip(x_positions, scaled_positions)],  # type: ignore[arg-type]
            x_values=x_values,
            y_values=y_value,  # type: ignore[arg-type]
            bar_heights=[b - a for a, b in zip(scaled_positions, prev_scaled_positions)],  # type: ignore[operator]
            bar_width=bar_width,
        )
        prev_cumulative_scaled_y_values = cumulative_scaled_y_values
    return rtn


def scatter_series_constructor(
        x_values: list | tuple,
        y_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
        x_axis: Axis,
        y_axis: Axis,
        series_names: list[str],
        bar_width: number,
        bar_gap: number,
) -> dict[str, Series]:
    _ignore = bar_width, bar_gap
    if len(y_values) != len(series_names):
        raise ValueError("y_values and series_names must have the same length")
    if not all(len(y_value) == len(x_values) for y_value in y_values):
        raise ValueError("y_values must all have the same length as x_values")
    return {
        name: ScatterSeries(
            points=[
                Point(x=x, y=y)  # type: ignore[arg-type]
                for x, y in zip(x_axis.get_positions(x_values), y_axis.get_positions(y_value))
            ],
            x_values=x_values,
            y_values=y_value,  # type: ignore[arg-type]
        )
        for name, y_value in zip(series_names, y_values)
    }


def horizontal_bar_series_constructor(
        y_values: list | tuple,
        x_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
        y_axis: Axis,
        x_axis: Axis,
        series_names: list[str],
        bar_width: number,
        bar_gap: number,
) -> dict[str, Series]:
    """
    Constructor for horizontal bar series.
    In horizontal bars:
      - y_values are categories (shown on y-axis/vertical)
      - x_values are the numerical values (shown on x-axis/horizontal)
      - bars grow horizontally (left to right)
    """
    if len(x_values) != len(series_names):
        raise ValueError("x_values and series_names must have the same length")
    if not all(len(x_value) == len(y_values) for x_value in x_values):
        raise ValueError("x_values must all have the same length as y_values")
    no_series = len(series_names)
    bar_span = bar_width + bar_gap
    bar_shift = bar_span * (no_series - 1) / 2
    # Calculate zero position on x-axis, clamped to axis bounds
    zero_fraction = x_axis.scale.value_to_fraction(0)
    zero_x = x_axis.position.x + max(0.0, min(1.0, zero_fraction)) * x_axis.length
    from .series import HorizontalBarSeries
    return {
        name: HorizontalBarSeries(
            points=[
                Point(x=x if x is not None else zero_x, y=y + bar_nr * bar_span - bar_shift)  # type: ignore[arg-type, operator]
                for x, y in zip(x_axis.get_positions(x_value), y_axis.get_positions(y_values))
            ],
            x_values=y_values,
            y_values=x_value,  # type: ignore[arg-type]
            bar_heights=[
                x - zero_x if x is not None else 0
                for x in x_axis.get_positions(x_value)
            ],
            bar_width=bar_width,
        )
        for bar_nr, name, x_value in zip(range(no_series), series_names, x_values)
    }


def default_x_range_constructor(x_values: list | tuple) -> list:
    return [v for v in x_values]


def default_y_range_constructor(
        y_values: list[list] | list[tuple] | tuple[list, ...] | tuple[tuple, ...],
) -> list:
    return [v for series in y_values for v in series]


class Chart(ABC):
    """
    overall svg template for chart
    """

    svg_begin_template = '<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

    height: number
    width: number
    custom_elements: list[str]
    series: dict[str, Any]

    def __init__(self, height: number, width: number) -> None:
        self.height = height
        self.width = width
        self.custom_elements = []
        self.series = {}

    @abstractmethod
    def get_element_list(self) -> list[str]: ...

    def add_custom_element(self, custom_element) -> None:
        self.custom_elements.append(custom_element)

    def modify_series(self, modifier: Callable) -> None:
        self.series = {name: modifier(series) for name, series in self.series.items()}

    def render(self) -> str:
        return "\n".join(
            [
                self.svg_begin_template.format(height=self.height, width=self.width),
                *self.get_element_list(),
                "</svg>",
            ]
        )

    def render_with_all_styles(
            self,
            styles: named_styles | None = None,
            include_default: bool = True,
    ) -> str:
        """
        :param styles: styles to use
        :param include_default: also use the default styles (to enable things like hover text)
        :return:
        """
        return "\n".join(
            [
                self.svg_begin_template.format(height=self.height, width=self.width),
                "<style>",
                render_all_styles(styles, include_default),
                "</style>",
                *self.get_element_list(),
                "</svg>",
            ]
        )

    def save(
            self,
            file_path: str,
            styles: named_styles | None = None,
            include_default: bool = True
    ) -> None:
        """
        Save the chart to a file.
        :param file_path: file path to write to
        :param styles: styles to use (if provided, will render with all styles)
        :param include_default: also use the default styles (only used when styles is provided)
        :return:
        """
        with open(file_path, "w+") as file:
            if styles is not None or not include_default:
                file.write(self.render_with_all_styles(styles, include_default))
            else:
                file.write(self.render())

    @staticmethod
    def generate_series_names(
            prefix: str,
            n: int,
            names: list[str] | tuple[str, ...] | None,
    ) -> list[str]:
        """
        generate missing names for series
        """
        return [
                   real if real is not None else generated
                   for real, generated in zip_longest(
                names if names is not None else [],
                [f"{prefix} {k}" for k in range(1, n + 1)],
            )
               ][:n]


class CartesianChart(Chart):
    """
    Base class for charts with two perpendicular axes (X and Y).
    This class provides the foundation for both vertical and horizontal oriented charts.
    Subclasses should define orientation-specific behavior.
    """

    __colour_defaults__ = ["green", "red", "blue", "orange", "yellow", "black"]

    default_major_grid_styles = {"stroke": "#6e6e6e", "stroke-width": "0.6"}
    default_minor_grid_styles = {"stroke": "#6e6e6e", "stroke-width": "0.2"}
    colour_property = "stroke"

    # The defaults are for axis classes - subclasses should override
    x_axis_type = Axis
    y_axis_type = Axis
    x_axis_scale_maker = staticmethod(make_linear_scale)
    y_axis_scale_maker = staticmethod(make_linear_scale)

    # The defaults are for series - subclasses should override
    x_range_constructor = staticmethod(default_x_range_constructor)
    y_range_constructor = staticmethod(default_y_range_constructor)
    series_constructor = staticmethod(no_series_constructor)

    def set_palette(self, colours: list[str] | tuple[str, ...]) -> None:
        for series, colour in zip(self.series, cycle(colours)):
            self.series[series].styles[self.colour_property] = colour


class VerticalChart(CartesianChart):
    """
    Any chart with a vertical y-axis and a horizontal x-axis
    - all lines share the same x values
    - y values differ
    """

    def __init__(
            self,
            # chart data
            x_values: list | tuple,
            y_values: list | tuple,
            sec_y_values: list | tuple | None = None,
            y_names: list[str] | None = None,
            sec_y_names: list[str] | None = None,
            # x-axis
            x_min: Any = None,
            x_max: Any = None,
            x_zero: bool = False,
            x_max_ticks: int = 12,
            x_shift: bool = False,
            x_label_format: Callable = default_format,
            x_axis_title: str | None = None,
            x_axis_title_styles: dict | None = None,
            x_axis_title_offset: int = 40,
            # primary y-axis
            y_min: Any = None,
            y_max: Any = None,
            y_zero: bool = False,
            y_max_ticks: int = 12,
            y_shift: bool = False,
            y_label_format: Callable = default_format,
            y_axis_title: str | None = None,
            y_axis_title_styles: dict | None = None,
            y_axis_title_offset: int = 40,
            # secondary y-axis
            sec_y_min: Any = None,
            sec_y_max: Any = None,
            sec_y_zero: bool = False,
            sec_y_max_ticks: int = 12,
            sec_y_shift: bool = False,
            sec_y_label_format: Callable = default_format,
            sec_y_axis_title: str | None = None,
            sec_y_axis_title_styles: dict | None = None,
            sec_y_axis_title_offset: int = 40,
            # canvas
            left_margin: number = 100,
            right_margin: number = 100,
            y_margin: number = 100,
            height: number = 600,
            width: number = 800,
            bar_width: number = 40,
            bar_gap: number = 2,
            colours: list[str] | tuple[str, ...] | None = None,
    ):
        """
        create a simple line chart
        :param x_values: the list of x values shared by all lines
        :param y_values: a list line values for the primary y-axis, each a list itself
        :param sec_y_values:  a list line values for the secondary y-axis, each a list itself
        :param y_names: optional list of names of the lines of the primary y-axis
        :param sec_y_names: optional list of names of the lines of the secondary y-axis
        :param x_min: optional minimum x value, only used in numeric axis
        :param x_max: optional maximum x value, only used in numeric axis
        :param x_zero: optionally force 0 to be included on the x-axis
        :param x_max_ticks: optional maximum number of ticks on the x-axis
        :param x_shift: optionally shift the x-axis - True: left side of graph touches the y-axis, value: shift graph left by that amount
        :param x_label_format: optional format of labels on the x-axis
        :param y_min: optional minimum value on the primary y-axis if it is numeric
        :param y_max: optional maximum value on the primary y-axis if is is numeric
        :param y_zero: optionally force 0 to be included on the primary y-axis
        :param y_max_ticks: optional maximum number of ticks on the primary y-axis
        :param y_shift: optionally shift the y-axis - True: bottom side of graph touches the x-axis, value: shift graph down by that amount
        :param y_label_format: optional format of labels on the primary y-axis
        :param sec_y_min: optional minimum value on the secondary y-axis
        :param sec_y_max: optional maximum value on the secondary y-axis
        :param sec_y_zero: optionally force 0 to be included on the secondary y-axis
        :param sec_y_max_ticks: optional maximum number of ticks on the secondary y-axis
        :param sec_y_shift: optionally shift the secondary y-axis - True: bottom side of graph touches the x-axis, value: shift graph down by that amount
        :param sec_y_label_format: optional format of labels on the secondary y-axis
        :param left_margin: optional left margin for the x-axis
        :param right_margin: optional right margin for the x-axis
        :param y_margin: optional margin for the y-axis
        :param height: optional height of the graph
        :param width: optional width of the graph
        :param colours: optional list of colours for the series
        """
        # Allow flat list for single-series: [1,2,3] → [[1,2,3]]
        if y_values and not isinstance(y_values[0], (list, tuple)):
            y_values = [y_values]
        if sec_y_values is not None and sec_y_values and not isinstance(sec_y_values[0], (list, tuple)):
            sec_y_values = [sec_y_values]

        super().__init__(height, width)
        self.x_axis = self.x_axis_type(  # type: ignore[abstract]
            x_position=left_margin,
            y_position=height - y_margin,
            data_points=self.x_range_constructor(x_values),
            axis_length=width - left_margin - right_margin,
            label_format=x_label_format,
            max_ticks=x_max_ticks,
            min_value=x_min,
            max_value=x_max,
            include_zero=x_zero,
            shift=x_shift,
            scale_maker=self.x_axis_scale_maker,
            title=x_axis_title,
            title_styles=x_axis_title_styles,
            title_offset=x_axis_title_offset
        )
        self.y_axis = self.y_axis_type(  # type: ignore[abstract]
            x_position=left_margin,
            y_position=y_margin,
            data_points=self.y_range_constructor(y_values),
            axis_length=height - 2 * y_margin,
            label_format=y_label_format,
            max_ticks=y_max_ticks,
            min_value=y_min,
            max_value=y_max,
            include_zero=y_zero,
            shift=y_shift,
            scale_maker=self.y_axis_scale_maker,
            secondary=False,
            title=y_axis_title,
            title_offset=y_axis_title_offset,
            title_styles=y_axis_title_styles
        )
        series_names = self.generate_series_names("Series", len(y_values), y_names)
        self.series = self.series_constructor(
            x_values,
            y_values,
            self.x_axis,
            self.y_axis,
            series_names,
            bar_width,
            bar_gap,
        )

        if sec_y_values is None:
            self.sec_y_axis = None
        else:
            sec_series_names = self.generate_series_names(
                "Secondary series",
                len(sec_y_values),
                sec_y_names,
            )
            self.sec_y_axis = self.y_axis_type(  # type: ignore[abstract]
                x_position=width - right_margin,
                y_position=y_margin,
                data_points=default_y_range_constructor(sec_y_values),
                axis_length=height - 2 * y_margin,
                label_format=sec_y_label_format,
                max_ticks=sec_y_max_ticks,
                min_value=sec_y_min,
                max_value=sec_y_max,
                include_zero=sec_y_zero,
                shift=sec_y_shift,
                scale_maker=self.y_axis_scale_maker,
                secondary=True,
                title=sec_y_axis_title,
                title_styles=sec_y_axis_title_styles,
                title_offset=sec_y_axis_title_offset
            )
            self.series.update(
                self.series_constructor(
                    x_values,
                    sec_y_values,
                    self.x_axis,
                    self.sec_y_axis,
                    sec_series_names,
                    bar_width,
                    bar_gap,
                )
            )
        self.legend: Legend | None = None
        self.set_palette(colours if colours else self.__colour_defaults__)

    def add_legend(
            self,
            x_position: number = 730,
            y_position: number = 200,
            element_x: number = 0,
            element_y: number = 20,
            line_length: number = 20,
            line_text_gap: number = 5,
            **kwargs,
    ):
        self.legend = LineLegend(
            x_position,
            y_position,
            self.series,
            element_x,
            element_y,
            line_length,
            line_text_gap,
        )

    def add_grids(
            self,
            minor_x_ticks: int = 0,
            minor_y_ticks: int = 0,
            major_grid_style: style_def | None = None,
            minor_grid_style: style_def | None = None,
    ):
        self.add_y_grid(minor_y_ticks, major_grid_style, minor_grid_style)
        self.add_x_grid(minor_x_ticks, major_grid_style, minor_grid_style)

    def add_y_grid(
            self,
            minor_ticks: int = 0,
            major_grid_style: style_def | None = None,
            minor_grid_style: style_def | None = None,
    ):
        major_style = (
            major_grid_style.copy()
            if major_grid_style is not None
            else self.default_major_grid_styles.copy()
        )
        minor_style = (
            minor_grid_style.copy()
            if minor_grid_style is not None
            else self.default_minor_grid_styles.copy()
        )
        positions = self.x_axis.get_positions(self.x_axis.scale.ticks, include_axis=False)
        for pos in positions:
            if pos is None:  # shifted out of the visible range
                continue
            minor_unit = self.x_axis.length / (len(self.x_axis.scale.ticks) - 1) / (minor_ticks + 1)
            for grid_line_nr in range(minor_ticks + 1):  # 0: major, others: minor
                self.y_axis.grid_lines.append(
                    Line(
                        x=pos - grid_line_nr * minor_unit,
                        y=self.x_axis.position.y - self.y_axis.length,
                        width=0,
                        height=self.y_axis.length,
                        styles=major_style if grid_line_nr == 0 else minor_style,
                    )
                )

    def add_x_grid(
            self,
            minor_ticks: int = 0,
            major_grid_style: style_def | None = None,
            minor_grid_style: style_def | None = None,
    ):
        major_style = (
            major_grid_style.copy()
            if major_grid_style is not None
            else self.default_major_grid_styles.copy()
        )
        minor_style = (
            minor_grid_style.copy()
            if minor_grid_style is not None
            else self.default_minor_grid_styles.copy()
        )
        positions = self.y_axis.get_positions(self.y_axis.scale.ticks, include_axis=False)
        for pos in positions:
            if pos is None:  # shifted out of the visible range
                continue
            minor_unit = self.y_axis.length / (len(self.y_axis.scale.ticks) - 1) / (minor_ticks + 1)
            for grid_line_nr in range(minor_ticks + 1):  # 0: major, others: minor
                self.y_axis.grid_lines.append(
                    Line(
                        x=self.y_axis.position.x,
                        y=pos + grid_line_nr * minor_unit,
                        width=self.x_axis.length,
                        height=0,
                        styles=major_style if grid_line_nr == 0 else minor_style,
                    )
                )

    def add_hover_modifier(
            self,
            modifier: Callable,
            radius: number,
            series_list: list[str] | tuple[str, ...] | None = None,
    ):
        def build_hover_marker(point, x_value, y_value, series_name):
            series_styles = self.series[series_name].styles
            circle = Circle(point.x, y=point.y, radius=radius, styles={"style": "opacity:0;"})
            mod = modifier(
                point,
                x_value=x_value,
                y_value=y_value,
                series_name=series_name,
                styles=series_styles,
            )
            return Group(children=[circle] + mod, classes=["psc-hover-group"])

        series_list = [s for s in self.series] if series_list is None else series_list
        for s in self.series:
            if s in series_list:
                hover_markers = [
                    build_hover_marker(p, x, y, s)
                    for p, x, y in self.series[s].pv_generator
                    if x is not None and y is not None and p.x is not None and p.y is not None
                ]
                self.series[s].add_custom_elements(hover_markers)

    def get_element_list(self) -> list[str]:
        return collapse_element_list(
            [self.x_axis],
            [self.y_axis],
            [self.legend],
            [self.sec_y_axis],
            [self.series[s] for s in self.series],
            self.custom_elements,
        )


class HorizontalChart(CartesianChart):
    """
    Chart with a horizontal value axis and vertical category/data axis.
    Useful for horizontal bar charts where categories are on Y-axis and values on X-axis.
    """

    def __init__(
            self,
            # chart data
            x_values: list | tuple,
            y_values: list | tuple,
            sec_x_values: list | tuple | None = None,
            x_names: list[str] | None = None,
            sec_x_names: list[str] | None = None,
            # y-axis (categories/vertical)
            y_min: Any = None,
            y_max: Any = None,
            y_zero: bool = False,
            y_max_ticks: int = 12,
            y_shift: bool = False,
            y_label_format: Callable = default_format,
            y_axis_title: str | None = None,
            y_axis_title_styles: dict | None = None,
            y_axis_title_offset: int = 40,
            # primary x-axis (values/horizontal)
            x_min: Any = None,
            x_max: Any = None,
            x_zero: bool = False,
            x_max_ticks: int = 12,
            x_shift: bool = False,
            x_label_format: Callable = default_format,
            x_axis_title: str | None = None,
            x_axis_title_styles: dict | None = None,
            x_axis_title_offset: int = 40,
            # secondary x-axis
            sec_x_min: Any = None,
            sec_x_max: Any = None,
            sec_x_zero: bool = False,
            sec_x_max_ticks: int = 12,
            sec_x_shift: bool = False,
            sec_x_label_format: Callable = default_format,
            sec_x_axis_title: str | None = None,
            sec_x_axis_title_styles: dict | None = None,
            sec_x_axis_title_offset: int = 40,
            # canvas
            left_margin: number = 100,
            right_margin: number = 100,
            x_margin: number = 100,
            height: number = 600,
            width: number = 800,
            bar_width: number = 40,
            bar_gap: number = 2,
            colours: list[str] | tuple[str, ...] | None = None,
    ):
        """
        Create a horizontal chart where categories are on Y-axis (vertical) and values on X-axis (horizontal).
        Parameters match the physical axes: x_values are horizontal (values), y_values are vertical (categories).
        """
        # Allow flat list for single-series: [1,2,3] → [[1,2,3]]
        if x_values and not isinstance(x_values[0], (list, tuple)):
            x_values = [x_values]
        if sec_x_values is not None and sec_x_values and not isinstance(sec_x_values[0], (list, tuple)):
            sec_x_values = [sec_x_values]

        super().__init__(height, width)

        # In horizontal charts:
        # - Y-axis is vertical and shows categories (y_values)
        # - X-axis is horizontal and shows values (x_values)
        self.y_axis = self.y_axis_type(  # type: ignore[abstract]
            x_position=left_margin,
            y_position=x_margin,
            data_points=self.x_range_constructor(y_values),
            axis_length=height - 2 * x_margin,
            label_format=y_label_format,
            max_ticks=y_max_ticks,
            min_value=y_min,
            max_value=y_max,
            include_zero=y_zero,
            shift=y_shift,
            scale_maker=self.y_axis_scale_maker,
            secondary=False,
            title=y_axis_title,
            title_styles=y_axis_title_styles,
            title_offset=y_axis_title_offset
        )

        self.x_axis = self.x_axis_type(  # type: ignore[abstract]
            x_position=left_margin,
            y_position=height - x_margin,
            data_points=self.y_range_constructor(x_values),
            axis_length=width - left_margin - right_margin,
            label_format=x_label_format,
            max_ticks=x_max_ticks,
            min_value=x_min,
            max_value=x_max,
            include_zero=x_zero,
            shift=x_shift,
            scale_maker=self.x_axis_scale_maker,
            title=x_axis_title,
            title_styles=x_axis_title_styles,
            title_offset=x_axis_title_offset
        )

        series_names = self.generate_series_names("Series", len(x_values), x_names)
        self.series = self.series_constructor(
            y_values,
            x_values,
            self.y_axis,
            self.x_axis,
            series_names,
            bar_width,
            bar_gap,
        )

        self.sec_x_axis = None
        if sec_x_values is not None:
            sec_series_names = self.generate_series_names(
                "Secondary series",
                len(sec_x_values),
                sec_x_names,
            )
            self.sec_x_axis = self.x_axis_type(  # type: ignore[abstract]
                x_position=left_margin,
                y_position=x_margin,
                data_points=default_x_range_constructor(sec_x_values),
                axis_length=width - left_margin - right_margin,
                label_format=sec_x_label_format,
                max_ticks=sec_x_max_ticks,
                min_value=sec_x_min,
                max_value=sec_x_max,
                include_zero=sec_x_zero,
                shift=sec_x_shift,
                scale_maker=self.x_axis_scale_maker,
                secondary=True,
                title=sec_x_axis_title,
                title_styles=sec_x_axis_title_styles,
                title_offset=sec_x_axis_title_offset
            )
            self.series.update(
                self.series_constructor(
                    x_values,
                    sec_x_values,
                    self.y_axis,
                    self.sec_x_axis,
                    sec_series_names,
                    bar_width,
                    bar_gap,
                )
            )

        self.legend: Legend | None = None
        self.set_palette(colours if colours else self.__colour_defaults__)

    def get_element_list(self) -> list[str]:
        return collapse_element_list(
            [self.x_axis],
            [self.y_axis],
            [self.legend],
            [self.sec_x_axis],
            [self.series[s] for s in self.series],
            self.custom_elements,
        )


class LineChart(VerticalChart):
    x_axis_type = XAxis  # type: ignore[assignment]
    y_axis_type = YAxis  # type: ignore[assignment]
    series_constructor = staticmethod(line_series_constructor)

    def __init__(self, *args, **kwargs):
        """
        intercept init to handle optional logarithmic scale
        :param x_log: optionally enable logarithmic scale
        :param y_log: optionally enable logarithmic scale
        """
        x_log = kwargs.pop("x_log", False)
        y_log = kwargs.pop("y_log", False)
        if x_log:
            self.x_axis_scale_maker = staticmethod(make_logarithmic_scale)
        if y_log:
            self.y_axis_scale_maker = staticmethod(make_logarithmic_scale)
        super().__init__(*args, **kwargs)


class SimpleLineChart(LineChart):
    x_axis_type = XAxis
    y_axis_type = YAxis
    series_constructor = staticmethod(line_series_constructor)


class BarChart(LineChart):
    x_axis_type = XAxis
    y_axis_type = YAxis
    x_axis_scale_maker = staticmethod(make_categories_scale)
    y_axis_scale_maker = staticmethod(make_linear_scale)
    series_constructor = staticmethod(bar_series_constructor)
    colour_property = "fill"

    def add_legend(  # type: ignore[override]
            self,
            x_position: number = 730,
            y_position: number = 200,
            element_x: number = 0,
            element_y: number = 20,
            bar_width: number = 30,
            bar_height: number = 5,
            bar_text_gap: number = 5,
            **kwargs,
    ):
        self.legend = BarLegend(
            x_position,
            y_position,
            self.series,
            element_x,
            element_y,
            bar_width,
            bar_height,
            bar_text_gap,
        )


class HorizontalBarChart(HorizontalChart):
    """
    Horizontal bar chart where categories are on Y-axis (vertical) and values on X-axis (horizontal).
    Bars grow from zero: positive values extend right, negative values extend left.
    """
    x_axis_type = XAxis
    y_axis_type = CategoryYAxis
    x_axis_scale_maker = staticmethod(make_linear_scale)
    y_axis_scale_maker = staticmethod(make_categories_scale)
    series_constructor = staticmethod(horizontal_bar_series_constructor)
    colour_property = "fill"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Move the y-axis line to the zero position on the x-axis
        zero_fraction = self.x_axis.scale.value_to_fraction(0)
        zero_x = self.x_axis.position.x + max(0.0, min(1.0, zero_fraction)) * self.x_axis.length
        if self.y_axis.axis_line is not None:
            self.y_axis.axis_line.position.x = zero_x
            self.y_axis.axis_line.end.x = zero_x
        # Remove tick marks — they were positioned relative to the original axis
        # location and would float disconnected from the moved axis line
        if zero_x != self.y_axis.position.x:
            self.y_axis.tick_lines = []

    def add_legend(  # type: ignore[override]
            self,
            x_position: number = 730,
            y_position: number = 200,
            element_x: number = 0,
            element_y: number = 20,
            bar_width: number = 30,
            bar_height: number = 5,
            bar_text_gap: number = 5,
            **kwargs,
    ):
        self.legend = BarLegend(
            x_position,
            y_position,
            self.series,
            element_x,
            element_y,
            bar_width,
            bar_height,
            bar_text_gap,
        )


class NormalisedBarChart(LineChart):
    x_axis_type = XAxis
    y_axis_type = YAxis
    x_axis_scale_maker = staticmethod(make_categories_scale)
    y_axis_scale_maker = staticmethod(make_linear_scale)
    series_constructor = staticmethod(normalised_bar_series_constructor)
    y_range_constructor = staticmethod(lambda y_values: [0, 1])
    colour_property = "fill"

    def add_legend(  # type: ignore[override]
            self,
            x_position: number = 730,
            y_position: number = 200,
            element_x: number = 0,
            element_y: number = 20,
            bar_width: number = 30,
            bar_height: number = 5,
            bar_text_gap: number = 5,
            **kwargs,
    ):
        self.legend = BarLegend(
            x_position,
            y_position,
            self.series,
            element_x,
            element_y,
            bar_width,
            bar_height,
            bar_text_gap,
        )


class ScatterChart(LineChart):
    x_axis_type = XAxis
    y_axis_type = YAxis
    series_constructor = staticmethod(scatter_series_constructor)
    colour_property = "fill"

    def add_legend(  # type: ignore[override]
            self,
            x_position: number = 730,
            y_position: number = 200,
            element_x: number = 0,
            element_y: number = 20,
            shape_text_gap: number = 5,
            **kwargs,
    ):
        self.legend = ScatterLegend(
            x_position,
            y_position,
            self.series,
            element_x,
            element_y,
            shape_text_gap,
        )


class DonutChart(Chart):
    """
    A donut style chart which is similar to a pie chart but has a blank interior
    """

    __segment_colour_defaults__ = ["green", "red", "blue", "orange", "yellow", "black"]

    def __init__(
            self,
            values: numbers_sequence,
            labels: list[str] | tuple[str, ...] | None = None,
            colours: list[str] | tuple[str, ...] | None = None,
            height: number = 400,
            width: number = 400,
            centre_x: number = 150,
            centre_y: number = 200,
            radius_inner: number = 55,
            radius_outer: number = 150,
            rotation: number = 70,
    ):
        """
        create a donut chart
        :param values: values to chart
        :param labels: labels to each segment
        :param height: canvas height
        :param width: canvas width
        :param centre_x: horizontal centre of donut
        :param centre_y: vertical centre of donut
        :param radius_inner: inner radius of donut (blank area)
        :param radius_outer: outer radius of donut (other area)
        :param rotation: rotation offset
        """
        super().__init__(height, width)
        self.values = values
        series_names = self.generate_series_names("Series", len(values), labels)
        # compute start and end angles for the value segments
        accumulated_values: list[number] = [0]
        for value in values:
            accumulated_values.append(value + accumulated_values[-1])
        total_value = accumulated_values[-1]
        rotated_angles = [rotation + (360 * value) / total_value for value in accumulated_values]
        start_end_angles = [
            rotated_angles[index: index + 2] for index in range(len(rotated_angles) - 1)
        ]
        self.colours = colours if colours is not None else self.__segment_colour_defaults__
        self.labels = None
        # create value segments
        self.legend: Legend | None = None
        for index, (start_theta, end_theta), name in zip(
                range(len(values)),
                start_end_angles,
                series_names,
        ):
            colour = self.colours[index % len(self.colours)]
            self.series[name] = DonutSegment(
                colour,
                start_theta,
                end_theta,
                radius_inner,
                radius_outer,
                centre_x,
                centre_y,
            )

    def add_hover_modifier(self, modifier: Callable):
        names = list(self.series)
        segments = [self.series[name] for name in names]
        chart_total = sum(self.values)
        self.series = {
            n: Group(
                children=(
                        [s] + modifier(position=s.position, name=n, value=v, chart_total=chart_total)
                )
            )
            for n, v, s in zip(names, self.values, segments)
        }
        for s in self.series:
            self.series[s].add_classes(["psc-hover-group"])

    def add_legend(  # type: ignore[override]
            self,
            x_position: number = 320,
            y_position: number = 175,
            element_x: number = 0,
            element_y: number = 20,
            circle_radius: number = 5,
            circle_text_gap: number = 5,
            **kwargs,
    ):
        self.legend = DonutLegend(
            x_position,
            y_position,
            self.series,
            element_x,
            element_y,
            circle_radius,
            circle_text_gap,
        )

    def get_element_list(self) -> list[str]:
        return collapse_element_list([self.series[s] for s in self.series], self.custom_elements, [self.legend])
