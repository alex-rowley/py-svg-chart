hover_style_name = "psc-hover-data"

all_styles = {
    f".psc-hover-group .{hover_style_name}":
        {
            "display": "none;"
        },
    f".psc-hover-group:hover .{hover_style_name}":
        {
            "display": "inline"
        }
}


def join_indent(values):
    return '\n'.join(['     ' + v for v in values])


def render_all_styles(styles=None):
    styles = all_styles if styles is None else styles
    return '\n'.join([
        '\n'.join([name + ' {', join_indent(s + ': ' + str(styles[name][s]) + ';' for s in styles[name]), '}\n'])
        for name in styles
    ])[:-1]
