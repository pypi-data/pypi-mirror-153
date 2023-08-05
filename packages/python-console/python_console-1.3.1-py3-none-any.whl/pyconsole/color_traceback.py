from __future__ import annotations

import warnings
import linecache
import sys

from collections import namedtuple
from traceback import walk_tb, format_exc
from pathlib import Path
from typing import TextIO, Callable
from types import TracebackType

from .global_data import get_console
from .color import Color, RESET, YELLOW, BRIGHT_WHITE, LIME, GRAY, UNDERLINE
from .color_parser import SIMPLE, RGB
from .table import Box, TitleBox
from .errors import TracebackWarning
from .console import Console


class TraceBack:
    '''
    # TraceBack Class

    The class used for formatting an exception into its colored version.

    You probably don't want to use this class if you want pretty errors and should use
    `install_errors` instead.

    If you do want to use this, then you should probably be doing it through the `from_exception`
    class method.

    In any case, it can be used as follows:

    e.g.
    ```python
      from pyconsole import Console
      from pyconsole.color_traceback import TraceBack


      console = Console()

      try:
          value = 1 / 0
      except ZeroDivisionError:
          traceback = TraceBack()
          console.print(traceback)
    ```
    '''
    def __init__(self, stacks: list = None, show_locals: bool = False, neighbors: int = 3,
                 indent: int = 2, colors:  list[Color] | None = None):
        if stacks is None:
            e_type, e_value, trace = sys.exc_info()

            if e_type is None or e_value is None or trace is None:
                raise ValueError("argument 'stacks' is required")

            stacks = self.extract(e_type, e_value, trace, show_locals=show_locals)

        self.stacks = stacks
        self.show_locals = show_locals
        self.neighbors = neighbors
        self.indent = indent
        self.console = get_console()
        self.colors = colors if colors else self.console.color.color_t["traceback"]

    @classmethod
    def extract(cls, e_type: type[BaseException], e_value: BaseException, trace: TracebackType, *,
                show_locals: bool = False) -> list:
        '''
        The `extract` class method extracts information from the exception for later pretty
        printing.

        ## Traceback Params

        e_type: type[BaseException]

        e_value: BaseException

        trace: TracebackType

        ## Parsing Params

        show_locals: bool = whether to show local variables or not. default is False.
        '''
        stacks = []
        is_cause = False
        Stack = namedtuple("Stack", ["e_type", "e_value", "is_cause", "frame", "syntax_error"])
        Frame = namedtuple("Frame", ["file_name", "line", "name", "locals"])
        SyntaxError_ = namedtuple("SyntaxError_", ["offset", "file_name", "line", "text", "msg"])

        while True:
            stack = Stack(str(e_type.__name__), str(e_value), is_cause, [], None)

            if isinstance(e_value, SyntaxError):
                stack = stack._replace(syntax_error=SyntaxError_(e_value.offset or 0,
                                                                 e_value.filename or "?",
                                                                 e_value.lineno or 0,
                                                                 e_value.text or "",
                                                                 e_value.msg))

            stacks.append(stack)

            for summary, line in walk_tb(trace):
                file_name = summary.f_code.co_filename
                file_name = str(Path(file_name).resolve()) if file_name else "?"
                frame_locals = ({key: value for key, value in summary.f_locals.items()}
                                if show_locals else None)
                frame = Frame(file_name, line, summary.f_code.co_name, frame_locals)
                stack.frame.append(frame)

            cause = getattr(e_value, "__cause__", None)

            if cause and cause.__traceback__:
                e_type = cause.__class__
                e_value = cause
                trace = cause.__traceback__

                if trace:
                    is_cause = True
                    continue

            cause = e_value.__context__

            if cause and cause.__traceback__ and not getattr(e_value, "__supress_context__", False):
                e_type = cause.__class__
                e_value = cause
                trace = cause.__traceback__

                if trace:
                    is_cause = False
                    continue

            break

        return stacks

    @classmethod
    def from_exception(cls, e_type: type[BaseException], e_value: BaseException,
                       trace: TracebackType, *, show_locals: bool = False, neighbors: int = 3,
                       indent: int = 2, colors: list[Color] | None = None):
        '''
        Creates a TraceBack object from the information found in an exception and the optional
        printing parameters.

        If you are using this, then you probably want to use it as follows:

        e.g.
        ```python
          import sys

          from pyconsole import Console
          from pyconsole.color_traceback import TraceBack


          console = Console()

          try:
              value = 1 / 0
          except ZeroDivisionError:
              e_type, e_value, trace = sys.exc_info()
              traceback = TraceBack.from_exception(e_type, e_value, trace)
              console.print(traceback)
        ```

        ## Traceback Params

        e_type: type[BaseException]

        e_value: BaseException

        trace: TracebackType

        ## Parsing Params

        show_locals: bool = whether to show local variables or not. default is False.

        neighbors: int = the amount of neighboring lines to show in addition to the line of the
        error. default is 3.

        indent: int = how much should local variables be indented if they are a container type.
        default is 2.

        colors: list[Color] | None = the list of colors to use for parsing elements. default value
        is None for auto-detection. (refer to `ColorParser` for more info on the colors list).
        '''
        stacks = TraceBack.extract(e_type, e_value, trace, show_locals=show_locals)
        return TraceBack(stacks, show_locals, neighbors, indent, colors)

    def __color__(self) -> str:
        string: str = ""
        files: dict[str, str] = {}

        for idx, stack in enumerate(reversed(self.stacks)):
            total = ""

            for frame in stack.frame:
                total += (f"{self.colors[3]}{frame.file_name}{RESET}:"
                          f"{self.colors[4]}{frame.line}{RESET} in "
                          f"{self.colors[5]}{frame.name}{RESET}\n")

                if frame.file_name not in files:
                    if "<stdin>" not in frame.file_name:
                        with open(frame.file_name, "r") as file:
                            contents = file.readlines()

                        files[frame.file_name] = contents
                    else:
                        files[frame.file_name] = []

                spaces = len(str(frame.line)) + len(str(self.neighbors))

                for i in range(self.neighbors, 0, -1):
                    if frame.line - i >= 0 and files[frame.file_name]:
                        total += f"{GRAY} {frame.line - i:>{spaces}} {RESET}"
                        text = files[frame.file_name][frame.line - i - 1]
                        total += text

                if files[frame.file_name]:
                    total += f"{self.colors[0]}❱{RESET}{BRIGHT_WHITE}{frame.line:>{spaces}} "
                    text = files[frame.file_name][frame.line - 1]
                    total += f"{text}{RESET}"

                for i in range(1, self.neighbors + 1):
                    if frame.line + i < len(files[frame.file_name]) - 1 and files[frame.file_name]:
                        total += f"{GRAY} {frame.line + i:>{spaces}} {RESET}"
                        text = files[frame.file_name][frame.line + i - 1]
                        total += text

                if frame.locals:
                    local_text = ""

                    for key in frame.locals:
                        value = self.console.color.parse(frame.locals[key], indent=self.indent,
                                                         ignore_str=False)
                        local_text += f"{self.colors[8]}{key}{RESET} = {value}\n"

                    local_text = local_text[:-1]
                    total += str(TitleBox(f"{self.colors[6]}locals{RESET}", local_text,
                                          color=self.colors[6]))
                    total += "\n"

            if stack.syntax_error is not None:
                total += (f"{self.colors[3]}{stack.syntax_error.file_name}{RESET}:"
                          f"{self.colors[4]}{stack.syntax_error.line}{RESET}\n")
                text = stack.syntax_error.text.rstrip()
                total += (f"  {text[:stack.syntax_error.offset - 1]}{UNDERLINE}"
                          f"{text[stack.syntax_error.offset - 1]}{RESET}")

                if stack.syntax_error.offset < len(text):
                    total += f"{text[stack.syntax_error.offset:]}"

                total += f"\n{' ' * (stack.syntax_error.offset + 1)}{self.colors[0]}▲{RESET}"

            total = total if total[-1] != "\n" else total[:-1]
            string += str(TitleBox((f"{self.colors[1]}Traceback{RESET} "
                                    f"{self.colors[2]}(most recent call last){RESET}"), total,
                                   full_screen=True, color=self.colors[0]))

            if stack.syntax_error:
                string += f"{self.colors[7]}{stack.e_type}{RESET}: {stack.syntax_error.msg}"
            else:
                string += f"{self.colors[7]}{stack.e_type}{RESET}: {stack.e_value}"

            if idx != len(self.stacks) - 1:
                if stack.is_cause:
                    string += ("\n\nThe above exception was the direct cause of the following "
                               "exception:\n\n")
                else:
                    string += ("\n\nDuring handling of the above exception, another exception "
                               "occurred:\n\n")

        return string


def __print_traceback(self, color: bool = True, show_locals: bool = False, neighbors: int = 3):
    '''
    Prints the latest traceback to `sys.stderr` if there is any, otherwise it shows a warning.

    ## Params

    color: bool = whether to print with color or not. default is True.

    show_locals: bool = whether to show local variables or not. default is False.

    neighbors: int = the amount of neighboring lines to show in addition to the line of the error.
    default is 3.
    '''
    if color:
        try:
            trace = TraceBack(show_locals=show_locals, neighbors=neighbors, indent=self.indent,
                              colors=self.color.color_t["traceback"])
            print(self.color.parse(trace), file=sys.stderr)
        except ValueError:
            self.warn("no recent traceback was found", TracebackWarning, stacklevel=2)
    else:
        print(format_exc(), file=sys.stderr)


Console.print_traceback = __print_traceback


def install_errors(*, show_locals: bool = False, neighbors: int = 3,
                   colors: list[Color] | None = None, **kwargs) -> Callable:
    '''
    Replaces and returns the old `sys.excepthook` with a colored and easier to read version.

    ## Params

    show_locals: bool = whether to show local variables or not. default is False.

    neighbors: int = the amount of neighboring lines to show in addition to the line of the
    error. default is 3.

    colors: list[Color] | None = the list of colors to use for parsing elements. default value
    is None for auto-detection. (refer to `ColorParser` for more info on the colors list).

    kwargs = keywords arguments for the console if there is no global defined yet. (refer to
    `Console` for more information on valid keyword arguments).

    ## Returns

    The return value is the old `sys.excepthook` callable.
    '''
    console = get_console(**kwargs)

    if colors:
        console.color.set_color(TracebackType, colors)

    def except_hook(type_: type[BaseException], value: BaseException, trace: TracebackType | None):
        console.error(TraceBack.from_exception(type_, value, trace, show_locals=show_locals,
                                               neighbors=neighbors, indent=console.indent,
                                               colors=console.color.color_t["traceback"]),
                      reset=False)

    old_hook, sys.excepthook = sys.excepthook, except_hook
    return old_hook


def install_warnings(**kwargs) -> Callable:
    '''
    Replaces and returns the old `warnings.showwarning` with a colored and easier to read version.

    ## Params

    kwargs = keywords arguments for the console if there is no global defined yet. (refer to
    `Console` for more information on valid keyword arguments).

    ## Returns

    The return value is the old `warnings.showwarning` callable.
    '''
    console = get_console(**kwargs)

    def show_warning(message: Warning | str, category: type[Warning], filename: str, lineno: int,
                     file: TextIO | None = None, line: str | None = None):
        if console.color.type_ == SIMPLE:
            filename_color = f"{LIME}{filename}{RESET}"
            warning_color = f"{YELLOW}{category.__name__}: {message}{RESET}"
            location = (f"\n  {BRIGHT_WHITE}{linecache.getline(filename, lineno).strip()}{RESET}"
                        if filename != "<stdin>" else "")
            msg_color = f"{filename_color}:{console.color.parse(lineno)}: {warning_color}{location}"
            msg_box = Box(msg_color, full_screen=True, color=YELLOW)
            console.error(msg_box, reset=False, sep="", color=False)
        elif console.color.type_ == RGB:
            filename_color = f"{Color.from_rgb(97, 205, 50)}{filename}{RESET}"
            yellow = Color.from_rgb(238, 210, 2)
            warning_color = f"{yellow}{category.__name__}: {message}{RESET}"
            white = Color.from_rgb(255, 255, 255)
            location = (f"\n  {white}{linecache.getline(filename, lineno).strip()}{RESET}"
                        if filename != "<stdin>" else "")
            msg_color = f"{filename_color}:{console.color.parse(lineno)}: {warning_color}{location}"
            msg_box = Box(msg_color, full_screen=True, color=yellow)
            console.error(msg_box, reset=False, sep="", color=False)

        linecache.clearcache()

    old_handler, warnings.showwarning = warnings.showwarning, show_warning
    return old_handler
