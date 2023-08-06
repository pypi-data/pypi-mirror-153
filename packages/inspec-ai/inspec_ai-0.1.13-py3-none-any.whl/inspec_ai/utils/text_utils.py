from colorama import init as colorama_init, Fore

from inspec_ai.utils.utils import _StrEnum
from typing import List


class Color(_StrEnum):
    GREEN = "green"
    RED = "red"


def enumerate_elements_in_a_sentence(str_items: List[str]) -> str:
    if len(str_items) == 1:
        return str_items[0]

    tmp = ", ".join(str_items[:-1])
    tmp += " and "
    tmp += str_items[-1]

    return tmp


def color_text_for_console(string: str, color: Color) -> str:
    """Adds the code to color the python console output when called with the print function."""
    colorama_init()  # To enable ANSI escape character sequences (for color) on Windows

    python_terminal_color_codes = {Color.GREEN: Fore.GREEN, Color.RED: Fore.RED}

    color_code = python_terminal_color_codes[color]

    return color_code + string + Fore.RESET
