<!-- Shields -->
[![Contributors][contributors-shield]][contributors-url]
[![Stars][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Repo Size][repo-size-shield]][repo-size-url]
[![MIT License][license-shield]][license-url]

<h1 align="center">PyConsole</h1>
<h3 align="center">A (basic) cross-platform python console manager</h3>

<!-- Table of Contents -->
<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
        </li>
        <li>
            <a href="#installation">Installation</a>
        </li>
        <li>
            <a href="#usage">Usage</a>
        </li>
        <li>
            <a href="#license">License</a>
        </li>
        <li>
            <a href="#features">Features</a>
            <ul>
                <li><a href="#console">Console</a></li>
                <ul>
                    <li><a href="#cursor">Cursor</a></li>
                </ul>
                <li><a href="#keyboard">Keyboard</a></li>
                <ul>
                    <li><a href="#key">Key</a></li>
                </ul>
                <li><a href="#color">Color</a></li>
                <li><a href="#color-parser">Color Parser</a></li>
                <li><a href="#box">Box</a></li>
                <li><a href="#other">Other</a></li>
            </ul>
        </li>
        <li>
            <a href="#acknowledgements">Acknowledgements</a>
        </li>
    </ol>
</details>

<!-- About the Project -->
## About The Project

This project aims to implement a cross-platform console manager and other console related 'graphical' functions, like box containers.

It draws inpiration from the curses module and [rich](https://github.com/Textualize/rich).

<!-- Getting Started -->
## Installation

To install simply use `pip`:
* To install run
  ```bash
  pip install python-console
  ```
* To uninstall run
  ```bash
  pip uninstall python-console
  ```

<!-- Usage Examples -->
## Usage

To begin with, we can import the library with:
  ```python
  import pyconsole
  ```

Or you can import specific things like the `Console` class:
  ```python
  from pyconsole import Console
  ```

For more complete examples check the [features](#features) section or run the `test.py` file in this repository.

<!-- Features -->
## Features

The main features of this library are:
* The `Console` class
  * The `Keyboard` class
  * The `Cursor` class
* Colors with the `Color` class
* Boxes with the `Box` and `TitleBox` class
* Pretty printing exceptions, warnings and interactive sessions

If you want to know more information that is not displayed here check out the docstrings in the code or using the intellisense of your IDE.

### Console

The focus of this library is the `Console`, it can be used like so:
```python
  from pyconsole import Console


  console = Console()
```

Or it can be customized with keyword arguments:
```python
  from pyconsole import Console, RGB


  console = Console(indent=4, pass_prompt="#", color_mode=RGB)
```

The console methods are:
* print
* error
* warn
* get_key
* get_pass
* print_traceback
* clear
* command

Other useful attributes are:
* system
* color
* cursor
* keyboard
* size

Some examples:

Print colored traceback with `print_traceback`
```python
  from pyconsole import Console, RGB


  console = Console(color_mode=RGB)

  try:
      invalid = 1 / 0
  except ZeroDivisionError:
      console.print_traceback()
```

Print the registered key name from a key press
```python
  from pyconsole import Console


  console = Console()
  key = console.get_key()
  console.print("The int", key, f"represents the key '{console.keyboard.Key(key)}'")
```

Print the terminal size and the OS name
```python
  from pyconsole import Console


  console = Console()
  console.print("The console dimensions are:", console.size)
  console.print(f"The current system is: '{console.system}'")
```

#### Cursor

The cursor key can be used to modify some cursor properties.

It can be used like so:
```python
  import time

  from pyconsole import Console


  console = Console()
  console.cursor.hide()
  time.sleep(5)
  console.cursor.restore()
```

Or it can wrap around a function and restore its values in case of an error, like using Ctrl+C to stop the execution:
```python
  import time

  from pyconsole import Console


  console = Console()
  console.cursor.wrap(time.sleep, 5)
```

It can also be moved to any valid position on the screen using `move`
```python
  from pyconsole import Console


  console = Console()
  console.cursor.move(4, 1)  # 4th row, 1st column (starting from the 1st row and the 1st column)
```

### Keyboard

The keyboard is the class that's in charge of registering keys and associating them according to platform.

Registering a new key
```python
  from pyconsole import Console


  console = Console()
  console.keyboard.register_key("TILDE", "~")
```

The list of registered keys can be found when using intellisense.

#### Key

The key class is the one that does the association between key and integer, but it still needs the keyboard to know the actual symbol.

Registering a new key but omiting the keyboard instance
```python
  from pyconsole import Keyboard


  Keyboard.Key.register("TILDE")
```

Or alternatively
```python
  from pyconsole import Keyboard


  Keyboard.Key.TILDE = Keyboard.Key.next_num
```

It should be noted that it's not really recommended to do the registration this way and should use it through the keyboard instance instead.

The key class can also be instantiated from an integer to return the corresponding string representation.

Getting the key representation from a number
```python
  from pyconsole import Keyboard


  print(Keyboard.Key(1))  # prints 'LEFT' for left arrow
```

### Color

The color class is a class that abstracts the ansi escape codes used for colors and other effects, like underline. If your Windows console (like the ancient cmd.exe) does not support ansi escape sequences then consider using [colorama](https://github.com/tartley/colorama) for a fully cross platform option.

Do note that the new Windows Terminal does support colors.

You can import some basic colors and use them like:
```python
  from console import Console, RED


  console = Console()
  console.print(f"{RED}This is red text")
```

Or you can do a manual reset
```python
  from pyconsole import Console, RED, BLUE, RESET


  console = Console()
  console.print(f"{RED}This is red{RESET} and {BLUE}this is blue{RESET}", reset=False)
```

You can also create simple colors with `ColorCode`s and `ColorMod`s
```python
  from pyconsole import Console, Color, ColorCode, ColorMod


  console = Console()
  color = Color(ColorCode.CYAN, [ColorMod.UNDERLINE, ColorMod.OVERLINE])
  console.print(f"{color}Hello")
```

You can even add two colors properties together
```python
  from pyconsole import Color, ColorCode, ColorMod


  color = Color(ColorCode.YELLOW, [ColorMod.BOLD])
  color += Color(mods=[ColorMod.STRIKE])
```

Or if you want more complex colors, you can create them using rgb values
```python
  from pyconsole import Color


  color = Color.from_rgb(246, 38, 129, bg=True)  # Use bg=True for background color
```

Additionally, you can add the `__color__` method to a custom class and define how you want it to look with color
```python
  from pyconsole import Console, LIME, BLUE, RESET


  class Example:
      def __init__(self, value):
          self.value = value

      def __color__(self):
          return f"{LIME}Example{RESET}(value={BLUE}{self.value}{RESET})"


  console = Console()
  example = Example(5)
  console.print(example)  # Will print the colored string defined by '__color__'
```

### Color Parser

The color parser is the classin charge of parsing different object types to different colors.

You can register a type and a color (or even change an already existing one)
```python
  from pyconsole import Console, Color, RGB


  console = Console(color_mode=RGB)
  console.color.set_color(bytearray, Color.from_rgb(48, 25, 52))
```

And you can parse an object into a colored string
```python
  from pyconsole import Console


  console = Console()
  console.print(f"This '{console.color.parse(12)}' is an f-string colored number")
```

By default it ignores string unless it's inside a container like a dictionary, but it can be changed by passing `ignore_str=False`
```python
  from pyconsole import Console


  console = Console()
  console.print(f"A {console.color.parse('colored', ignore_str=False)} string")
```

Do note that it will returned the colored representation of the string, meaning, it will add quotes.

### Box

The `Box` and `TitleBox` classes surround your text wwith a border making a box or a titled box respectively.

You can create a box with multiple lines and border color
```python
  from pyconsole import Box, LIME


  box = Box("Multiple lines\nin one box\nwith a border color :)", color=LIME)
```

The `TitleBox` class works the same way, but with an added title
```python
  from pyconsole import TitleBox, GREEN, LIME, RESET


  box = TitleBox("A Cool Title", f"Just a box\nwith a title\nand {LIME}COLOR{RESET}", color=GREEN)
```

### Other

Some other useful functions include:
* `install_errors` for pretty error formatting all the time (no need to call `console.print_traceback` inside a try-except block)
* `install_warnings` for pretty warnings formatting
* `pretty.install` for pretty interactive session printing
* `install` for installing all of the above
* `get_console` to get the global console instance that the functions above use
* `set_console` to change the global console properties

<!-- License -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Acknowledgements -->
## Acknowledgements

None of the following are associated with the project in any way. They are mentioned as a source of 
learning and inspiration for parts of this project.

* [Rich](https://github.com/Textualize/rich)

<!-- Links -->
[contributors-shield]: https://img.shields.io/github/contributors/DaHunterTime/PyConsole.svg?style=for-the-badge
[contributors-url]: https://github.com/DaHunterTime/PyConsole/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/DaHunterTime/PyConsole.svg?style=for-the-badge
[stars-url]: https://github.com/DaHunterTime/PyConsole/stargazers
[issues-shield]: https://img.shields.io/github/issues/DaHunterTime/PyConsole.svg?style=for-the-badge
[issues-url]: https://github.com/DaHunterTime/PyConsole/issues
[repo-size-shield]: https://img.shields.io/github/repo-size/DaHunterTime/PyConsole.svg?style=for-the-badge
[repo-size-url]: https://github.com/DaHunterTime/PyConsole/archive/refs/heads/main.zip
[license-shield]: https://img.shields.io/github/license/DaHunterTime/PyConsole.svg?style=for-the-badge
[license-url]: https://github.com/DaHunterTime/PyConsole/blob/main/LICENSE