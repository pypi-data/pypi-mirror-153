from .....model.argument.option.common._decoder import _DecodedOption
from .....model.argument.option.long import LongOptionWithValue
from .....model.build.type import BuildType

__all__ = ["BuildTypeFlutterOption", "BuildTypeOutputOption"]


class BuildTypeFlutterOption(LongOptionWithValue, _DecodedOption[BuildType]):
    def __init__(self, description: str) -> None:
        LongOptionWithValue.__init__(self, "build-type", description)
        _DecodedOption.__init__(self, description)

    def _convert(self, value: str) -> BuildType:
        return BuildType.from_flutter(value)


class BuildTypeOutputOption(LongOptionWithValue, _DecodedOption[BuildType]):
    def __init__(self, description: str) -> None:
        LongOptionWithValue.__init__(self, "build-type", description)
        _DecodedOption.__init__(self, description)

    def _convert(self, value: str) -> BuildType:
        return BuildType.from_output(value)
