from collections import namedtuple

from rich.terminal_theme import (
    DIMMED_MONOKAI,
    MONOKAI,
    NIGHT_OWLISH,
    SVG_EXPORT_THEME,
    TerminalTheme,
)

Colors = namedtuple("Colors", "black, red, green, yellow, blue, magenta, cyan, white")
Theme = namedtuple("Theme", "background, foreground, colors, bright_colors")

cat_mocha = Theme(
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
)
CAT_MOCHA = TerminalTheme(
    cat_mocha.background,
    cat_mocha.foreground,
    cat_mocha.colors,
    cat_mocha.bright_colors,
)
cat_frappe = Theme(
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
)
CAT_FRAPPE = TerminalTheme(
    cat_frappe.background,
    cat_frappe.foreground,
    cat_frappe.colors,
    cat_frappe.bright_colors,
)
cat_macchiato = Theme(
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
)
CAT_MACCHIATO = TerminalTheme(
    cat_macchiato.background,
    cat_macchiato.foreground,
    cat_macchiato.colors,
    cat_macchiato.bright_colors,
)
cat_latte = Theme(
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
)
CAT_LATTE = TerminalTheme(
    cat_latte.background,
    cat_latte.foreground,
    cat_latte.colors,
    cat_latte.bright_colors,
)

THEMES = {
    "cat_mocha": CAT_MOCHA,
    "cat_frappe": CAT_FRAPPE,
    "cat_macchiato": CAT_MACCHIATO,
    "cat_latte": CAT_LATTE,
    "monokai": MONOKAI,
    "dimmed_monokai": DIMMED_MONOKAI,
    "night_owlish": NIGHT_OWLISH,
    "rich_default": SVG_EXPORT_THEME,
}
