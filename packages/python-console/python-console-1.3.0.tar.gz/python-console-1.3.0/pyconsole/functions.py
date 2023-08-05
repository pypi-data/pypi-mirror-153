from __future__ import annotations

from typing import Callable

from .color import Color
from .color_traceback import install_errors, install_warnings
from . import pretty


def install(*, show_locals: bool = False, neighbors: int = 3, colors: list[Color] | None = None,
            **kwargs) -> tuple[Callable, Callable, Callable]:
    '''
    Calls the functions `install_errors`, `install_warnings` and `pretty.install` with their
    respective keyword arguments.

    It returns a tuple of all three installers return value in the order shown above.
    '''
    old_error = install_errors(show_locals=show_locals, neighbors=neighbors, colors=colors,
                               **kwargs)
    old_warning = install_warnings(**kwargs)
    old_pretty = pretty.install(**kwargs)

    return old_error, old_warning, old_pretty
