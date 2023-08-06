from typing import Tuple

from ....model.argument.option.option import Option

__all__ = ["OptionAll"]


class OptionAll(Option):
    def __init__(self) -> None:
        super().__init__("")

    def describe(self) -> Tuple[str, str]:
        return ("", "Accept everything")
