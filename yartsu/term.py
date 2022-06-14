import shutil
from typing import Any

from rich import box
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.table import Table as RichTable
from rich.theme import Theme

MAX_WIDTH = 120


class Table(RichTable):
    def __init__(self, box: box.Box = box.ROUNDED, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.box = box


class ErrorHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an error."""

    highlights = [r"(?P<error>\[\w+Error\])"]


theme = Theme({"header": "bold cyan", "option": "yellow", "metavar": "green"})


class Term:
    def __init__(self, width: int) -> None:

        self.console = Console(highlight=False, theme=theme, width=width)
        self.err_console = Console(
            theme=Theme({"error": "bold red"}, inherit=True),
            stderr=True,
            highlighter=ErrorHighlighter(),
            width=width,
        )

    def print(self, *objects: Any, err: bool = False, **kwargs: Any) -> None:
        console = self.console if not err else self.err_console
        console.print(*objects, **kwargs)

    def stylize(self, *objects: Any, **kwargs: Any) -> str:
        with self.console.capture() as capture:
            self.print(*objects, **kwargs, end="")
        return capture.get()

    def debug(self, renderable: Any, **kwargs: Any) -> None:
        self.console.print("[dim]>>debug[/]:\n", renderable, **kwargs)


cols = shutil.get_terminal_size().columns
term = Term(width=MAX_WIDTH if cols > MAX_WIDTH else cols)
