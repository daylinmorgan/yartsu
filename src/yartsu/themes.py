import json
import sys
from importlib.resources import files

from rich.color import parse_rgb_hex
from rich.terminal_theme import (
    DIMMED_MONOKAI,
    MONOKAI,
    NIGHT_OWLISH,
    SVG_EXPORT_THEME,
    TerminalTheme,
)

from .term import term


def get_builtin_themes():
    return (
        resource.name.split(".")[0]
        for resource in (files("yartsu") / "themes").iterdir()
        if resource.is_file()
    )


def load_theme(name: str) -> TerminalTheme:
    theme_file = files("yartsu") / "themes" / f"{name}.json"
    with theme_file.open("r") as f:
        theme_json = json.load(f)

    try:
        format = theme_json["format"]

        if format == "rgb":
            background = theme_json["background"]
            foreground = theme_json["foreground"]
            colors = theme_json["colors"]
            if "bright_colors" in theme_json:
                bright_colors = theme_json["bright_colors"]
            else:
                bright_colors = colors

        elif format == "hex":
            background = parse_rgb_hex(theme_json["background"])
            foreground = parse_rgb_hex(theme_json["foreground"])
            colors = [parse_rgb_hex(c) for c in theme_json["colors"]]
            if "bright_colors" in theme_json:
                bright_colors = [parse_rgb_hex(c) for c in theme_json["bright_colors"]]
            else:
                bright_colors = colors
        else:
            print("[ThemeError]: unknown color format type {color_fmt}")

        theme = TerminalTheme(background, foreground, colors, bright_colors)
    except KeyError as e:
        term.print(
            f"[ThemeError]: error loading {name} theme. "
            f"Couldn't load {e} from theme json.",
            err=True,
        )
        sys.exit(1)

    return theme


THEMES = {
    # **{
    #     theme.name: TerminalTheme(
    #         theme.background,
    #         theme.foreground,
    #         theme.colors,
    #         theme.bright_colors,
    #     )
    #     for theme in THEME_DEFINITIONS
    #
    # },
    **{name: load_theme(name) for name in get_builtin_themes()},
    **{
        "monokai": MONOKAI,
        "dimmed_monokai": DIMMED_MONOKAI,
        "night-owlish": NIGHT_OWLISH,
        "rich-default": SVG_EXPORT_THEME,
    },
}
