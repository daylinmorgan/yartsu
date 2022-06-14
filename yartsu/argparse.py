import sys
from argparse import ONE_OR_MORE, SUPPRESS, ZERO_OR_MORE, Action
from argparse import ArgumentParser as StdArgParser
from argparse import HelpFormatter as StdHelpFormatter
from typing import Any, NoReturn, Tuple, Union

from rich.text import Text

from .term import term


class CustomFormatter(StdHelpFormatter):
    def _format_action_invocation(self, action: Action) -> str:
        if not action.option_strings:
            (metavar,) = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            # parts will be iterable of Text objects
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(
                    [Text(option, style="option") for option in action.option_strings]
                )

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            # change to
            #    -s, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                parts.extend(
                    [Text(option, style="option") for option in action.option_strings]
                )
                # add metavar to last string
                parts[-1].append_text(Text(f" {args_string}", style="metavar"))
            return term.stylize(Text(", ").join(parts))

    # from argparse.RawDescriptionHelpFormatter
    def _fill_text(self, text: str, width: int, indent: str) -> str:
        return term.stylize(
            Text("").join(
                Text.from_markup(indent + line)
                for line in text.splitlines(keepends=True)
            )
        )

    def start_section(self, heading: str) -> None:  # type: ignore
        return super().start_section(term.stylize(heading, style="header"))

    def _format_action(self, action: Action) -> str:
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)
        action_header_len = Text.from_ansi(action_header).cell_len

        tup: Union[Tuple[int, str, int, str], Tuple[int, str, str]]

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup

        # short action name; start on the same line and pad two spaces
        elif action_header_len <= action_width:
            tup = self._current_indent, "", action_width, action_header
            action_header = f"{' '*self._current_indent}{action_header}{' '*(action_width+2 - action_header_len)}"
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help and action.help.strip():
            help_text = self._expand_help(action)
            if help_text:
                help_lines = self._split_lines(help_text, help_width)
                parts.append("%*s%s\n" % (indent_first, "", help_lines[0]))
                for line in help_lines[1:]:
                    parts.append("%*s%s\n" % (help_position, "", line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith("\n"):
            parts.append("\n")

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)

    def _get_invocation_length(self, invocation: Any) -> int:
        return Text.from_ansi(invocation).cell_len

    def _format_args(self, action: Action, default_metavar: str) -> str:
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs == ZERO_OR_MORE:
            return "[%s ...]" % get_metavar(1)
        elif action.nargs == ONE_OR_MORE:
            return "%s ..." % get_metavar(1)
        else:
            return super()._format_args(action, default_metavar)

    def add_argument(self, action: Action) -> None:
        if action.help is not SUPPRESS:

            # find all invocations
            get_invocation = self._format_action_invocation
            invocations = [get_invocation(action)]
            for subaction in self._iter_indented_subactions(action):
                invocations.append(get_invocation(subaction))

            # update the maximum item length accounting for ansi codes from rich
            invocation_length = max(map(self._get_invocation_length, invocations))
            action_length = invocation_length + self._current_indent
            self._action_max_length = max(self._action_max_length, action_length)

            # add the item to the list
            self._add_item(self._format_action, [action])


class ArgumentParser(StdArgParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.formatter_class = CustomFormatter

    def error(self, message: str) -> NoReturn:
        """error(message: string)
        Prints a usage message incorporating the message to stderr and
        exits.
        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        term.print(f"[YartsuCLIError]({self.prog.strip()}): {message}", err=True)
        sys.exit(1)
