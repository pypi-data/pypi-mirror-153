from __future__ import annotations

import platform
import inspect

from collections import defaultdict
from warnings import warn

from .errors import KeyboardWarning, KeyNotFoundError


class Keyboard:
    '''
    # Keyboard Class

    The keyboard class manages a key registry used in `Console.get_key()`

    ## Attributes

    system: str = the system where the keyboard instance was created. equivalent of
    `platform.system()`.

    key_values: defaultdict[str, int] = the currently registered keys.
    '''
    class KeyMeta(type):
        '''
        # Key Meta Class

        The key meta class in charge of setting the key's attributes.
        '''
        @property
        def next_num(cls):
            return cls._next_num

        def __setattr__(cls, name: str, value):
            if hasattr(cls, name):
                if name == "_next_num":
                    return super().__setattr__(name,  value)
                elif name == "next_num":
                    raise AttributeError("next_num is read only")

                raise AttributeError("cannot reassign members")

            if not isinstance(value, int):
                raise TypeError("the value must be of type int")

            if value < cls._next_num:
                raise ValueError(f"the value must be unique (next available: {cls._next_num})")
            elif value > cls._next_num:
                value = cls._next_num
                warn(f"value set to the next available number: {cls._next_num}", KeyboardWarning, 2)

            cls._next_num += 1
            super().__setattr__(name, value)

        def __repr__(cls) -> str:
            return "<Keyboard.Key>"

    class Key(metaclass=KeyMeta):
        '''
        # Key Class

        The key class contains a registry of valid keys as integers.

        ## Attributes

        next_num: int = the next available number for key registration. currently starts at 98.

        ## Instance

        If you try to instantiate the Key class then you won't get a Key object, but instead will
        get the associated name of the given integer or a KeyNotFoundError if there is no match.

        e.g.
        ```python
          from pyconsole import Keyboard


          key = Keyboard.Key(1)
          print(f"The key associated with the number 1 is {key}")
          # The key associated with the number 1 is LEFT
        ```

        ## Registered Keys

        The following is the default registered keys list:
        * LEFT: left arrow key
        * RIGHT: right arrow key
        * UP: up arrow key
        * DOWN: down arrow key
        * ESC: escape key
        * DELETE: delete key
        * ENTER: enter key
        * A: 'a' key
        * B: 'b' key
        * C: 'c' key
        * D: 'd' key
        * E: 'e' key
        * F: 'f' key
        * G: 'g' key
        * H: 'h' key
        * I_: 'i' key
        * J: 'j' key
        * K: 'k' key
        * L: 'l' key
        * M: 'm' key
        * N: 'n' key
        * O_: 'o' key
        * P: 'p' key
        * Q: 'q' key
        * R: 'r' key
        * S: 's' key
        * T: 't' key
        * U: 'u' key
        * V: 'v' key
        * W: 'w' key
        * X: 'x' key
        * Y: 'y' key
        * Z: 'z' key
        * TAB: tab key
        * CAPS_A: upper case 'A'
        * CAPS_B: upper case 'B'
        * CAPS_C: upper case 'C'
        * CAPS_D: upper case 'D'
        * CAPS_E: upper case 'E'
        * CAPS_F: upper case 'F'
        * CAPS_G: upper case 'G'
        * CAPS_H: upper case 'H'
        * CAPS_I: upper case 'I'
        * CAPS_J: upper case 'J'
        * CAPS_K: upper case 'K'
        * CAPS_L: upper case 'L'
        * CAPS_M: upper case 'M'
        * CAPS_N: upper case 'N'
        * CAPS_O: upper case 'O'
        * CAPS_P: upper case 'P'
        * CAPS_Q: upper case 'Q'
        * CAPS_R: upper case 'R'
        * CAPS_S: upper case 'S'
        * CAPS_T: upper case 'T'
        * CAPS_U: upper case 'U'
        * CAPS_V: upper case 'V'
        * CAPS_W: upper case 'W'
        * CAPS_X: upper case 'X'
        * CAPS_Y: upper case 'Y'
        * CAPS_Z: upper case 'Z'
        * ONE: '1' key
        * TWO: '2' key
        * THREE: '3' key
        * FOUR: '4' key
        * FIVE: '5' key
        * SIX: '6' key
        * SEVEN: '7' key
        * EIGHT: '8' key
        * NINE: '9' key
        * ZERO: '0' key
        * EXCLAMATION: '!' key
        * SLASH: '/' key
        * QUESTION: '?' key
        * LEFT_PARENTHESIS: '(' key
        * RIGHT_PARENTHESIS: ')' key
        * LESS_THAN: '<' key
        * GREATER_THAN: '>' key
        * Ñ: 'ñ' key
        * CAPS_Ñ: upper case 'Ñ'
        * PLUS: '+' key
        * HYPHEN_MINUS: '-' key
        * ASTERISK: '*' key
        * LEFT_BRACKET: '[' key
        * RIGHT_BRACKET: ']' key
        * LEFT_BRACE: '{' key
        * RIGHT_BRACE: '}' key
        * AMPERSAND: '&' key
        * AT: '@' key
        * DOT: '.' key
        * COMMA: ',' key
        * COLON: ':' key
        * SEMI_COLON: ';' key
        * UNDERSCORE: '_' key
        * EQUALS: '=' key
        * PIPE: '|' key
        * SPACE: spacebar key
        * CTRL_C: the ctrl + c combination
        '''
        LEFT = 1
        RIGHT = 2
        UP = 3
        DOWN = 4
        ESC = 5
        DELETE = 6
        ENTER = 7
        A = 8
        B = 9
        C = 10
        D = 11
        E = 12
        F = 13
        G = 14
        H = 15
        I_ = 16
        J = 17
        K = 18
        L = 19
        M = 20
        N = 21
        O_ = 22
        P = 23
        Q = 24
        R = 25
        S = 26
        T = 27
        U = 28
        V = 29
        W = 30
        X = 31
        Y = 32
        Z = 33
        TAB = 34
        CAPS_A = 35
        CAPS_B = 36
        CAPS_C = 37
        CAPS_D = 38
        CAPS_E = 39
        CAPS_F = 40
        CAPS_G = 41
        CAPS_H = 42
        CAPS_I = 43
        CAPS_J = 44
        CAPS_K = 45
        CAPS_L = 46
        CAPS_M = 47
        CAPS_N = 48
        CAPS_O = 49
        CAPS_P = 50
        CAPS_Q = 51
        CAPS_R = 52
        CAPS_S = 53
        CAPS_T = 54
        CAPS_U = 55
        CAPS_V = 56
        CAPS_W = 57
        CAPS_X = 58
        CAPS_Y = 59
        CAPS_Z = 60
        ONE = 61
        TWO = 62
        THREE = 63
        FOUR = 64
        FIVE = 65
        SIX = 66
        SEVEN = 67
        EIGHT = 68
        NINE = 69
        ZERO = 70
        EXCLAMATION = 71
        SLASH = 72
        QUESTION = 73
        LEFT_PARENTHESIS = 74
        RIGHT_PARENTHESIS = 75
        LESS_THAN = 76
        GREATER_THAN = 77
        Ñ = 78
        CAPS_Ñ = 79
        PLUS = 80
        HYPHEN_MINUS = 81
        ASTERISK = 82
        LEFT_BRACKET = 83
        RIGHT_BRACKET = 84
        LEFT_BRACE = 85
        RIGHT_BRACE = 86
        AMPERSAND = 87
        AT = 88
        DOT = 89
        COMMA = 90
        COLON = 91
        SEMI_COLON = 92
        UNDERSCORE = 93
        EQUALS = 94
        PIPE = 95
        SPACE = 96
        CTRL_C = 97

        _next_num = 98

        @classmethod
        def register(cls, name: str):
            '''
            Registers a key with the next available integer.

            ## Params

            name: str = the name of the key to register

            An example use would be:

            e.g.
            ```python
              from pyconsole import Keyboard


              Keyboard.Key.register("TILDE")
            ```

            Or alternatively:

            e.g.
            ```python
              from pyconsole import Keyboard


              Keyboard.Key.TILDE = Keyboard.Key.next_num
            ```
            '''
            setattr(cls, name, cls._next_num)

        def __new__(cls, value):
            def key_error():
                raise KeyNotFoundError(f"key '{value}' not registered")

            default = dir(type("dummy", (object,), {}))
            values = [x for x in inspect.getmembers(cls) if x[0] not in default]
            values = list(zip(*values))
            values = defaultdict(key_error, zip(values[1], values[0]))

            return values[value]

    def __init__(self):
        self._system = platform.system()

        def key_error():
            raise KeyNotFoundError("key not registered in keyboard")

        self._key_values = defaultdict(key_error, {
            "\r": Keyboard.Key.ENTER,
            "\t": Keyboard.Key.TAB,
            "a": Keyboard.Key.A,
            "b": Keyboard.Key.B,
            "c": Keyboard.Key.C,
            "d": Keyboard.Key.D,
            "e": Keyboard.Key.E,
            "f": Keyboard.Key.F,
            "g": Keyboard.Key.G,
            "h": Keyboard.Key.H,
            "i": Keyboard.Key.I_,
            "j": Keyboard.Key.J,
            "k": Keyboard.Key.K,
            "l": Keyboard.Key.L,
            "m": Keyboard.Key.M,
            "n": Keyboard.Key.N,
            "o": Keyboard.Key.O_,
            "p": Keyboard.Key.P,
            "q": Keyboard.Key.Q,
            "r": Keyboard.Key.R,
            "s": Keyboard.Key.S,
            "t": Keyboard.Key.T,
            "u": Keyboard.Key.U,
            "v": Keyboard.Key.V,
            "w": Keyboard.Key.W,
            "x": Keyboard.Key.X,
            "y": Keyboard.Key.Y,
            "z": Keyboard.Key.Z,
            "A": Keyboard.Key.CAPS_A,
            "B": Keyboard.Key.CAPS_B,
            "C": Keyboard.Key.CAPS_C,
            "D": Keyboard.Key.CAPS_D,
            "E": Keyboard.Key.CAPS_E,
            "F": Keyboard.Key.CAPS_F,
            "G": Keyboard.Key.CAPS_G,
            "H": Keyboard.Key.CAPS_H,
            "I": Keyboard.Key.CAPS_I,
            "J": Keyboard.Key.CAPS_J,
            "K": Keyboard.Key.CAPS_K,
            "L": Keyboard.Key.CAPS_L,
            "M": Keyboard.Key.CAPS_M,
            "N": Keyboard.Key.CAPS_N,
            "O": Keyboard.Key.CAPS_O,
            "P": Keyboard.Key.CAPS_P,
            "Q": Keyboard.Key.CAPS_Q,
            "R": Keyboard.Key.CAPS_R,
            "S": Keyboard.Key.CAPS_S,
            "T": Keyboard.Key.CAPS_T,
            "U": Keyboard.Key.CAPS_U,
            "V": Keyboard.Key.CAPS_V,
            "W": Keyboard.Key.CAPS_W,
            "X": Keyboard.Key.CAPS_X,
            "Y": Keyboard.Key.CAPS_Y,
            "Z": Keyboard.Key.CAPS_Z,
            "1": Keyboard.Key.ONE,
            "2": Keyboard.Key.TWO,
            "3": Keyboard.Key.THREE,
            "4": Keyboard.Key.FOUR,
            "5": Keyboard.Key.FIVE,
            "6": Keyboard.Key.SIX,
            "7": Keyboard.Key.SEVEN,
            "8": Keyboard.Key.EIGHT,
            "9": Keyboard.Key.NINE,
            "0": Keyboard.Key.ZERO,
            "!": Keyboard.Key.EXCLAMATION,
            "/": Keyboard.Key.SLASH,
            "?": Keyboard.Key.QUESTION,
            "(": Keyboard.Key.LEFT_PARENTHESIS,
            ")": Keyboard.Key.RIGHT_PARENTHESIS,
            "<": Keyboard.Key.LESS_THAN,
            ">": Keyboard.Key.GREATER_THAN,
            "ñ": Keyboard.Key.Ñ,
            "Ñ": Keyboard.Key.CAPS_Ñ,
            "+": Keyboard.Key.PLUS,
            "-": Keyboard.Key.HYPHEN_MINUS,
            "*": Keyboard.Key.ASTERISK,
            "[": Keyboard.Key.LEFT_BRACKET,
            "]": Keyboard.Key.RIGHT_BRACKET,
            "{": Keyboard.Key.LEFT_BRACE,
            "}": Keyboard.Key.RIGHT_BRACE,
            "&": Keyboard.Key.AMPERSAND,
            ".": Keyboard.Key.DOT,
            ",": Keyboard.Key.COMMA,
            ":": Keyboard.Key.COLON,
            ";": Keyboard.Key.SEMI_COLON,
            "_": Keyboard.Key.UNDERSCORE,
            "=": Keyboard.Key.EQUALS,
            "|": Keyboard.Key.PIPE,
            " ": Keyboard.Key.SPACE,
            "\x03": Keyboard.Key.CTRL_C
        })

        if self.system == "Windows":
            arrows = {
                "K": Keyboard.Key.LEFT,
                "M": Keyboard.Key.RIGHT,
                "H": Keyboard.Key.UP,
                "P": Keyboard.Key.DOWN
            }

            self.key_values["\x00"] = defaultdict(key_error, arrows)
            self.key_values["\x1b"] = Keyboard.Key.ESC
            self.key_values["\x08"] = Keyboard.Key.DELETE
        else:
            arrows = {
                "D": Keyboard.Key.LEFT,
                "C": Keyboard.Key.RIGHT,
                "A": Keyboard.Key.UP,
                "B": Keyboard.Key.DOWN
            }

            self.key_values["\x1b"] = defaultdict(lambda: Keyboard.Key.ESC, arrows)
            self.key_values["\x7f"] = Keyboard.Key.DELETE

    @property
    def system(self):
        return self._system

    @property
    def key_values(self):
        return self._key_values

    def register_key(self, name: str, key: str):
        '''
        Registers a key with a given string.

        ## Params

        name: str = the name you want to register the key as.

        key: str = the string representing the key.

        e.g.
        ```python
        from pyconsole import Console


        console = Console()
        console.keyboard.register_key('TILDE', '~')
        ```
        '''
        Keyboard.Key.register(name)
        self.key_values[key] = Keyboard.Key.next_num - 1
