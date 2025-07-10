from abc import abstractmethod

from .helpers import collapse_element_list
from .shapes import Shape, Line, Text, Rect, Circle
from .shared import number


class Legend(Shape):
    """
    base class for legends
    """

    @abstractmethod
    def get_element_list(self) -> list: ...


class LineLegend(Legend):
    """
    legend for line charts
    """

    default_line_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(
            self,
            x: number,
            y: number,
            series,
            element_x: number,
            element_y: number,
            line_length: number,
            line_text_gap: number,
    ):
        super().__init__(x, y)
        self.series = series
        self.lines, self.texts = [], []
        x_pos, y_pos = self.position.x, self.position.y
        for index, series in enumerate(self.series):
            self.lines.append(
                Line(x_pos, y_pos, width=line_length, height=0, styles=self.series[series].styles)
            )
            self.texts.append(
                Text(
                    x_pos + line_length + line_text_gap,
                    y_pos,
                    content=series,
                    styles=self.default_line_legend_text_styles,
                )
            )
            x_pos += element_x
            y_pos += element_y

    def get_element_list(self) -> list[str]:
        return collapse_element_list(self.lines, self.texts)


class BarLegend(Legend):
    """
    legend for bar charts
    """

    default_line_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(
            self,
            x: number,
            y: number,
            series,
            element_x: number,
            element_y: number,
            bar_width: number,
            bar_height: number,
            bar_text_gap: number,
    ):
        super().__init__(x, y)
        self.series = series
        self.lines, self.texts = [], []
        x_pos, y_pos = self.position.x, self.position.y
        for index, series in enumerate(self.series):
            self.lines.append(
                Rect(
                    x_pos,
                    y_pos - bar_height / 2,
                    width=bar_width,
                    height=bar_height,
                    styles=self.series[series].styles,
                ),
            )
            self.texts.append(
                Text(
                    x_pos + bar_width + bar_text_gap,
                    y_pos,
                    content=series,
                    styles=self.default_line_legend_text_styles,
                ),
            )
            x_pos += element_x
            y_pos += element_y

    def get_element_list(self) -> list[str]:
        return collapse_element_list(self.lines, self.texts)


class ScatterLegend(Legend):
    """
    legend for a scatter chart
    """

    default_scatter_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(
            self,
            x: number,
            y: number,
            series,
            element_x: number,
            element_y: number,
            shape_text_gap: number,
    ):
        super().__init__(x, y)
        self.series = series
        self.legends, self.texts = [], []
        x_pos, y_pos = self.position.x, self.position.y
        for index, series in enumerate(self.series):
            self.legends.append(
                self.series[series].shape_template(x_pos, y_pos, styles=self.series[series].styles)
            )
            self.texts.append(
                Text(
                    x_pos + shape_text_gap,
                    y_pos,
                    content=series,
                    styles=self.default_scatter_legend_text_styles,
                )
            )
            x_pos += element_x
            y_pos += element_y

    def get_element_list(self) -> list[str]:
        return collapse_element_list(self.legends, self.texts)


class DonutLegend(Legend):
    """
    Legend for donut (or pie) charts using small colored circles.
    """

    default_circle_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(
            self,
            x: number,
            y: number,
            series,
            element_x: number,
            element_y: number,
            circle_radius: number,
            circle_text_gap: number,
    ):
        super().__init__(x, y)
        self.series = series
        self.circles, self.texts = [], []
        x_pos, y_pos = self.position.x, self.position.y
        for index, series_name in enumerate(self.series):
            self.circles.append(
                Circle(
                    x=x_pos + circle_radius,
                    y=y_pos,
                    radius=circle_radius,
                    styles=self.series[series_name].styles,
                )
            )
            self.texts.append(
                Text(
                    x_pos + 2 * circle_radius + circle_text_gap,
                    y_pos,
                    content=series_name,
                    styles=self.default_circle_legend_text_styles,
                )
            )
            x_pos += element_x
            y_pos += element_y

    def get_element_list(self) -> list[str]:
        return collapse_element_list(self.circles, self.texts)
