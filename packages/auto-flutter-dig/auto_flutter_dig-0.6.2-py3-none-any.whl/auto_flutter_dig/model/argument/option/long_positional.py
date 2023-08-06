from typing import Tuple

from ....model.argument.option.long import LongOptionWithValue
from ....model.argument.option.positional import PositionalOption

__all__ = ["LongPositionalOption"]


class LongPositionalOption(LongOptionWithValue, PositionalOption):
    def __init__(self, long: str, position: int, description: str) -> None:
        LongOptionWithValue.__init__(self, long, "")
        PositionalOption.__init__(self, position, long, description)

    def describe(self) -> Tuple[str, str]:
        return ("--" + self.long, self.description)
