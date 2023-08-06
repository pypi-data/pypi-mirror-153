from .....model.argument.option.common._decoder import _DecodedOption
from .....model.argument.option.long_short import LongShortOptionWithValue
from .....model.project.flavor import Flavor

__all__ = ["FlavorOption"]


class FlavorOption(LongShortOptionWithValue, _DecodedOption[Flavor]):
    def __init__(self, description: str) -> None:
        LongShortOptionWithValue.__init__(self, "f", "flavor", description)
        _DecodedOption.__init__(self, description)

    def _convert(self, value: str) -> Flavor:
        return value
