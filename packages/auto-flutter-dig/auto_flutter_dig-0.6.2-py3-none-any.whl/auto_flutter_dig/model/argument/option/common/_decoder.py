from abc import abstractmethod
from typing import Callable, Generic, Optional, TypeVar

from .....model.argument.arguments import Args
from .....model.argument.option.option import Option

T_co = TypeVar("T_co", covariant=True)  # pylint: disable=invalid-name

__all__ = ["_DecodedOption"]


class _DecodedOption(Option, Generic[T_co]):
    def get(self, args: Args) -> T_co:
        value = args.get(self)
        if value is None:
            raise ValueError("Check if option exists before getting")
        return self._convert(value)

    def get_or_default(self, args: Args, default: Callable[[], T_co]) -> T_co:
        value = args.get(self)
        if value is None:
            return default()
        return self._convert(value)

    def get_or_none(self, args: Args) -> Optional[T_co]:
        value = args.get(self)
        if value is None:
            return None
        return self._convert(value)

    @abstractmethod
    def _convert(self, value: str) -> T_co:
        raise NotImplementedError()
