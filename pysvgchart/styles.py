"""
styles - constants and functions for CSS styles
"""

from .shared import named_styles, style_def

hover_style_name = "psc-hover-data"

default_styles = {
    f".psc-hover-group .{hover_style_name}": {
        "display": "none",
    },
    f".psc-hover-group:hover .{hover_style_name}": {
        "display": "inline",
    },
}


def render_style_dict(style_dict: style_def) -> str:
    indent = " " * 4
    nl = "\n"
    return f"""
{{
{indent}{f"{nl}{indent}".join(f"{param}: {value};" for param, value in style_dict.items())}
}}
    """.strip()


def optionally_merge_styles_to_default(
    styles: named_styles | None = None,
    include_default: bool = True,
) -> named_styles:
    if styles is None:
        return {**default_styles} if include_default else {}
    return {**styles, **default_styles} if include_default else {**styles}


def render_all_styles(
    styles: named_styles | None = None,
    include_default: bool = True,
) -> str:
    rendered_styles = (
        default_styles.copy()
        if styles is None
        else optionally_merge_styles_to_default(styles, include_default)
    )
    return "\n".join(
        [f"{name} {render_style_dict(rendered_styles[name])}\n" for name in rendered_styles]  # type: ignore[operator]
    )[:-1]
