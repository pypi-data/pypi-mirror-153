from __future__ import annotations

from enum import Enum
from typing import List, Optional

from termcolor import colored


class StringBuilder:
    class Color(Enum):
        DEFAULT = None
        GREY = "grey"
        RED = "red"
        GREEN = "green"
        YELLOW = "yellow"
        BLUE = "blue"
        MAGENTA = "magenta"
        CYAN = "cyan"
        WHITE = "white"

    def __init__(self) -> None:
        self.__content: List[str] = []

    def append(
        self,
        string: str,
        color: Color = Color.DEFAULT,
        bold: bool = False,
        end: Optional[str] = None,
    ) -> StringBuilder:
        if color == StringBuilder.Color.DEFAULT and not bold:
            self.__content.append(string)
            if not end is None:
                self.__content.append(end)
        else:
            end = "" if end is None else end
            attr = ["bold"] if bold else None
            self.__content.append(colored(string + end, color=color.value, attrs=attr))

        return self

    def __str__(self) -> str:
        return "".join(self.__content)

    def __repr__(self) -> str:
        return str(self.__content)

    def str(self) -> str:
        return self.__str__()


# Simple alias
SB = StringBuilder
