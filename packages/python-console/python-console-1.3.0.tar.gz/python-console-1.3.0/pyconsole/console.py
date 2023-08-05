from __future__ import annotations

import platform
import time
import threading
import getpass
import concurrent.futures
import os
import sys

from typing import Callable
from warnings import warn

from inputhandler import getwch

from .color import Color, BLUE, RESET, YELLOW
from .color_parser import ColorParser, SIMPLE, RGB
from .keyboard import Keyboard


if platform.system() == "Windows":
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

    class _ConsoleInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.wintypes._COORD), ("cursor_pos", ctypes.wintypes._COORD),
                    ("attributes", ctypes.wintypes.WORD), ("window", ctypes.wintypes.SMALL_RECT),
                    ("max_size", ctypes.wintypes._COORD)]
else:
    import signal


class Console:
    '''
    # Console Class

    The console class can be used to manipulate the console and the standard output to an extent.

    ## Params

    indent: int = indicates how much to indent containers when parsing them to a colored string.
    default is 2.

    pass_prompt: str = what to show after the normal prompt when asking for a password with the
    `getpass` method. default is "" (it is a key on a nerd font, if you can't see it then you don't
    have a compatible font installed and should probably change this value - or the font. for more
    information visit: (https://www.nerdfonts.com/).

    color_mode: ColorParser.DefaultType = the color mode that you want the console to be in. default
    is SIMPLE. (options are: SIMPLE or RGB).

    ## Other Attributes

    color: ColorParser = the color parser object associated with the console instance.

    system: str = the current system the console was instanciated in. equivalent of calling
    `platform.system()`.

    cursor: Cursor = the current console cursor object.

    keyboard: Keyboard = the current keyboard associated with the console instance.

    size: terminal_size = the current terminal dimensions. equivalent of `os.get_terminal_size()`.
    '''
    class Cursor:
        '''
        # Console Cursor Class

        The cursor class is used for updating the cursor settings on the terminal.

        ## Attributes

        system: str = the current system the cursor is in. equivalent of `platform.system()`.
        '''
        def __init__(self):
            self._system: str = platform.system()

            if self.system == "Windows":
                self._curi = _CursorInfo()
                self._handle = ctypes.windll.kernel32.GetStdHandle(-11)
                ctypes.windll.kernel32.GetConsoleCursorInfo(self._handle, ctypes.byref(self._curi))

                self._coni = _ConsoleInfo()
                ctypes.windll.kernel32.GetConsoleScreenBufferInfo(self._handle,
                                                                  ctypes.byref(self._coni))

        @property
        def system(self):
            return self._system

        def hide(self):
            '''
            Hides the cursor on the screen.

            Note: don't forget to call the `restore` method to set the terminal back to its original
            state. or wrap around the function where you want to hide the cursor with the `wrap`
            method.
            '''
            if self.system == "Windows":
                self._curi.visible = False
                ctypes.windll.kernel32.SetConsoleCursorInfo(self._handle, ctypes.byref(self._curi))
            else:
                print("\033[?25l", end="", flush=True)

        def restore(self):
            '''
            Restores the cursor to its original visible state.
            '''
            if self.system == "Windows":
                self._curi.visible = True
                ctypes.windll.kernel32.SetConsoleCursorInfo(self._handle, ctypes.byref(self._curi))
            else:
                print("\033[?25h", end="", flush=True)

        def wrap(self, func: Callable, *args, **kwargs):
            '''
            Wraps the function passed as `func` hiding the cursor and restoring its settings after
            execution or in case of an exception.

            ## Params

            func: Callable = the function you want to wrap.

            args = positional arguments passed to the function `func`.

            kwargs = keyword arguments passed to the function `func`.
            '''
            self.hide()

            try:
                value = func(*args, **kwargs)
            finally:
                self.restore()

            return value

        def move(self, row: int = 1, column: int = 1):
            '''
            Moves the cursor position to the one specified by row and column. default is the top
            left corner (1, 1).
            '''
            if self.system == "Windows":
                new_pos = ctypes.wintypes._COORD(row - 1, column - 1)
                ctypes.windll.kernel32.SetConsoleCursorPosition(self._handle, new_pos)
            else:
                print(f"\033[{row};{column}H", end="")

    def __init__(self, *, indent: int = 2, pass_prompt: str = "",
                 color_mode: ColorParser.DefaultType = SIMPLE):
        self.indent: int = indent
        self.pass_prompt: str = pass_prompt
        self._color = ColorParser(color_mode)
        self._system = platform.system()
        self._cursor: Console.Cursor = Console.Cursor()
        self._keyboard = Keyboard()
        self._size: os.terminal_size = os.get_terminal_size()

    @property
    def color(self):
        return self._color

    @property
    def system(self):
        return self._system

    @property
    def cursor(self):
        return self._cursor

    @property
    def keyboard(self):
        return self._keyboard

    @property
    def size(self):
        self._size = os.get_terminal_size()
        return self._size

    def print(self, *args, color: bool = True, reset: bool = True, sep: str = " ", end: str = "\n",
              flush: bool = False):
        '''
        Prints the values to the standard output in color format if the keyword argument `color` is
        set to True. otherwise it prints only non parsed text.

        ## Params

        args = positional arguments that will be color parsed and then print on the standard output.

        color: bool = whether to print in color or not. default is True.

        reset: bool = whether to automatically end the print with a `RESET` color token. deafult is
        True.

        sep: str = the string separator value. default is a space.

        end: str = the string end value. default is a new line.

        flush: bool = whether to flush the stream forcefully or not. default is False.
        '''
        if color:
            if reset:
                end = f"{end}{RESET}"

            print(*[self.color.parse(x, self.indent) for x in args], sep=sep, end=end, flush=flush)
        else:
            print(*args, sep=sep, end=end, flush=flush)

    def error(self, *args, color: bool = True, reset: bool = True, sep: str = " ", end: str = "\n",
              flush: bool = False):
        '''
        Prints colored to `sys.stderr` if `color` is set to True. otherwise it prints only non
        parsed text.

        ## Params

        args = positional arguments that will be color parsed and then print on the standard output.

        color: bool = whether to print in color or not. default is True.

        reset: bool = whether to automatically end the print with a `RESET` color token. deafult is
        True.

        sep: str = the string separator value. default is a space.

        end: str = the string end value. default is a new line.

        flush: bool = whether to flush the stream forcefully or not. default is False.
        '''
        if color:
            if reset:
                end = f"{end}{RESET}"

            print(*[self.color.parse(x, self.indent) for x in args], sep=sep, end=end,
                  file=sys.stderr, flush=flush)
        else:
            print(*args, sep=sep, end=end, flush=flush)

    def warn(self, message: str | Warning, category: type[Warning] | None = None,
             stacklevel: int = 1, source=None):
        '''
        A simple wrapper around `warnings.warn`
        '''
        warn(message, category, stacklevel + 1, source)

    def get_key(self, *, stop_exec: bool = True) -> int:
        '''
        Get a key press and return its integer representation.

        Check `Keyboard.Key` for more information.

        ## Optional Keyword Arguments

        stop_exec: bool = whether to raise KeyboardInterrupt when Ctrl+C is inputed or not. default
        is True.
        '''
        key: str = getwch()

        if self.system == "Windows" and key == "\x00":
            return self.keyboard.key_values[key][getwch()]
        elif self.system != "Windows" and key == "\x1b":
            def interrupt(signum, frame):
                raise RuntimeError

            def get_arrow():
                try:
                    old_values = signal.setitimer(signal.ITIMER_REAL, 0.01)
                    getwch()
                    char = getwch()
                    signal.setitimer(signal.ITIMER_REAL, *old_values)
                    return char
                except RuntimeError:
                    return

            old_handle = signal.signal(signal.SIGALRM, interrupt)
            value: Keyboard.Key = self.keyboard.key_values[key][get_arrow()]
            signal.signal(signal.SIGALRM, old_handle)

            return value
        elif key == "\x03":
            if stop_exec:
                raise KeyboardInterrupt

        return self.keyboard.key_values[key]

    def getpass(self, prompt: str = "Password: ") -> str:
        '''
        Ask for a password without showing the text.

        ## Params

        prompt: str = what to show when asking for the password.

        Note: the console instance attribute of `pass_prompt` is shown after the given `prompt` as a
        blinking colored string until the password is fully given.

        ## Returns

        It returns the entered password as a string.
        '''
        def helper() -> str:
            active: bool = True

            def show_prompt():
                while active:
                    color = YELLOW if self.color.type_ == SIMPLE else Color.from_rgb(255, 215, 0)
                    show = f"\r{prompt}{color}{self.pass_prompt}{RESET}"
                    print(show, end="", flush=True)
                    time.sleep(0.5 if active else 0)
                    print(f"\r{prompt}{' ' * len(self.pass_prompt)}", end="", flush=True)
                    time.sleep(0.5 if active else 0)

            show_thread = threading.Thread(target=show_prompt, daemon=True)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                password_exec = executor.submit(getpass.getpass, "")
                show_thread.start()
                password = password_exec.result()
                active = False
                show_thread.join()
                print("\r", end="", flush=True)

            return password

        return self.cursor.wrap(helper)

    def clear(self):
        '''
        Clears the screen and moves the cursor to the top left corner.
        '''
        self.cursor.move()
        empty = " " * self.size.columns * self.size.lines
        print(empty, end="")
        self.cursor.move()

    def command(self, cmd: str) -> int:
        '''
        Executes a shell command and returns its exit code. equivalent to `os.system`.

        ## Params

        cmd: str = the command to execute

        ## Returns

        Returns the exit status
        '''
        return os.system(cmd)

    def __repr__(self) -> str:
        if self.color.type_ == SIMPLE:
            return f"Console(indent={self.indent}, mode=SIMPLE)"
        elif self.color.type_ == RGB:
            return f"Console(indent={self.indent}, mode=RGB)"

    def __color__(self) -> str:
        if self.color.type_ == SIMPLE:
            indent_color: str = f"{self.color.parse(self.indent)}"
            mode_color: str = f"{YELLOW}SIMPLE{RESET}"
            return f"{BLUE}Console{RESET}(indent={indent_color}, mode={mode_color})"
        elif self.color.type_ == RGB:
            console_color: str = f"{Color.from_rgb(86, 19, 212)}Console{RESET}"
            indent_color: str = f"{self.color.parse(self.indent)}"
            mode_color: str = f"{Color.from_rgb(255, 215, 0)}RGB{RESET}"
            return f"{console_color}(indent={indent_color}, mode={mode_color})"
