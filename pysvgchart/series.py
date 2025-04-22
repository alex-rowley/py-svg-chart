import math

from .shapes import Shape
from .helpers import collapse_element_list


class Series(Shape):

    def __init__(self, x_position, y_position, styles=None, classes=None):
        super().__init__(x_position=x_position, y_position=y_position, styles=styles, classes=classes)
        self.custom_elements = []

    def add_custom_elements(self, custom_elements):
        self.custom_elements.extend(custom_elements)


class DonutSegment(Series):
    path_template = (
        '<path d="M {outer_begin_x},{outer_begin_y} '
        'A {radius_outer} {radius_outer} 0 {large_arc_flag} 1 {outer_end_x} {outer_end_y} '
        'L {inner_begin_x},{inner_begin_y} '
        'A {radius_inner} {radius_inner} 0 {large_arc_flag} 0 {inner_end_x} {inner_end_y} '
        'Z" fill="{colour}" {attributes}></path>'
    )

    def __init__(self, colour, start_theta, end_theta, radius_inner, radius_outer, centre_x, centre_y, styles=None, classes=None):
        super().__init__(x_position=centre_x, y_position=centre_y, styles=styles, classes=classes)
        self.start_theta = start_theta
        self.end_theta = end_theta
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.radius_inner = radius_inner
        self.radius_outer = radius_outer
        self.colour = colour

    @property
    def start_theta_rad(self):
        return math.radians(self.start_theta)

    @property
    def end_theta_rad(self):
        return math.radians(self.end_theta)

    @property
    def inner_begin_x(self):
        return self.position.x + self.radius_inner * math.cos(self.end_theta_rad)

    @property
    def inner_end_x(self):
        return self.position.x + self.radius_inner * math.cos(self.start_theta_rad)

    @property
    def inner_begin_y(self):
        return self.position.y + self.radius_inner * math.sin(self.end_theta_rad)

    @property
    def inner_end_y(self):
        return self.position.y + self.radius_inner * math.sin(self.start_theta_rad)

    @property
    def outer_begin_x(self):
        return self.position.x + self.radius_outer * math.cos(self.start_theta_rad)

    @property
    def outer_end_x(self):
        return self.position.x + self.radius_outer * math.cos(self.end_theta_rad)

    @property
    def outer_begin_y(self):
        return self.position.y + self.radius_outer * math.sin(self.start_theta_rad)

    @property
    def outer_end_y(self):
        return self.position.y + self.radius_outer * math.sin(self.end_theta_rad)

    @property
    def large_arc_flag(self):
        return 1 if (self.end_theta - self.start_theta) > 180 else 0

    def get_element_list(self):
        return [
            self.path_template.format(
                outer_begin_x=self.outer_begin_x,
                outer_begin_y=self.outer_begin_y,
                radius_inner=self.radius_inner,
                radius_outer=self.radius_outer,
                large_arc_flag=self.large_arc_flag,
                outer_end_x=self.outer_end_x,
                outer_end_y=self.outer_end_y,
                inner_end_x=self.inner_end_x,
                inner_end_y=self.inner_end_y,
                inner_begin_x=self.inner_begin_x,
                inner_begin_y=self.inner_begin_y,
                colour=self.colour,
                attributes=self.attributes
            )
        ] + collapse_element_list(self.custom_elements)


class LineSeries(Series):
    """
    line series given as a number of (x, y)-points
    """
    __default_styles__ = {'stroke-width': '2'}
    path_begin_template = '<path d="{path}" fill="none" {attributes}/>'

    def __init__(self, points, x_values, y_values, styles=None, classes=None):
        super().__init__(x_position=points[0].x, y_position=points[0].y, styles=styles, classes=classes)
        self.points = points
        self.x_values = x_values
        self.y_values = y_values

    @property
    def pv_generator(self):
        return zip(self.points, self.x_values, self.y_values)

    @property
    def path_length(self):
        return sum(math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) for p1, p2 in zip(self.points, self.points[1:])) if len(self.points) > 2 else 0

    def get_element_list(self):
        path = ' '.join(['{0} {1} {2}'.format("L" if i else "M", p.x, p.y) for i, p in enumerate(self.points)])
        return [self.path_begin_template.format(path=path, attributes=self.attributes)] + collapse_element_list(self.custom_elements)


class BarSeries(Series):

    bar_template = '<rect x="{x}" y="{y}" width="{w}" height="{h}" {attributes}/>'
    __default_styles__ = {'stroke': 'none'}

    def __init__(self, points, x_values, y_values, bar_width, bar_heights, styles=None, classes=None):
        super().__init__(x_position=points[0].x, y_position=points[0].y, styles=styles, classes=classes)
        self.points = points
        self.x_values = x_values
        self.y_values = y_values
        self.bar_width = bar_width
        self.bar_heights = bar_heights

    @property
    def pv_generator(self):
        return zip(self.points, self.x_values, self.y_values)

    def get_element_list(self):
        bars = [self.bar_template.format(x=p.x - self.bar_width/2, y=p.y, w=self.bar_width, h=h, attributes=self.attributes) for p, h in zip(self.points,self.bar_heights)]
        return bars + collapse_element_list(self.custom_elements)
