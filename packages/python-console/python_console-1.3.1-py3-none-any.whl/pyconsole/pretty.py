import sys
import builtins

from typing import Callable

from .global_data import get_console


def install(**kwargs) -> Callable:
    '''
    Installs pretty printing for interactive sessions.

    ## Params

    kwargs = keyword arguments for the global console. (refer to `Console` for more information on
    valid keyword arguments).

    ## Returns

    It returns the previous `sys.displayhook`.
    '''
    console = get_console(**kwargs)

    def display_hook(value):
        if value is not None:
            builtins._ = None
            console.print(console.color.parse(value, console.indent, ignore_str=False), color=False)
            builtins._ = value

    old_hook, sys.displayhook = sys.displayhook, display_hook
    return old_hook
