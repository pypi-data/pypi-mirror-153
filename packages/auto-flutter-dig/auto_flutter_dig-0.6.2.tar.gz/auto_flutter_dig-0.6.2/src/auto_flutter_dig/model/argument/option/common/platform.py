from .....core.utils import _Enum
from .....model.argument.option.common._decoder import _DecodedOption
from .....model.argument.option.long import LongOptionWithValue
from .....model.platform.platform import Platform

__all__ = ["PlatformOption"]


class PlatformOption(LongOptionWithValue, _DecodedOption[Platform]):
    def __init__(self, description: str) -> None:
        LongOptionWithValue.__init__(self, "platform", description)
        _DecodedOption.__init__(self, description)

    def _convert(self, value: str) -> Platform:
        return _Enum.parse_value(Platform, value)
