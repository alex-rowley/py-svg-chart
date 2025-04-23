from .helpers import collapse_element_list, default_format
from .series import DonutSegment, LineSeries, BarSeries
from .axes import Axis, XAxis, YAxis, SimpleXAxis
from .shapes import Point, Line, Group, Circle
from .legends import LineLegend, BarLegend
from .styles import render_all_styles


def line_series_constructor(x_values, y_values, x_axis, y_axis, series_names, bar_width, bar_gap):
    return {
        name: LineSeries(
            points=[
                Point(x, y)
                for x, y in zip(x_axis.get_positions(x_values), y_axis.get_positions(y_value))
            ],
            x_values=x_values,
            y_values=y_value
        )
        for name, y_value in zip(series_names, y_values)
    }


def bar_series_constructor(x_values, y_values, x_axis, y_axis, series_names, bar_width, bar_gap):
    no_series = len(series_names)
    x_start_offs = (bar_width + bar_gap) * (no_series - 1) / 2
    return {
        name: BarSeries(
            points=[
                Point(x - x_start_offs + (bar_width + bar_gap) * index, y)
                for x, y in zip(x_axis.get_positions(x_values), y_axis.get_positions(y_value))
            ],
            x_values=x_values,
            y_values=y_value,
            bar_heights=[y_axis.position.y + y_axis.length - y for y in y_axis.get_positions(y_value)],
            bar_width=bar_width,
        )
        for index, name, y_value, in zip(range(no_series), series_names, y_values)
    }


def normalised_bar_series_constructor(x_values, y_values, x_axis, y_axis, series_names, bar_width, bar_gap):
    rtn = dict()
    prev_cumulative_scaled_y_values = [0] * len(y_values[0])
    total_values = [sum(y) for y in zip(*y_values)]
    x_positions = x_axis.get_positions(x_values)
    for y_value, name in zip(y_values, series_names):
        cumulative_scaled_y_values = [a + b / t for a, b, t in zip(prev_cumulative_scaled_y_values, y_value, total_values)]
        prev_scaled_positions = y_axis.get_positions(prev_cumulative_scaled_y_values)
        scaled_positions = y_axis.get_positions(cumulative_scaled_y_values)
        rtn[name] = BarSeries(
            points=[Point(x, y) for x, y in zip(x_positions, scaled_positions)],
            x_values=x_values,
            y_values=y_value,
            bar_heights=[b - a for a, b in zip(scaled_positions, prev_scaled_positions)],
            bar_width=bar_width,
        )
        prev_cumulative_scaled_y_values = cumulative_scaled_y_values
    return rtn


def default_y_range_constructor(y_values):
    return [v for series in y_values for v in series]


class Chart:
    """
    overall svg template for chart
    """
    svg_begin_template = '<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.custom_elements = []
        self.series = []

    def get_element_list(self):
        raise NotImplementedError("Not implemented in generic chart.")

    def add_custom_element(self, custom_element):
        self.custom_elements.append(custom_element)

    def modify_series(self, modifier):
        self.series = [modifier(s) for s in self.series]

    def render(self):
        return '\n'.join([
            self.svg_begin_template.format(height=self.height, width=self.width),
            *self.get_element_list(),
            '</svg>'
        ])

    def render_with_all_styles(self, styles=None, include_default=True):
        """
        :param styles: list of styles to use
        :param include_default: also use the default styles (to enable things like hover text)
        :return:
        """
        return '\n'.join([
            self.svg_begin_template.format(height=self.height, width=self.width),
            '<style>',
            render_all_styles(styles, include_default),
            '</style>',
            *self.get_element_list(),
            '</svg>'
        ])


class VerticalChart(Chart):
    """
    Any chart with a vertical y-axis and a horizontal x-axis
    - all lines share the same x values
    - y values differ
    """
    __colour_defaults__ = ['green', 'red', 'blue', 'orange', 'yellow', 'black']

    default_major_grid_styles = {'stroke': '#6e6e6e', 'stroke-width': '0.6'}
    default_minor_grid_styles = {'stroke': '#6e6e6e', 'stroke-width': '0.2'}
    colour_property = 'stroke'

    # The defaults are for line class
    x_axis_type = Axis
    y_range_constructor = staticmethod(default_y_range_constructor)
    series_constructor = staticmethod(lambda **kwargs: kwargs)

    def __init__(
            self,
            # chart data
            x_values,
            y_values,
            sec_y_values=None,
            y_names=None,
            sec_y_names=None,
            # x-axis
            x_min=None,
            x_max=None,
            x_zero=False,
            x_max_ticks=12,
            x_label_format=default_format,
            # primary y-axis
            y_min=None,
            y_max=None,
            y_zero=False,
            y_max_ticks=12,
            y_label_format=default_format,
            # secondary y-axis
            sec_y_min=None,
            sec_y_max=None,
            sec_y_zero=False,
            sec_y_max_ticks=12,
            sec_y_label_format=default_format,
            # canvas
            left_margin=100,
            right_margin=100,
            y_margin=100,
            height=600,
            width=800,
            bar_width=40,
            bar_gap=2,
            colours=None
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
        :param x_label_format: optional format of labels on the x-axis
        :param y_min: optional minimum value on the primary y-axis if it is numeric
        :param y_max: optional maximum value on the primary y-axis if is is numeric
        :param y_zero: optionally force 0 to be included on the primary y-axis
        :param y_max_ticks: optional maximum number of ticks on the primary y-axis
        :param y_label_format: optional format of labels on the primary y-axis
        :param sec_y_min: optional minimum value on the secondary y-axis
        :param sec_y_max: optional maximum value on the secondary y-axis
        :param sec_y_zero: optionally force 0 to be included on the secondary y-axis
        :param sec_y_max_ticks: optional maximum number of ticks on the secondary y-axis
        :param sec_y_label_format: optional format of labels on the secondary y-axis
        :param x_margin: optional margin for the x-axis
        :param y_margin: optional margin for the y-axis
        :param height: optional height of the graph
        :param width: optional width of the graph
        :param colours: optional list of colours for the series
        """
        super().__init__(height, width)
        self.x_axis = None
        self.y_axis = None
        self.legend = None
        self.sec_y_axis = None
        self.series = []
        self.y_axis = YAxis(
            x_position=left_margin,
            y_position=y_margin,
            data_points=self.y_range_constructor(y_values),
            axis_length=height - 2 * y_margin,
            label_format=y_label_format,
            max_ticks=y_max_ticks,
            min_value=y_min,
            max_value=y_max,
            include_zero=y_zero,
        )
        self.x_axis = self.x_axis_type(
            x_position=left_margin,
            y_position=height - y_margin,
            data_points=x_values,
            axis_length=width - left_margin - right_margin,
            label_format=x_label_format,
            max_ticks=x_max_ticks,
            min_value=x_min,
            max_value=x_max,
            include_zero=x_zero,
        )
        series_names = y_names if y_names is not None else ['Series {0}'.format(k) for k in range(len(y_values))]
        self.series = self.series_constructor(x_values, y_values, self.x_axis, self.y_axis, series_names, bar_width, bar_gap)

        if sec_y_values is not None:
            sec_all_y_values = [v for series in sec_y_values for v in series]
            sec_series_names = sec_y_names if sec_y_names is not None else ['Secondary series {0}'.format(k) for k in range(len(sec_y_values))]
            self.sec_y_axis = YAxis(
                x_position=width - right_margin,
                y_position=y_margin,
                data_points=sec_all_y_values,
                axis_length=height - 2 * y_margin,
                label_format=sec_y_label_format,
                max_ticks=sec_y_max_ticks,
                min_value=sec_y_min,
                max_value=sec_y_max,
                include_zero=sec_y_zero,
                secondary=True,
            )
            self.series.update(self.series_constructor(x_values, sec_y_values, self.x_axis, self.sec_y_axis, sec_series_names, bar_width, bar_gap))

        for index, series in enumerate(self.series):
            series_colours = colours if colours else self.__colour_defaults__
            self.series[series].styles[self.colour_property] = series_colours[index % len(series_colours)]

    def add_legend(self, x_position=730, y_position=200, element_x=0, element_y=20, line_length=20, line_text_gap=5):
        self.legend = LineLegend(x_position, y_position, self.series, element_x, element_y, line_length, line_text_gap)

    def add_grids(self, minor_x_ticks=0, minor_y_ticks=0, major_grid_style=None, minor_grid_style=None):
        self.add_y_grid(minor_y_ticks, major_grid_style, minor_grid_style)
        self.add_x_grid(minor_x_ticks, major_grid_style, minor_grid_style)

    def add_y_grid(self, minor_ticks=0, major_grid_style=None, minor_grid_style=None):
        major_style = major_grid_style.copy() if major_grid_style is not None else self.default_major_grid_styles.copy()
        minor_style = minor_grid_style.copy() if minor_grid_style is not None else self.default_minor_grid_styles.copy()
        positions = self.x_axis.get_positions(self.x_axis.limits[1:])
        for p in positions:
            self.y_axis.grid_lines.append(
                Line(
                    x_position=p,
                    y_position=self.x_axis.position.y - self.y_axis.length,
                    width=0,
                    height=self.y_axis.length,
                    styles=major_style
                )
            )
            minor_step = self.x_axis.length / (len(self.x_axis.limits) - 1) / (minor_ticks + 1)
            for j in range(1, minor_ticks + 1):
                minor_offset = p - j * minor_step
                self.y_axis.grid_lines.append(Line(
                    x_position=minor_offset,
                    y_position=self.x_axis.position.y - self.y_axis.length,
                    width=0,
                    height=self.y_axis.length,
                    styles=minor_style
                ))

    def add_x_grid(self, minor_ticks=0, major_grid_style=None, minor_grid_style=None):
        major_style = major_grid_style.copy() if major_grid_style is not None else self.default_major_grid_styles.copy()
        minor_style = minor_grid_style.copy() if minor_grid_style is not None else self.default_minor_grid_styles.copy()
        positions = self.y_axis.get_positions(self.y_axis.limits[1:])
        for p in positions:
            self.x_axis.grid_lines.append(
                Line(
                    x_position=self.y_axis.position.x,
                    y_position=p,
                    width=self.x_axis.length,
                    height=0,
                    styles=major_style
                )
            )
            minor_step = self.y_axis.length / (len(self.y_axis.limits) - 1) / (minor_ticks + 1)
            for j in range(1, minor_ticks + 1):
                minor_offset = p + j * minor_step
                self.y_axis.grid_lines.append(Line(
                    x_position=self.y_axis.position.x,
                    y_position=minor_offset,
                    width=self.x_axis.length,
                    height=0,
                    styles=minor_style
                ))

    def add_hover_modifier(self, modifier, radius, series_list=None):
        def build_hover_marker(point, x_value, y_value, series_name):
            series_styles = self.series[series_name].styles
            circle = Circle(point.x, y_position=point.y, radius=radius, styles={'style': 'opacity:0;'})
            mod = modifier(point, x_value=x_value, y_value=y_value, series_name=series_name, styles=series_styles)
            return Group(children=[circle] + mod, classes=['psc-hover-group'])

        series_list = [s for s in self.series] if series_list is None else series_list
        for s in self.series:
            if s in series_list:
                hover_markers = [build_hover_marker(p, x, y, s) for p, x, y in self.series[s].pv_generator]
                self.series[s].add_custom_elements(hover_markers)

    def get_element_list(self):
        return collapse_element_list([self.x_axis], [self.y_axis], [self.legend], [self.sec_y_axis], [self.series[s] for s in self.series], self.custom_elements)


class LineChart(VerticalChart):
    x_axis_type = XAxis
    series_constructor = staticmethod(line_series_constructor)


class SimpleLineChart(LineChart):
    x_axis_type = SimpleXAxis
    series_constructor = staticmethod(line_series_constructor)


class BarChart(LineChart):
    x_axis_type = SimpleXAxis
    series_constructor = staticmethod(bar_series_constructor)
    colour_property = 'fill'

    def add_legend(self, x_position=730, y_position=200, element_x=0, element_y=20, bar_width=30, bar_height=5, bar_text_gap=5):
        self.legend = BarLegend(x_position, y_position, self.series, element_x, element_y, bar_width, bar_height, bar_text_gap)


class NormalisedBarChart(LineChart):
    x_axis_type = SimpleXAxis
    series_constructor = staticmethod(normalised_bar_series_constructor)
    y_range_constructor = staticmethod(lambda y_values: [0, 1])
    colour_property = 'fill'

    def add_legend(self, x_position=730, y_position=200, element_x=0, element_y=20, bar_width=30, bar_height=5, bar_text_gap=5):
        self.legend = BarLegend(x_position, y_position, self.series, element_x, element_y, bar_width, bar_height, bar_text_gap)


class DonutChart(Chart):
    """
    A donut style chart which is similar to a pie chart but has a blank interior
    """
    __segment_colour_defaults__ = ['green', 'red', 'blue', 'orange', 'yellow', 'black']

    def __init__(self, values, labels=None, height=200, width=200, centre_x=100, centre_y=100, radius_inner=55, radius_outer=100, rotation=270):
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
        self.series = dict()
        self.values = values
        series_names = labels if labels is not None else ['Series {0}'.format(k) for k in range(len(values))]
        # compute start and end angles for the value segments
        accumulated_values = [0]
        for value in values:
            accumulated_values.append(value + accumulated_values[-1])
        total_value = accumulated_values[-1]
        rotated_angles = [rotation + (360 * value) / total_value for value in accumulated_values]
        start_end_angles = [rotated_angles[index:index + 2] for index in range(len(rotated_angles) - 1)]
        # create value segments
        for index, (start_theta, end_theta), name in zip(range(len(values)), start_end_angles, series_names):
            colour = self.__segment_colour_defaults__[index % len(self.__segment_colour_defaults__)]
            self.series[name] = DonutSegment(colour, start_theta, end_theta, radius_inner, radius_outer, centre_x, centre_y)

    def add_hover_modifier(self, modifier):
        names = list(self.series)
        segments = [self.series[name] for name in names]
        self.series = {
            n: Group(
                children=[s] + modifier(
                    position=s.position,
                    name=n,
                    value=v,
                    chart_total=sum(self.values)
                )
            )
            for n, v, s in zip(names, self.values, segments)
        }
        for s in self.series:
            self.series[s].add_classes(['psc-hover-group'])

    def get_element_list(self):
        return collapse_element_list([self.series[s] for s in self.series], self.custom_elements)
