from typing import Any, Dict, Optional

from ...core.json.type import Json
from ...model.platform.flavored_config import Flavor, PlatformConfig, PlatformConfigFlavored

__all__ = [
    "MergePlatformConfigFlavored",
    "PlatformConfigFlavored",
    "Flavor",
]


class _MergedPlatformConfig(PlatformConfig):
    def __init__(
        self,
        default: Optional[PlatformConfigFlavored],
        platform: Optional[PlatformConfigFlavored],
        flavor: Optional[Flavor],
    ) -> None:
        super().__init__(None, None, None, None, None)
        if not default is None:
            self._merge(default)
            if not flavor is None:
                config = default.get_config_by_flavor(flavor)
                if not config is None:
                    self._merge(config)
        if not platform is None:
            self._merge(platform)
            if not flavor is None:
                config = platform.get_config_by_flavor(flavor)
                if not config is None:
                    self._merge(config)

    def append_build_param(self, param: str):
        raise AssertionError(f"{type(self).__name__} is read only")

    def remove_build_param(self, param: str) -> bool:
        raise AssertionError(f"{type(self).__name__} is read only")

    def add_extra(self, key: str, value: str):
        raise AssertionError(f"{type(self).__name__} is read only")

    def remove_extra(self, key: str) -> bool:
        raise AssertionError(f"{type(self).__name__} is read only")

    def to_json(self) -> Json:
        raise AssertionError(f"{type(self).__name__} is read only")

    @staticmethod
    def from_json(json: Json) -> Optional[Any]:
        raise AssertionError(f"{_MergedPlatformConfig.__name__} is read only")


class MergePlatformConfigFlavored(PlatformConfigFlavored):
    def __init__(
        self,
        default: Optional[PlatformConfigFlavored],
        platform: Optional[PlatformConfigFlavored],
    ) -> None:
        super().__init__()
        self.default = default
        self.platform = platform
        self.__cached: Dict[Flavor, _MergedPlatformConfig] = {}

    def append_build_param(self, param: str):
        raise AssertionError(f"{type(self).__name__} is read only")

    def remove_build_param(self, param: str) -> bool:
        raise AssertionError(f"{type(self).__name__} is read only")

    def add_extra(self, key: str, value: str):
        raise AssertionError(f"{type(self).__name__} is read only")

    def remove_extra(self, key: str) -> bool:
        raise AssertionError(f"{type(self).__name__} is read only")

    def to_json(self) -> Json:
        raise AssertionError(f"{type(self).__name__} is read only")

    @staticmethod
    def from_json(json: Json) -> Optional[Any]:
        raise AssertionError(f"{MergePlatformConfigFlavored.__name__} is read only")

    def get_config_by_flavor(self, flavor: Optional[Flavor]) -> PlatformConfig:
        key = self.__get_cache_key(flavor)
        if key in self.__cached:
            return self.__cached[key]
        config = _MergedPlatformConfig(self.default, self.platform, flavor)
        self.__cached[key] = config
        return config

    def obtain_config_by_flavor(self, flavor: Optional[Flavor]) -> PlatformConfig:
        return self.get_config_by_flavor(flavor)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(default={self.default}, platform={self.platform})"

    @staticmethod
    def __get_cache_key(flavor: Optional[Flavor]) -> Flavor:
        if flavor is None:
            return "-#-#-"
        return flavor
