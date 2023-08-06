from __future__ import annotations

from typing import Dict, List, Optional

from ...core.json.codec import JsonDecode, JsonEncode
from ...core.json.serializable import Json, Serializable
from ...model.platform.config import BuildType, PlatformConfig, RunType, TaskIdList
from ...model.project.flavor import Flavor

__all__ = [
    "PlatformConfigFlavored",
    "PlatformConfig",
    "RunType",
    "BuildType",
    "TaskIdList",
    "Flavor",
]


class PlatformConfigFlavored(PlatformConfig, Serializable["PlatformConfigFlavored"]):
    def __init__(
        self,
        build_param: Optional[List[str]] = None,
        run_before: Optional[Dict[RunType, TaskIdList]] = None,
        output: Optional[str] = None,
        outputs: Optional[Dict[BuildType, str]] = None,
        extras: Optional[Dict[str, str]] = None,
        flavored: Optional[Dict[Flavor, PlatformConfig]] = None,
    ) -> None:
        super().__init__(build_param, run_before, output, outputs, extras)
        self.flavored: Optional[Dict[Flavor, PlatformConfig]] = flavored

    def to_json(self) -> Json:
        parent = super().to_json()
        if not isinstance(parent, Dict):
            raise AssertionError("PlatformConfig must return Dict as json")
        if not self.flavored is None:
            flavored = {"flavored": JsonEncode.encode(self.flavored)}
            return {**parent, **flavored}
        return parent

    @staticmethod
    def from_json(json: Json) -> Optional[PlatformConfigFlavored]:
        output = PlatformConfigFlavored()
        other = PlatformConfig.from_json(json)
        if not other is None:
            output._merge(other)  # pylint:  disable=protected-access
        if isinstance(json, Dict):
            if "flavored" in json:
                output.flavored = JsonDecode.decode_optional_dict(json["flavored"], Flavor, PlatformConfig)
        return output

    def get_config_by_flavor(self, flavor: Optional[Flavor]) -> Optional[PlatformConfig]:
        if flavor is None:
            return self
        if self.flavored is None:
            return None
        if not flavor in self.flavored:
            return None
        return self.flavored[flavor]

    def obtain_config_by_flavor(self, flavor: Optional[Flavor]) -> PlatformConfig:
        if flavor is None:
            return self
        if self.flavored is None:
            self.flavored = {}
        if not flavor in self.flavored:
            self.flavored[flavor] = PlatformConfig()
        return self.flavored[flavor]

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", flavored={self.flavored})"
