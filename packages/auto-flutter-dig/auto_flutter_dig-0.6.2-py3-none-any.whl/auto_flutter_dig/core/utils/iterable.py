from __future__ import annotations

from abc import ABC
from typing import Callable, Iterable, Iterator, List, Optional, Tuple, Type, TypeVar


class _Iterable(ABC):
    T = TypeVar("T")
    T_co = TypeVar("T_co", covariant=True)

    @staticmethod
    def first_or_none(iterable: Iterable[T], condition: Callable[[T], bool]) -> Optional[T]:
        for item in iterable:
            if condition(item):
                return item
        return None

    @staticmethod
    def first_or_default(iterable: Iterable[T], condition: Callable[[T], bool], fallback: Callable[[], T]) -> T:
        for item in iterable:
            if condition(item):
                return item
        return fallback()

    @staticmethod
    def flatten(iterable: Iterable[Iterable[T]]) -> List[T]:
        return [item for sublist in iterable for item in sublist]

    @staticmethod
    def count(iterable: Iterable[T]) -> int:
        out = 0
        for _ in iterable:
            out += 1
        return out

    @staticmethod
    def is_empty(iterable: Iterable[T]) -> bool:
        for _ in iterable:
            return False
        return True

    class Flatten(Iterator[T]):
        def __init__(self, iterable: Iterable[Iterable[_Iterable.T]]) -> None:
            super().__init__()
            self.__iterables = iterable.__iter__()
            self.__current: Optional[Iterator[_Iterable.T]] = None

        def __next__(self) -> _Iterable.T:
            while True:
                if self.__current is None:
                    self.__current = next(self.__iterables).__iter__()
                try:
                    return next(self.__current)
                except StopIteration:
                    self.__current = None
                    continue

    class FilterOptional(Iterator[T]):
        def __init__(self, iterable: Iterable[Optional[_Iterable.T]]) -> None:
            super().__init__()
            self._iter = iterable.__iter__()

        def __next__(self) -> _Iterable.T:
            while True:
                out = next(self._iter)
                if not out is None:
                    return out

    K = TypeVar("K")

    class FilterTupleOptional(Iterator[Tuple[K, T]]):
        def __init__(self, iterable: Iterable[Tuple[_Iterable.K, Optional[_Iterable.T]]]) -> None:
            super().__init__()
            self._iter = iterable.__iter__()

        def __next__(self) -> Tuple[_Iterable.K, _Iterable.T]:
            while True:
                out = next(self._iter)
                if not out[1] is None:
                    return (out[0], out[1])

    class Merge(Iterable[T]):
        def __init__(self, *iterables: Iterable[_Iterable.T]) -> None:
            super().__init__()
            self.__flatten = _Iterable.Flatten(iterables)

        def __iter__(self) -> Iterator[_Iterable.T]:
            return self.__flatten

    class Apply(Iterator[T_co]):
        def __init__(
            self,
            iterable: Iterable[_Iterable.T_co],
            apply: Callable[[_Iterable.T_co], None],
        ) -> None:
            super().__init__()
            self.__iterator = iterable.__iter__()
            self.__apply = apply

        def __next__(self) -> _Iterable.T_co:
            item = next(self.__iterator)
            self.__apply(item)
            return item

    class FilterInstance(Iterator[T_co]):
        def __init__(self, iterable: Iterable[_Iterable.T], cls: Type[_Iterable.T_co]) -> None:
            super().__init__()
            self.__iterator = iterable.__iter__()
            self.__cls = cls

        def __next__(self) -> _Iterable.T_co:
            while True:
                out = next(self.__iterator)
                if isinstance(out, self.__cls):
                    return out
