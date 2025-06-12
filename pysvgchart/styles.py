
hover_style_name = "psc-hover-data"

default_styles = {
    f".psc-hover-group .{hover_style_name}": {
        "display": "none",
    },
    f".psc-hover-group:hover .{hover_style_name}": {
        "display": "inline",
    },
}


def render_style_dict(style_dict: dict) -> str:
    indent = " " * 4
    return f"""
{{
{indent}{f"\n{indent}".join(f"{param}: {value};" for param, value in style_dict.items())}
}}
    """.strip()


def optionally_merge_styles_to_default(styles, include_default):
    return {**styles, **default_styles} if include_default else styles


def render_all_styles(styles=None, include_default=True):
    rendered_styles = (
        default_styles.copy()
        if styles is None
        else optionally_merge_styles_to_default(styles, include_default)
    )
    return "\n".join(
        [f"{name} {render_style_dict(rendered_styles[name])}\n" for name in rendered_styles]
    )[:-1]
