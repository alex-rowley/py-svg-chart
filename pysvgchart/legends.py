from .shapes import Shape, Line, Text, Rect
from .helpers import collapse_element_list


class LineLegend(Shape):
    default_line_legend_text_styles = {'alignment-baseline': 'middle'}

    def __init__(self,
                 x_position,
                 y_position,
                 series,
                 element_x,
                 element_y,
                 line_length,
                 line_text_gap,
                 ):
        super().__init__(x_position, y_position)
        self.series = series
        self.lines, self.texts = [], []
        x_pos, y_pos = self.position.x, self.position.y
        for index, series in enumerate(self.series):
            self.lines.append(Line(x_pos, y_pos, line_length, 0, styles=self.series[series].styles))
            self.texts.append(Text(x_pos + line_length + line_text_gap, y_pos, content=series, styles=self.default_line_legend_text_styles))
            x_pos += element_x
            y_pos += element_y

    def get_element_list(self):
        return collapse_element_list(self.lines, self.texts)


class BarLegend(Shape):
    default_line_legend_text_styles = {'alignment-baseline': 'middle'}

    def __init__(self,
                 x_position,
                 y_position,
                 series,
                 element_x,
                 element_y,
                 bar_width,
                 bar_height,
                 bar_text_gap
                 ):
        super().__init__(x_position, y_position)
        self.series = series
        self.lines, self.texts = [], []
        x_pos, y_pos = self.position.x, self.position.y
        for index, series in enumerate(self.series):
            self.lines.append(Rect(x_pos, y_pos - bar_height/2, bar_width, bar_height, styles=self.series[series].styles))
            self.texts.append(Text(x_pos + bar_width + bar_text_gap, y_pos, content=series, styles=self.default_line_legend_text_styles))
            x_pos += element_x
            y_pos += element_y

    def get_element_list(self):
        return collapse_element_list(self.lines, self.texts)