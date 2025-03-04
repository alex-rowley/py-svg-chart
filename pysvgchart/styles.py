all_styles = {
    ".psc-hover-group .psc-hover-data":
        {
            "display": "none;"
        },
    ".psc-hover-group:hover .psc-hover-data":
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
