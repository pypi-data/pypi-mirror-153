from __future__ import annotations

import textwrap

from enum import Enum
from numbers import Number
from types import FunctionType, ModuleType

from .color import Color, ColorCode, ColorMod, RESET


class ColorParser:
    '''
    # Color Parser Class

    Parses objects into colored strings depending of the parser type (SIMPLE or RGB) and the
    registered color for the given object type.

    ## Params

    type_: DefaultType = the type of the parser, which can be SIMPLE or RGB. default value is
    SIMPLE.

    e.g.
    ```python
      from pyconsole import ColorParser, RGB


      parser = ColorParser(RGB)
    ```
    '''
    class DefaultType(Enum):
        SIMPLE = 1
        RGB = 2

    def __init__(self, type_: ColorParser.DefaultType = DefaultType.SIMPLE):
        self.type_: ColorParser.DefaultType = type_

        if self.type_ == ColorParser.DefaultType.SIMPLE:
            self.color_t = {
                Number: Color(ColorCode.CYAN),
                str: Color(ColorCode.BRIGHT_GREEN),
                bool: Color(ColorCode.GRAY),
                "container": [
                    Color(ColorCode.YELLOW),
                    Color(ColorCode.MAGENTA),
                    Color(ColorCode.BLUE)
                ],
                FunctionType: Color(ColorCode.BRIGHT_RED),
                type(None): Color(ColorCode.RED),
                type: Color(ColorCode.BRIGHT_MAGENTA),
                ModuleType: Color(ColorCode.BRIGHT_RED),
                type(...): Color(ColorCode.GREEN),
                "traceback": [
                    Color(ColorCode.RED),  # Border color and error
                    Color(ColorCode.RED),  # Traceback color
                    Color(ColorCode.BRIGHT_RED, [ColorMod.FAINT]),  # Most recent call color
                    Color(ColorCode.YELLOW),  # File color
                    Color(ColorCode.BLUE),  # File line color
                    Color(ColorCode.GREEN),  # Function color
                    Color(ColorCode.BRIGHT_YELLOW),  # Locals border color
                    Color(ColorCode.RED),  # Final error message
                    Color(ColorCode.YELLOW, [ColorMod.FAINT])  # Locals variable
                ]
            }
        elif self.type_ == ColorParser.DefaultType.RGB:
            self.color_t = {
                Number: Color.from_rgb(54, 247, 186),
                str: Color.from_rgb(69, 250, 60),
                bool: Color.from_rgb(160, 160, 160),
                "container": [
                    Color.from_rgb(255, 215, 0),
                    Color.from_rgb(207, 52, 118),
                    Color.from_rgb(86, 52, 207)
                ],
                FunctionType: Color.from_rgb(209, 54, 78),
                type(None): Color.from_rgb(217, 20, 49),
                type: Color.from_rgb(201, 77, 250),
                ModuleType: Color.from_rgb(250, 71, 55),
                type(...): Color.from_rgb(14, 189, 2),
                "traceback": [
                    Color.from_rgb(255, 13, 13),  # Border color and error
                    Color.from_rgb(255, 18, 49),  # Traceback color
                    Color.from_rgb(209, 10, 24),  # Most recent call color
                    Color.from_rgb(227, 193, 2),  # File color
                    Color.from_rgb(5, 8, 227),  # File line color
                    Color.from_rgb(4, 194, 4),  # Function color
                    Color.from_rgb(255, 165, 0),  # Locals border color
                    Color.from_rgb(255, 0, 0),  # Final error message
                    Color.from_rgb(209, 180, 13)  # Locals variable
                ]
            }
        else:
            raise NotImplementedError

    def set_color(self, type_: type | str, color: Color | list[Color]):
        '''
        Registers a type with a given color.

        ## Params

        type_: type = it's the type of the object you want to register, like int.

        color: Color = it's the color you want to parse your `type_` into.

        Notice that if `type_` is a string then only two values will really have any effect, and
        those are 'container' and 'traceback'. Both expect a list[Color] as the `color` parameter.

        For 'container', the `color` parameter can be an arbitrarily long list, with each value
        meaning the color for a deeper nested container in increasing order before it loops back.

        For 'traceback', the `color` parameter expects a 9 elements list, where each element
        represents a part of the exception that it colors. Those are, in the expected order:
        * Border color and error arrow color
        * Traceback (title color)
        * Most recent call (secondary title color)
        * File color
        * File line color
        * Function name color
        * Locals border color
        * Final error message
        * Locals variable names color
        '''
        self.color_t[type_] = color

    def parse(self, item, indent: int = 0, *, ignore_str: bool = True, depth: int = 0) -> str:
        '''
        Parses an object to a string with its respected coloring and other attributes. If the object
        is not registered then it just returns it's normal string representation.

        ## Params

        item: any = the object you want to parse.

        indent: int = the indentation fot containers like lists. default value is 0.

        ## Internal Parameters

        ignore_string: bool = if you want to ignore the parsing of a string into color or not.
        default value is True, but changes when inside containers to False.

        depth: int = value that references how many times the function has been internally called.
        it's used to know which color to use on nested containers. default value is 0.

        ## Return

        The return value is the parsed string ending with a 'reset color' code.
        '''
        color: Color | list[Color] | None = self.color_t.get(type(item), None)

        if color is None:
            if isinstance(item, Number):
                color = self.color_t[Number]
            elif isinstance(item, (list, tuple, set, dict)):
                color = self.color_t["container"]
                depth = depth if depth < len(color) else 0
                color = color[depth]
                item_str: str = (["[", "]"] if isinstance(item, list)
                                 else (["(", ")"] if isinstance(item, tuple) else ["{", "}"]))
                delimiter_l: str = f"{color}{item_str[0]}{RESET}"
                delimiter_r: str = f"{color}{item_str[1]}{RESET}"
                nl: str = "\n" if indent else ""
                space: str = " " * indent if indent else ""
                join: str = ",\n" if indent else ", "

                if isinstance(item, dict):
                    values = [(self.parse(x, indent=indent, ignore_str=False, depth=depth + 1),
                               self.parse(y, indent=indent, ignore_str=False, depth=depth + 1))
                              for x, y in item.items()]
                    inside: str = textwrap.indent(join.join(f"{x}: {y}" for x, y in values), space)
                else:
                    values = [self.parse(x, indent=indent, ignore_str=False, depth=depth + 1)
                              for x in item]
                    inside: str = textwrap.indent(join.join(values), space)

                return f"{delimiter_l}{nl}{inside}{nl}{delimiter_r}"
            elif hasattr(item, "__color__"):
                return item.__color__()
            else:
                return str(item)
        else:
            if isinstance(item, str):
                if not ignore_str:
                    item = repr(item)
                else:
                    return item

        return f"{color}{item}{RESET}"


#####################################################
#                 Color Parser Mode                 #
#####################################################
SIMPLE = ColorParser.DefaultType.SIMPLE
RGB = ColorParser.DefaultType.RGB
#####################################################
