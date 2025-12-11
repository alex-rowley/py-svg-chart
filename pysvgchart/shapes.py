"""
Low-level SVG shape primitives.

These are the building blocks for all chart elements. Each shape knows how to
render itself as SVG markup via get_element_list().

Classes:
    Point: 2D coordinate dataclass (x, y)
    Element: Abstract base class with styles and CSS classes
    Shape: Abstract positioned element (has position: Point)
    Line: SVG <line> element
    Circle: SVG <circle> element
    Rect: SVG <rect> element
    Text: SVG <text> element
    Group: SVG <g> container for multiple elements

Common patterns:
    - All shapes have styles (dict of SVG attributes) and classes (CSS class names)
    - attributes property formats styles/classes for SVG attribute string
    - Shapes can be added to charts via chart.add_custom_element(shape)

Example:
    text = Text(x=100, y=50, content='Label', styles={'fill': 'red'})
    circle = Circle(x=200, y=100, radius=5, classes=['highlight'])
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .helpers import collapse_element_list
from .shared import number, style_def


@dataclass
class Point:
    """
    point in 2D space
    """

    x: number
    y: number


class Element(ABC):
    """
    abstract base class for all visual elements
    """

    __default_classes__: list[str] = []
    __default_styles__: style_def = {}

    def __init__(
        self,
        styles: style_def | None = None,
        classes: list[str] | None = None,
    ):
        self.styles = self.__default_styles__.copy() if styles is None else styles
        self.classes = self.__default_classes__.copy() if classes is None else classes

    @property
    def attributes(self) -> str:
        attributes = (
            {
                **self.styles,
                "class": " ".join(self.classes),
            }
            if len(self.classes) > 0
            else self.styles
        )
        return " ".join([a + '="' + attributes[a] + '"' for a in attributes])

    def add_classes(self, classes: list[str]) -> None:
        self.classes.extend(classes)

    @abstractmethod
    def get_element_list(self) -> list: ...


class Shape(Element):
    """
    abstract base class for all shapes
    """

    def __init__(
        self,
        x: number,
        y: number,
        styles: style_def | None = None,
        classes: list[str] | None = None,
    ):
        super().__init__(styles, classes)
        self.position = Point(x=x, y=y)

    @abstractmethod
    def get_element_list(self) -> list: ...


class Line(Shape):
    """
    straight line between two points
    """

    line_template = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {attributes}/>'

    def __init__(
        self,
        x: number,
        y: number,
        *,
        width: number | None = None,
        height: number | None = None,
        x2: number | None = None,
        y2: number | None = None,
        styles: style_def | None = None,
        classes: list[str] | None = None,
    ):
        if width is None and height is None and x2 is not None and y2 is not None:
            pass
        elif width is not None and height is not None and x2 is None and y2 is None:
            x2 = x + width
            y2 = y + height
        else:
            raise ValueError("use either width and height, or x2 and y2")
        super().__init__(x, y, styles, classes)
        self.end = Point(x2, y2)
        self.styles = dict() if styles is None else styles

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} start={self.position} end={self.end}>"

    @property
    def start(self) -> Point:
        return self.position

    def get_element_list(self) -> list:
        return [
            self.line_template.format(
                x1=self.start.x,
                y1=self.start.y,
                x2=self.end.x,
                y2=self.end.y,
                attributes=self.attributes,
            ),
        ]


class Circle(Shape):
    """
    circle around a center point
    """

    circle_template = '<circle cx="{x}" cy="{y}" r="{r}" {attributes}/>'

    def __init__(
        self,
        x: number,
        y: number,
        *,
        radius: number | None = None,
        styles: style_def | None = None,
        classes: list[str] | None = None,
    ):
        super().__init__(x, y, styles, classes)
        self.radius = radius

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} c={self.position} r={self.radius}>"

    def get_element_list(self) -> list[str]:
        return [
            self.circle_template.format(
                x=self.position.x,
                y=self.position.y,
                r=self.radius,
                attributes=self.attributes,
            ),
        ]


class Rect(Shape):
    """
    rectangle at a position with dimensions
    """

    rect_template = '<rect x="{x}" y="{y}" width="{width}" height="{height}" {attributes}/>'

    def __init__(
        self,
        x: number,
        y: number,
        *,
        width: number | None = None,
        height: number | None = None,
        x2: number | None = None,
        y2: number | None = None,
        styles: style_def | None = None,
        classes: list[str] | None = None,
    ):
        if width is not None and height is not None and x2 is None and y2 is None:
            pass
        elif width is None and height is None and x2 is not None and y2 is not None:
            width = max(x, x2) - min(x, x2)
            height = max(y, y2) - min(y, y2)
        else:
            raise ValueError("use either width and height, or x2 and y2")
        super().__init__(x, y, styles, classes)
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} pos={self.position} w={self.width} h={self.height}>"

    def get_element_list(self) -> list[str]:
        return [
            self.rect_template.format(
                x=self.position.x,
                y=self.position.y,
                width=self.width,
                height=self.height,
                attributes=self.attributes,
            ),
        ]


class Text(Shape):
    """
    text at a position
    """

    text_template = '<text x="{x}" y="{y}" {attributes}>{content}</text>'

    def __init__(self, x, y, content, styles=None, classes=None):
        super().__init__(x, y, styles, classes)
        self.content = content

    def __repr__(self):
        return f"<{self.__class__.__name__} pos={self.position} content={self.content} styles={self.styles}>"

    def get_element_list(self) -> list:
        return [
            self.text_template.format(
                x=self.position.x,
                y=self.position.y,
                content=self.content,
                attributes=self.attributes,
            ),
        ]


class Group(Element):
    """
    a group of visual elements
    """

    group_template = "<g {attributes}>"

    def __init__(
        self,
        styles=None,
        classes=None,
        children: list[Element] | None = None,
    ):
        super().__init__(styles, classes)
        self.children = [] if children is None else children

    def __repr__(self):
        return f"<{self.__class__.__name__} children={self.children}>"

    def add_children(self, children):
        self.children.extend(children)

    def get_element_list(self) -> list:
        return (
            [self.group_template.format(attributes=self.attributes)]
            + collapse_element_list(self.children)
            + ["</g>"]
        )
