from .shapes import Shape, Line, Text, Rect
from .helpers import collapse_element_list


class LineLegend(Shape):
    """
    legend for line charts
    """

    default_line_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(
        self,
        x,
        y,
        series,
        element_x,
        element_y,
        line_length,
        line_text_gap,
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

    def get_element_list(self):
        return collapse_element_list(self.lines, self.texts)


class BarLegend(Shape):
    """
    legend for bar charts
    """

    default_line_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(self, x, y, series, element_x, element_y, bar_width, bar_height, bar_text_gap):
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

    def get_element_list(self):
        return collapse_element_list(self.lines, self.texts)


class ScatterLegend(Shape):
    """
    legend for a scatter chart
    """

    default_scatter_legend_text_styles = {"alignment-baseline": "middle"}

    def __init__(
        self,
        x,
        y,
        series,
        element_x,
        element_y,
        shape_text_gap,
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

    def get_element_list(self):
        return collapse_element_list(self.legends, self.texts)
