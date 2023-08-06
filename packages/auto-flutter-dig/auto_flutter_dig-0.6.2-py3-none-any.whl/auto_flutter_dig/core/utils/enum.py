from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Callable, Type, TypeVar

from ...core.utils.iterable import _Iterable


class _Enum(ABC):
    E = TypeVar("E", bound=Enum)
    V = TypeVar("V")

    @staticmethod
    def parse_value(enum: Type[E], value: V, field: Callable[[E], V] = lambda x: x.value) -> E:
        output = _Iterable.first_or_none(enum.__iter__(), lambda x: field(x) == value)
        if output is None:
            raise ValueError(f"Value `{value}` not found in enum `{enum.__name__}`")
        return output

    @staticmethod
    def parse(enum: Type[E], field: Callable[[E], V] = lambda x: x.value) -> Callable[[V], E]:
        return lambda value: _Enum.parse_value(enum, value, field)
