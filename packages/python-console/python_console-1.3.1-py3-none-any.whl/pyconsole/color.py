from __future__ import annotations

from enum import Enum


class ColorCode(Enum):
    BLACK = 30
    BG_BLACK = 40
    RED = 31
    BG_RED = 41
    GREEN = 32
    BG_GREEN = 42
    YELLOW = 33
    BG_YELLOW = 43
    BLUE = 34
    BG_BLUE = 44
    MAGENTA = 35
    BG_MAGENTA = 45
    CYAN = 36
    BG_CYAN = 46
    WHITE = 37
    BG_WHITE = 47
    GRAY = 90
    BG_GRAY = 100
    BRIGHT_RED = 91
    BG_BRIGHT_RED = 101
    BRIGHT_GREEN = 92
    BG_BRIGHT_GREEN = 102
    BRIGHT_YELLOW = 93
    BG_BRIGHT_YELLOW = 103
    BRIGHT_BLUE = 94
    BG_BRIGHT_BLUE = 104
    BRIGHT_MAGENTA = 95
    BG_BRIGHT_MAGENTA = 105
    BRIGHT_CYAN = 96
    BG_BRIGHT_CYAN = 106
    BRIGHT_WHITE = 97
    BG_BRIGHT_WHITE = 107


class ColorMod(Enum):
    RESET = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    STRIKE = 9
    DOUBLE_UNDERLINE = 21
    OVERLINE = 53


class Color:
    '''
    # Color Class

    creates an ansi escape sequence representing the desired color and modifications selected.

    ## Params

    code: ColorCode = a ColorCode enum object representing a color value.

    mods: lsit[ColorMod] = a list of ColorMod enum object representing text modifications.

    e.g.
    ```python
      from pyconsole import Color, ColorCode, ColorMod


      color = Color(ColorCode.RED, [ColorMod.BOLD, ColorMod.UNDERLINE])
    ```

    ## Other Options

    you can also create a color from an rgb value using the `from_rgb` class method.
    '''
    def __init__(self, code: ColorCode | None = None, mods: list[ColorMod] | None = None):
        self.code: str = f"{code.value}" if code is not None else ""
        self.mods: str = ";".join(f"{x.value}" for x in mods) if mods else ""
        self.attrs: str = ";".join(x for x in [self.code, self.mods] if x)
        self.color: str = f"\033[{self.attrs}m" if self.attrs else ""
        self.rgb: bool = False

    @classmethod
    def from_rgb(cls, r: int = 0, g: int = 0, b: int = 0, *, bg: bool = False) -> Color:
        '''
        Creates a color from an rgb value.

        ## Params

        r: int = represents the red value, with a non enforced range of (0, 255).

        g: int = represents the green value, with a non enforced range of (0, 255).

        b: int = represents the blue value, with a non enforced range of (0, 255).

        bg: bool = if the value is a background color instead of foreground. default is False.

        e.g.
        ```python
          color = Color.from_rgb(255, 0, 255)
          bg_rgb = Color.from_rgb(240, 10, 0, bg=True)
        ```

        ## Return

        Returns a color instance with the given values.
        '''
        color = cls()
        color.attrs = f"{r};{g};{b}"

        if not bg:
            color.color = f"\033[38;2;{color.attrs}m"
        else:
            color.color = f"\033[48;2;{color.attrs}m"

        color.rgb = True
        return color

    def __add__(self, other: Color) -> Color:
        if isinstance(other, Color):
            new = Color()
            new.rgb = self.rgb | other.rgb

            self_bg = "48" if "48" in self.color else "38"
            self_color = f"{self_bg};2;{self.attrs}" if self.rgb else self.code
            other_bg = "48" if "48" in other.color else "38"
            other_color = f"{other_bg};2;{other.attrs}" if other.rgb else other.code
            new.code = ";".join(x for x in [self_color, other_color] if x)

            new.mods = ";".join(x for x in [self.mods, other.mods] if x)

            new.attrs = ";".join(x for x in [new.code, new.mods] if x)
            new.color = f"\033[{new.attrs}m" if new.attrs else ""

            return new
        else:
            raise NotImplementedError

    def __str__(self) -> str:
        return self.color

    def __repr__(self) -> str:
        return f"Color(color={self.attrs}, rgb={self.rgb})"


#####################################################
#                  Color Constants                  #
#####################################################
RED = Color(ColorCode.RED)
BLUE = Color(ColorCode.BLUE)
LIME = Color(ColorCode.BRIGHT_GREEN)
YELLOW = Color(ColorCode.YELLOW)
CYAN = Color(ColorCode.CYAN)
WHITE = Color(ColorCode.WHITE)
GREEN = Color(ColorCode.GREEN)
GRAY = Color(ColorCode.GRAY)
BRIGHT_WHITE = Color(ColorCode.BRIGHT_WHITE)
RESET = Color(mods=[ColorMod.RESET])
BOLD = Color(mods=[ColorMod.BOLD])
UNDERLINE = Color(mods=[ColorMod.UNDERLINE])
#####################################################
