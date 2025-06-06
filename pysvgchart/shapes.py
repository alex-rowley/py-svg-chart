from abc import ABC, abstractmethod
from dataclasses import dataclass

from .helpers import collapse_element_list


@dataclass
class Point:
    """
    point in 2D space
    """
    x: float | int
    y: float | int


class Element(ABC):
    """
    abstract base class for all visual elements
    """
    __default_classes__ = []
    __default_styles__ = dict()

    def __init__(self, styles=None, classes=None):
        self.styles = self.__default_styles__.copy() if styles is None else styles
        self.classes = self.__default_classes__.copy() if classes is None else classes

    @property
    def attributes(self):
        attributes = {**self.styles, 'class': ' '.join(self.classes)} if len(self.classes) > 0 else self.styles
        return " ".join([a + '="' + attributes[a] + '"' for a in attributes])

    def add_classes(self, classes):
        self.classes.extend(classes)

    @abstractmethod
    def get_element_list(self):
        ...


class Shape(Element):
    """
    abstract base class for all shapes
    """

    def __init__(self, x, y, styles=None, classes=None):
        super().__init__(styles, classes)
        self.position = Point(x=x, y=y)


class Line(Shape):
    """
    straight line between two points
    """
    line_template = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {attributes}/>'

    def __init__(self, x, y, width, height, styles=None, classes=None):
        super().__init__(x, y, styles, classes)
        self.end = Point(x + width, y + height)
        self.styles = dict() if styles is None else styles

    def __repr__(self):
        return f"<{self.__class__.__name__} start={self.position} end={self.end}>"

    @property
    def start(self):
        return self.position

    def get_element_list(self):
        return [self.line_template.format(x1=self.start.x, y1=self.start.y, x2=self.end.x, y2=self.end.y, attributes=self.attributes)]


class Circle(Shape):
    """
    circle around a center point
    """
    circle_template = '<circle cx="{x}" cy="{y}" r="{r}" {attributes}/>'

    def __init__(self, x, y, radius, styles=None, classes=None):
        super().__init__(x, y, styles, classes)
        self.radius = radius

    def __repr__(self):
        return f"<{self.__class__.__name__} c={self.position} r={self.radius}>"

    def get_element_list(self):
        return [self.circle_template.format(x=self.position.x, y=self.position.y, r=self.radius, attributes=self.attributes)]


class Rect(Shape):
    """
    rectangle at a position with dimensions
    """
    rect_template = '<rect x="{x}" y="{y}" width="{width}" height="{height}" {attributes}/>'

    def __init__(self, x, y, width, height, styles=None, classes=None):
        super().__init__(x, y, styles, classes)
        self.width = width
        self.height = height

    def __repr__(self):
        return f"<{self.__class__.__name__} pos={self.position} w={self.width} h={self.height}>"

    def get_element_list(self):
        return [self.rect_template.format(
            x=self.position.x,
            y=self.position.y,
            width=self.width,
            height=self.height,
            attributes=self.attributes
        )]


class Text(Shape):
    """
    text at a position
    """
    text_template = '<text x="{x}" y="{y}" {attributes}>{content}</text>'

    def __init__(self, x, y, content, styles=None, classes=None):
        super().__init__(x, y, styles, classes)
        self.styles = dict() if styles is None else styles
        self.content = content

    def __repr__(self):
        return f"<{self.__class__.__name__} pos={self.position} content={self.content} styles={self.styles}>"

    def get_element_list(self):
        return [self.text_template.format(x=self.position.x, y=self.position.y, content=self.content, attributes=self.attributes)]


class Group(Element):
    """
    a group of visual elements
    """
    group_template = '<g {attributes}>'

    def __init__(self, styles=None, classes=None, children=None):
        super().__init__(styles, classes)
        self.children = [] if children is None else children

    def __repr__(self):
        return f"<{self.__class__.__name__} children={self.children}>"

    def add_children(self, children):
        self.children.extend(children)

    def get_element_list(self):
        return [self.group_template.format(attributes=self.attributes)] + collapse_element_list(self.children) + ['</g>']
