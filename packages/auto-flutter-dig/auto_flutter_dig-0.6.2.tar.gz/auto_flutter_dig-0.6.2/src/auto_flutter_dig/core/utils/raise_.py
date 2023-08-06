from __future__ import annotations

from typing import NoReturn


class _Raise:
    def __init__(self, error: BaseException) -> None:
        self._error = error

    def throw(self, *args) -> NoReturn:
        raise self._error
