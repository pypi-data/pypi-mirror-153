from __future__ import annotations

import textwrap
import re

from .color import RESET


def wrap(contents: str, width: int) -> list[str]:
    '''
    Wraps text on maximum width ignoring color related characters and new lines.

    ## Params

    contents: str = the contents to wrap.

    width: int = the maximum length allowed before wrapping.

    ## Returns

    returns a list of sub-strings of the original text width each string having a max length of
    `width`.
    '''
    pattern = re.compile("(\033)[^m]*m", re.DOTALL)
    color_pos: list[str] = []

    result = contents

    while match := pattern.search(result):
        pos = match.span()

        if pos[1] == len(result) or result[pos[1]] == "\n":
            if result[pos[0] - 1] == "\x00":
                temp = result[:pos[0]] + result[pos[1]:]
                color_pos[-1] = color_pos[-1] + match.group()
            else:
                temp = result[:pos[0] - 1] + "\x00" + result[pos[1]:]
                color_pos.append(result[pos[0] - 1] + match.group())
        else:
            temp = result[:pos[0]] + "\x00" + result[pos[1] + 1:]
            color_pos.append(match.group() + result[pos[1]])

        result = temp

    wrapped = ["\n".join(textwrap.wrap(line, width, replace_whitespace=False))
               for line in result.split("\n")]
    temp = [x.split("\n") for x in wrapped]
    wrapped = [y for x in temp for y in x]

    current = 0

    for idx, item in enumerate(wrapped):
        amount = item.count("\x00")

        for _ in range(amount):
            wrapped[idx] = wrapped[idx].replace("\x00", color_pos[current], 1)
            current += 1

    return wrapped


def shorten(text: str, width: int, placeholder: str = " [...]") -> str:
    '''
    Shortens text ignoring color related characters and adds a placeholder at the end

    ## Params

    text: str = the text to shorten.

    width: int = the max length allowed before shortening.

    placeholder: str = what to add at the end if shortening happened. default is " [...]"

    ## Returns

    Returns the shortened string if it exceded the maximum width, otherwise it returns the same
    string.
    '''
    pattern = re.compile("(\033)[^m]*m", re.DOTALL)
    color_pos: list[str] = []

    result = text.replace("\n", " ")

    while match := pattern.search(result):
        pos = match.span()

        if pos[1] == len(result):
            if result[pos[0] - 1] == "\x00":
                temp = result[:pos[0]] + result[pos[1]:]
                color_pos[-1] = color_pos[-1] + match.group()
            else:
                temp = result[:pos[0] - 1] + "\x00" + result[pos[1]:]
                color_pos.append(result[pos[0] - 1] + match.group())
        else:
            temp = result[:pos[0]] + "\x00" + result[pos[1] + 1:]
            color_pos.append(match.group() + result[pos[1]])

        result = temp

    short = textwrap.shorten(result, width, placeholder=placeholder)

    amount = short.count("\x00")

    for i in range(amount):
        short = short.replace("\x00", color_pos[i], 1)

    if amount < len(color_pos):
        short += str(RESET)

    return short
