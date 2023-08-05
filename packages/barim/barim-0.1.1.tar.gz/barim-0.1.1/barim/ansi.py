from enum import Enum
from typing import List, Union


class Color(Enum):
    """
    Sets of predefined 8 bits colors
    """

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

    def __str__(self) -> str:
        return self.value


class Style(Enum):
    """
    Sets of predefined 8 bits styling
    """

    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    RESET = "\033[0m"

    def __str__(self) -> str:
        return self.value


def fg_from_id(id_: int) -> str:
    """
    Apply foreground color (8 bits) based of the provided ID

    :param id_: int
    :return: str
    """
    return f"\033[38;5;{id_}m"


def bg_from_id(id_: int) -> str:
    """
    Apply background color (8 bits) based of the provided ID

    :param id_: int
    :return: str
    """
    return f"\033[48;5;{id_}m"


def fg_from_rgb(r: int, g: int, b: int) -> str:
    """
    Apply foreground color (24 bits) based of the provided RGB value

    :param r: int
    :param g: int
    :param b: int
    :return: str
    """
    return f"\033[38;2;{r};{g};{b}m"


def bg_from_rgb(r: int, g: int, b: int) -> str:
    """
    Apply background color (24 bits) based of the provided RGB value

    :param r: int
    :param g: int
    :param b: int
    :return: str
    """
    return f"\033[48;2;{r};{g};{b}m"


def wrap(code: Union[Color, Style, str], text: str) -> str:
    """
    Apply color or style on a text and reset it

    :param code: Union[Color, Style, str]
    :param text: str
    :return: str
    """
    return f"{code}{text}{Style.RESET}"


def wraps(codes: List[Union[Color, Style, str]], text: str) -> str:
    """
    Applies multiple colors or styles to a given text and reset it

    :param codes: List[Union[Color, Style, str]]
    :param text: str
    :return: str
    """
    return f"{''.join([str(code) for code in codes])}{text}{Style.RESET}"


def success(text: str) -> str:
    """
    Apply a green color to the provided text

    :param text: str
    :return: str
    """
    return wraps([Style.BOLD, Color.GREEN], text)


def error(text: str) -> str:
    """
    Apply a red color to the provided text

    :param text: str
    :return: str
    """
    return wraps([Style.BOLD, Color.RED], text)


def warning(text: str) -> str:
    """
    Apply an orange color to the provided text

    :param text: str
    :return: str
    """
    return wraps([Style.BOLD, fg_from_id(202)], text)
