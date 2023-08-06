from abc import ABC
from typing import Optional

from ....core.utils import _Ensure, _If
from ....model.result import Result

__all__ = ["Operation", "OpMessage", "OpDescription", "OpResult"]


class Operation(ABC):
    ...


class OpMessage(Operation):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = _Ensure.instance(message, str, "message")


class OpDescription(Operation):
    def __init__(self, description: Optional[str]) -> None:
        super().__init__()
        self.description: str = _If.not_none(_Ensure.type(description, str, "description"), lambda x: x, lambda: "")


class OpResult(Operation):
    def __init__(self, result: Result) -> None:
        super().__init__()
        self.result: Result = _Ensure.instance(result, Result, "result")
