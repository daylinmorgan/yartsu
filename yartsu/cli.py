import os
import sys
import textwrap
from argparse import SUPPRESS, FileType, Namespace
from pathlib import Path

from rich.__main__ import make_test_card
from rich.console import Console
from rich.text import Text

from ._export_format import CONSOLE_SVG_FORMAT
from ._run_cmd import run_cmd
from ._version import __version__
from .argparse import ArgumentParser
from .term import term
from .themes import THEMES

DEFAULT_THEME = os.getenv("YARTSU_THEME", "cat-mocha")


def get_args() -> Namespace:

    parser = ArgumentParser(
        usage=SUPPRESS,
        description=textwrap.dedent(
            r"""
        [bold italic cyan]usage[/]:

            ls --color=always | yartsu \[options]
            [dim]OR[/]
            yartsu \[options] -- ls --color
            [dim]OR[/]
            ls --color=always > ls.txt; yartsu -i ls.txt

        convert terminal output to svg
        """
        ),
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-i",
        "--input",
        help="input file [default: stdin]",
        type=FileType("r"),
        default=(None if sys.stdin.isatty() else sys.stdin),
    )
    parser.add_argument("cmd", type=str, nargs="*", default="", help=SUPPRESS)
    parser.add_argument(
        "-o",
        "--output",
        help="output svg file [default: %(default)s]",
        type=Path,
        default=Path("capture.svg"),
    )
    parser.add_argument("-t", "--title", help="title for terminal window", type=str)
    parser.add_argument("-w", "--width", help="width of svg", type=int)
    parser.add_argument(
        "--theme",
        help="theme to use for highlighting [default: %(default)s]",
        type=str,
        default=DEFAULT_THEME,
    )
    parser.add_argument(
        "--list-themes", help="list available themes", action="store_true"
    )
    parser.add_argument("--demo", help=SUPPRESS, action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_args()
    console = Console(record=True)

    if args.list_themes:
        term.print("Available themes:")
        term.print("\n".join(["  - " + theme for theme in THEMES]))
        sys.exit(0)

    if args.cmd and args.input or not (args.cmd or args.input or args.demo):
        term.print(
            "[UsageError]: either use the --input option "
            "OR pipe terminal output to yartsu",
            err=True,
        )
        term.print("See 'yartsu --help' for more information", err=True)
        sys.exit(1)

    if args.theme not in THEMES:
        term.print(f"[ThemeError]: {args.theme} is not a valid theme", err=True)
        sys.exit(1)

    if args.cmd:
        cmd = " ".join(args.cmd)

        try:
            returncode, captured_output = run_cmd(cmd)
        except FileNotFoundError:
            term.print(f"[CmdError]: issue running {cmd}", err=True)
            sys.exit(1)

        if returncode != 0:
            term.print(f"[CmdError]: issue running {cmd}", err=True)
            sys.exit(returncode)

        parsed_input = Text.from_ansi(captured_output)
    else:
        cmd = None

    if args.input:
        parsed_input = Text.from_ansi(args.input.read())

    elif args.demo:
        parsed_input = make_test_card()

    title = args.title or cmd or "yartsu"

    if args.width:
        console.width = args.width
    elif args.demo:
        console.width = 120
    else:
        console.width = max(console.measure(parsed_input).maximum, 40)

    console.print(parsed_input)

    console.save_svg(
        args.output,
        title=title,
        theme=THEMES[args.theme],
        code_format=CONSOLE_SVG_FORMAT,
    )

    term.print(f"\nSaved to {args.output}.")
