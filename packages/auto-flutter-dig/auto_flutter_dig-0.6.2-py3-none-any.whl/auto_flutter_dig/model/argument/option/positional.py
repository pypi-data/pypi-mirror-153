from typing import Tuple

from ....core.utils import _Ensure
from ....model.argument.option.valued import OptionWithValue

__all__ = ["PositionalOption"]


class PositionalOption(OptionWithValue):
    def __init__(self, position: int, name: str, description: str) -> None:
        super().__init__(description)
        self.name: str = _Ensure.instance(name, str, "name")
        self.position: int = _Ensure.instance(position, int, "position")

    def describe(self) -> Tuple[str, str]:
        return ("{{" + self.name + "}}", self.description)
