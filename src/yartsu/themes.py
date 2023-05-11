import json
import os
import sys
from importlib.resources import files

from rich import box
from rich.color import parse_rgb_hex
from rich.table import Table
from rich.terminal_theme import (
    DIMMED_MONOKAI,
    MONOKAI,
    NIGHT_OWLISH,
    SVG_EXPORT_THEME,
    TerminalTheme,
)

from .term import term


class YartsuTheme(TerminalTheme):
    def __init__(self, *args, src: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.src = src

    @classmethod
    def load_theme(cls, name: str, src: str):
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
                    bright_colors = [
                        parse_rgb_hex(c) for c in theme_json["bright_colors"]
                    ]
                else:
                    bright_colors = colors
            else:
                print("[ThemeError]: unknown color format type {color_fmt}")

        except KeyError as e:
            term.print(
                f"[ThemeError]: error loading {name} theme. "
                f"Couldn't load {e} from theme json.",
                err=True,
            )
            sys.exit(1)

        return cls(background, foreground, colors, bright_colors, src=src)


class ThemeDB:
    def __init__(self):
        self.default = os.getenv("YARTSU_THEME", "cat-mocha")
        self.selected = self.default
        self.themes = {
            **self._load_yartsu_themes(),
            **{
                "dimmed_monokai": DIMMED_MONOKAI,
                "monokai": MONOKAI,
                "night-owlish": NIGHT_OWLISH,
                "rich-default": SVG_EXPORT_THEME,
            },
        }

    def _load_yartsu_themes(self):
        return {
            name: YartsuTheme.load_theme(name, src="yartsu")
            for name in sorted(
                resource.name.split(".")[0]
                for resource in (files("yartsu") / "themes").iterdir()
                if resource.is_file()
            )
        }

    def list(self):
        table = Table(title="Available Themes", box=box.MINIMAL)
        table.add_column("name")
        table.add_column("source")

        for name, theme in self.themes.items():
            source = theme.src if isinstance(theme, YartsuTheme) else "rich"
            table.add_row(name, source)

        term.print(table)
