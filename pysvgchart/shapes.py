from .helpers import collapse_element_list


class Point:

    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position


class Element:
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

    def get_element_list(self):
        raise NotImplementedError("Not implemented in base class.")


class Shape(Element):

    def __init__(self, x_position, y_position, styles=None, classes=None):
        super().__init__(styles, classes)
        self.position = Point(x_position, y_position)


class Line(Shape):
    line_template = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {attributes}/>'

    def __init__(self, x_position, y_position, width, height, styles=None, classes=None):
        super().__init__(x_position, y_position, styles, classes)
        self.end = Point(x_position + width, y_position + height)
        self.styles = dict() if styles is None else styles

    @property
    def start(self):
        return self.position

    def get_element_list(self):
        return [self.line_template.format(x1=self.start.x, y1=self.start.y, x2=self.end.x, y2=self.end.y, attributes=self.attributes)]


class Circle(Shape):
    circle_template = '<circle cx="{x}" cy="{y}" r="{r}" {attributes}/>'

    def __init__(self, x_position, y_position, radius, styles=None, classes=None):
        super().__init__(x_position, y_position, styles, classes)
        self.radius = radius

    def get_element_list(self):
        return [self.circle_template.format(x=self.position.x, y=self.position.y, r=self.radius, attributes=self.attributes)]


class Rect(Shape):
    rect_template = '<rect x="{x}" y="{y}" width="{width}" height="{height}" {attributes}/>'

    def __init__(self, x_position, y_position, width, height, styles=None, classes=None):
        super().__init__(x_position, y_position, styles, classes)
        self.width = width
        self.height = height

    def get_element_list(self):
        return [self.rect_template.format(
            x=self.position.x,
            y=self.position.y,
            width=self.width,
            height=self.height,
            attributes=self.attributes
        )]


class Text(Shape):
    text_template = '<text x="{x}" y="{y}" {attributes}>{content}</text>'

    def __init__(self, x_position, y_position, content, styles=None, classes=None):
        super().__init__(x_position, y_position, styles, classes)
        self.styles = dict() if styles is None else styles
        self.content = content

    def get_element_list(self):
        return [self.text_template.format(x=self.position.x, y=self.position.y, content=self.content, attributes=self.attributes)]


class Group(Element):
    group_template = '<g {attributes}>'

    def __init__(self, styles=None, classes=None, children=None):
        super().__init__(styles, classes)
        self.children = [] if children is None else children

    def add_children(self, children):
        self.children.extend(children)

    def get_element_list(self):
        return [self.group_template.format(attributes=self.attributes)] + collapse_element_list(self.children) + ['</g>']
