import io
import platform
import sys
import textwrap
from argparse import SUPPRESS, FileType
from pathlib import Path

from rich.__main__ import make_test_card
from rich.text import Text

from ._argparse import ArgumentParser
from ._export_format import CONSOLE_SVG_FORMAT
from ._version import __version__
from .console import Console
from .term import term
from .theme import ThemeDB

themes = ThemeDB()


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        usage=SUPPRESS,
        description=textwrap.dedent(
            r"""
        [header]usage[/]:

        three ways to convert terminal output to svg:
            1: `ls --color=always | yartsu \[options]`
            2: `yartsu \[options] -- ls --color`
            3: `ls --color=always > ls.txt; yartsu -i ls.txt`
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
        default=themes.default,
    )
    parser.add_argument(
        "--list-themes", help="list available themes", action="store_true"
    )
    parser.add_argument("--demo", help=SUPPRESS, action="store_true")
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    console = Console(record=True, force_terminal=True)

    if args.list_themes:
        themes.list()
        sys.exit(0)

    if args.cmd and args.input or not (args.cmd or args.input or args.demo):
        term.print(
            "[UsageError]: either use the --input option "
            "OR pipe terminal output to yartsu",
            err=True,
        )
        term.print("See below for more information:\n")
        parser.print_help()
        sys.exit(1)

    # TODO: move this error somewhere else
    if args.theme not in themes.themes:
        term.print(f"[ThemeError]: {args.theme} is not a valid theme", err=True)
        sys.exit(1)

    if args.demo:
        console = Console(
            file=io.StringIO(),
            record=True,
            force_terminal=True,
            color_system="truecolor",
            legacy_windows=False,
        )
        parsed_input = make_test_card()  # type: ignore

    elif args.cmd:
        cmd = " ".join(args.cmd)
        if platform.system() == "windows":
            term.print("[CmdError]: cmd mode is not supported on Windows", err=True)
            sys.exit(1)
        from ._run_cmd import run_cmd

        try:
            returncode, captured_output = run_cmd(cmd)
        except FileNotFoundError:
            term.print(f"[CmdError]: issue running {cmd}", err=True)
            sys.exit(1)

        if returncode != 0:
            term.print(f"[CmdError]: issue running {cmd}", err=True)
            sys.exit(returncode)

        parsed_input = Text.from_ansi(captured_output)

    elif args.input:
        cmd = None
        parsed_input = Text.from_ansi(args.input.read())

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
        theme=themes.themes[args.theme],
        code_format=CONSOLE_SVG_FORMAT,
    )

    term.print(f"\nSaved to {args.output}.")
