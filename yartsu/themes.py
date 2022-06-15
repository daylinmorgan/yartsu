from collections import namedtuple

from rich.color import parse_rgb_hex
from rich.terminal_theme import (
    DIMMED_MONOKAI,
    MONOKAI,
    NIGHT_OWLISH,
    SVG_EXPORT_THEME,
    TerminalTheme,
)

Colors = namedtuple("Colors", "black, red, green, yellow, blue, magenta, cyan, white")
Theme = namedtuple("Theme", "name background, foreground, colors, bright_colors")

THEME_DEFINITIONS = [
    Theme(
        name="cat-mocha",
        background=(30, 30, 46),
        foreground=(198, 208, 245),
        colors=Colors(
            black=(179, 188, 223),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(86, 89, 112),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
        bright_colors=Colors(
            black=(161, 168, 201),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(67, 70, 90),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
    ),
    Theme(
        name="cat-frappe",
        background=(48, 52, 70),
        foreground=(198, 206, 239),
        colors=Colors(
            black=(179, 188, 223),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(86, 89, 112),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
        bright_colors=Colors(
            black=(161, 168, 201),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(67, 70, 90),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
    ),
    Theme(
        name="cat-macchiato",
        background=(36, 39, 58),
        foreground=(197, 207, 245),
        colors=Colors(
            black=(179, 188, 223),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(86, 89, 112),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
        bright_colors=Colors(
            black=(161, 168, 201),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(67, 70, 90),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
    ),
    Theme(
        name="cat-latte",
        background=(239, 241, 245),
        foreground=(76, 79, 105),
        colors=Colors(
            black=(179, 188, 223),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(86, 89, 112),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
        bright_colors=Colors(
            black=(161, 168, 201),
            cyan=(148, 226, 213),
            yellow=(249, 226, 175),
            blue=(135, 176, 249),
            red=(243, 139, 168),
            white=(67, 70, 90),
            green=(166, 227, 161),
            magenta=(245, 194, 231),
        ),
    ),
    Theme(
        name="dracula",
        background=parse_rgb_hex("282a36"),
        foreground=parse_rgb_hex("f8f8f2"),
        colors=Colors(
            black=parse_rgb_hex("21222c"),
            cyan=parse_rgb_hex("8be9fd"),
            yellow=parse_rgb_hex("f1fa8c"),
            blue=parse_rgb_hex("bd93f9"),
            red=parse_rgb_hex("ff5555"),
            green=parse_rgb_hex("50fa7b"),
            magenta=parse_rgb_hex("ff79c6"),
            white=parse_rgb_hex("f8f8f2"),
        ),
        bright_colors=Colors(
            black=parse_rgb_hex("6272a4"),
            cyan=parse_rgb_hex("a4ffff"),
            red=parse_rgb_hex("ff6e6e"),
            yellow=parse_rgb_hex("ffffa5"),
            blue=parse_rgb_hex("d6acff"),
            green=parse_rgb_hex("69ff94"),
            magenta=parse_rgb_hex("ff92df"),
            white=parse_rgb_hex("ffffff"),
        ),
    ),
]


THEMES = {
    **{
        theme.name: TerminalTheme(
            theme.background,
            theme.foreground,
            theme.colors,
            theme.bright_colors,
        )
        for theme in THEME_DEFINITIONS
    },
    **{
        "monokai": MONOKAI,
        "dimmed_monokai": DIMMED_MONOKAI,
        "night-owlish": NIGHT_OWLISH,
        "rich-default": SVG_EXPORT_THEME,
    },
}
