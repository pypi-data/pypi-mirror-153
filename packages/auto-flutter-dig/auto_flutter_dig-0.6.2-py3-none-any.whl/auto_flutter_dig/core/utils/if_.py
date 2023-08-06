from abc import ABC
from typing import Callable, Optional, TypeVar

from ...core.utils.ensure import _EnsureCallable


class _If(ABC):
    T = TypeVar("T")
    V = TypeVar("V")

    @staticmethod
    def none(value: Optional[T], positive: Callable[[], V], negative: Callable[[T], V]) -> V:
        _EnsureCallable.instance(positive, "positive")
        _EnsureCallable.instance(negative, "negative")

        if value is None:
            return positive()
        return negative(value)

    @staticmethod
    def not_none(value: Optional[T], positive: Callable[[T], V], negative: Callable[[], V]) -> V:
        _EnsureCallable.instance(positive, "positive")
        _EnsureCallable.instance(negative, "negative")

        if value is None:
            return negative()
        return positive(value)
