from .....core.utils import _Enum
from .....model.argument.option.common._decoder import _DecodedOption
from .....model.argument.option.long import LongOptionWithValue
from .....model.build.mode import BuildMode

__all__ = ["BuildModeOption"]


class BuildModeOption(LongOptionWithValue, _DecodedOption[BuildMode]):
    def __init__(self, description: str) -> None:
        LongOptionWithValue.__init__(self, "build-mode", description)
        _DecodedOption.__init__(self, description)

    def _convert(self, value: str) -> BuildMode:
        return _Enum.parse_value(BuildMode, value)
