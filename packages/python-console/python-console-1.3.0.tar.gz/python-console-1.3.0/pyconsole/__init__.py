'''
# PyConsole

The `pyconsole` module from the `python-console` package.

It contains multiple features like:
* A `Console` class for pretty printing and otherr utilities.
* Colors
* Keyboard key press detection
* pretty printing for errors, warnings and interactive mode
* `Box` and `TitleBox` classes for container printing

## Usage

The module can ve imported and used as follows:

e.g. print 'Hello, World!' in blue
```python
  from pyconsole import Console, BLUE


  console = Console()
  console.print(f"{BLUE}Hello, World!")
```

## Imports

All the things that you can import, grouped by 'theme', are:
* Console
* Color, ColorCode, ColorMod
  * RESET, RED, BLUE, LIME, YELLOW, CYAN, WHITE, BOLD, GREEN, GRAY, UNDERLINE, BRIGHT_WHITE
* ColorParser, SIMPLE, RGB
* Keyboard
* KeyboardWarning, KeyNotFoundError, TracebackWarning
* get_console, set_console
* Box, TitleBox
* install_warnings, install_errors
* colorwrap
* pretty
* install
'''

from .console import Console
from .color import Color, ColorCode, ColorMod, RESET, RED, BLUE, LIME, YELLOW, CYAN, WHITE, BOLD, \
                   GREEN, GRAY, UNDERLINE, BRIGHT_WHITE
from .color_parser import ColorParser, SIMPLE, RGB
from .keyboard import Keyboard
from .errors import KeyboardWarning, KeyNotFoundError, TracebackWarning
from .global_data import get_console, set_console
from .table import Box, TitleBox
from .color_traceback import install_warnings, install_errors
from . import colorwrap, pretty
from .functions import install
