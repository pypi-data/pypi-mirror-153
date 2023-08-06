from abc import ABC, abstractmethod
from typing import Tuple

from ....core.utils import _Ensure

__all__ = ["Option"]


class Option(ABC):
    def __init__(self, description: str) -> None:
        super().__init__()
        self.description: str = _Ensure.instance(description, str, "description")

    @abstractmethod
    def describe(self) -> Tuple[str, str]:
        raise NotImplementedError("Require to implement Option.describe()")

    def __str__(self) -> str:
        return str(self.describe())
