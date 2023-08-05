from __future__ import annotations

import os
import re

from .color import Color, RESET
from . import colorwrap


class Box:
    '''
    # Box Class

    The box class displays its contents inside a box.

    ## Params

    contents: str = the box's contents.

    width: int = the box's width. default is -1 to find the width from the length of the contents.

    height: int = the box's minimum height. default is -1 to find the height from the amount of
    lines that are needed to display all contents.

    full_screen: bool = whether to use all the console's available width. default is False.

    fit: bool = wheter to scale the width to fit the longest line. it's ignored if `full_screen` is
    True. default is True.

    color: Color | None = the box's border color. default is no color.

    ## Additional Attributes

    lines: list[str] = a list of 6 elements representing the box's border. in order: vertical bar,
    horizontal bar, top left corner, top right corner, bottom left corner and bottom right corner.
    '''
    def __init__(self, contents: str, width: int = -1, height: int = -1, full_screen: bool = False,
                 fit: bool = True, color: Color | None = None):
        self.lines = ["│", "─", "╭", "╮", "╰", "╯"]
        self._pattern = re.compile("(\033)[^m]*m", re.DOTALL)
        self._full_screen = full_screen
        self._fit = fit
        self._color: Color | str = color or ""
        self._contents = contents
        self._width = width
        self.width = width
        self.height = height

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: Color | None):
        self._color = value or ""

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        size = os.get_terminal_size()

        if not self.full_screen:
            temp = self.contents.split("\n")
            temp = [self._pattern.sub("", x) for x in temp]
            max_len = max([len(x) for x in temp])

            if self.fit:
                self._width = max_len if self._width < max_len else self._width
            else:
                self._width = self._width if self._width >= 1 else max_len

        self._width = self._width if 1 <= self._width <= size.columns - 4 else size.columns - 4

    @property
    def fit(self):
        return self._fit

    @fit.setter
    def fit(self, value: bool):
        self._fit = value

        if not self.full_screen and self._fit:
            self.width = self.width

    @property
    def full_screen(self):
        return self._full_screen

    @full_screen.setter
    def full_screen(self, value: bool):
        self._full_screen = value

        self.width = os.get_terminal_size().columns - 4

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, value: str):
        self._contents = value

        if not self.full_screen:
            self.width = self.width

    def __str__(self) -> str:
        if self.full_screen:
            self.full_screen = True

        reset = RESET if self.color else ""
        vertical = f"{self.color}{self.lines[0]}{reset}"

        wrapped = colorwrap.wrap(self.contents, self.width)
        wrapped = [f"{vertical} " + x for x in wrapped]

        left_height = self.height - len(wrapped)
        up = left_height // 2 if left_height > 0 else 0
        down = left_height - up if left_height > 0 else 0

        top = f"{self.lines[2]}{self.lines[1] * (self.width + 2)}{self.lines[3]}"
        bottom = f"{self.lines[4]}{self.lines[1] * (self.width + 2)}{self.lines[5]}"
        empty = f"{vertical}{' ' * (self.width + 2)}{vertical}\n"

        string = f"{self.color}{top}{reset}\n" + (empty * up)

        for item in wrapped:
            offset = self.width - len(self._pattern.sub("", item)) + 2
            string += (f"{item}" + (" " * offset) + f" {vertical}\n")

        string += ((empty * down) + f"{self.color}{bottom}{reset}")

        return string

    def __repr__(self) -> str:
        return (f"Box(width={self.width}, height={self.height}, full_screen={self.full_screen}, "
                f"fit={self.fit}, color={repr(self.color)})")


class TitleBox(Box):
    '''
    # Title Box Class

    A sub-class of the box class, it displays its contents inside a box with a title.

    ## Params

    title: str = the box's title.

    contents: str = the box's contents.

    width: int = the box's width. default is -1 to find the width from the length of the contents
    and the title.

    height: int = the box's minimum height. default is -1 to find the height from the amount of
    lines that are needed to display all contents.

    full_screen: bool = whether to use all the console's available width. default is False.

    fit: bool = wheter to scale the width to fit the longest line. it's ignored if `full_screen` is
    True. default is True.

    color: Color | None = the box's border color. default is no color.

    placeholder: str = what to replace part of the title if it can't fit on the given width. default
    is " [...]".

    ## Additional Attributes

    lines: list[str] = a list of 6 elements representing the box's border. in order: vertical bar,
    horizontal bar, top left corner, top right corner, bottom left corner and bottom right corner.
    '''
    def __init__(self, title: str, contents: str, width: int = -1, height: int = -1,
                 full_screen: bool = False, fit: bool = True, color: Color | None = None,
                 placeholder: str = " [...]"):
        self._title = title
        super().__init__(contents, width, height, full_screen, fit, color)
        self.placeholder = placeholder

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        size = os.get_terminal_size()

        if not self.full_screen:
            temp = self.contents.split("\n")
            nc_title = [self._pattern.sub("", self.title.replace("\n", " ") + "12")]
            temp = [self._pattern.sub("", x) for x in temp] + nc_title
            max_len = max([len(x) for x in temp])

            if self.fit:
                self._width = max_len if self._width < max_len else self._width
            else:
                self._width = self._width if self._width >= 1 else max_len

        self._width = self._width if 1 <= self._width <= size.columns - 4 else size.columns - 4

    def __str__(self) -> str:
        string = super().__str__()
        title = colorwrap.shorten(self.title, self.width - 2, self.placeholder)

        space = self.width - len(self._pattern.sub("", title) + "12")
        left = space // 2 if space > 0 else 0
        right = space - left if space > 0 else 0

        reset = RESET if self.color else ""
        tl = f"{self.lines[1] * left}{reset}"
        tr = f"{self.color}{self.lines[1] * right}"
        top = f"{self.lines[2]}{self.lines[1]}{tl} {title} {tr}{self.lines[1]}{self.lines[3]}"
        top = f"{self.color}{top}{reset}"

        temp = string.split("\n")
        temp[0] = top
        return "\n".join(temp)

    def __repr__(self) -> str:
        return "Title" + super().__repr__()[:-1] + f", placeholder={self.placeholder})"
