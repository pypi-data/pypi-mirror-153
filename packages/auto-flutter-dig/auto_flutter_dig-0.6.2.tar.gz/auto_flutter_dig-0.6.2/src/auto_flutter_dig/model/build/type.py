from __future__ import annotations

from enum import Enum

from ...core.utils import _Ensure, _Enum
from ...model.platform.platform import Platform


class _BuildTypeItem:
    def __init__(self, flutter: str, output: str, platform: Platform) -> None:
        self.flutter: str = _Ensure.instance(flutter, str, "flutter")
        self.output: str = _Ensure.instance(output, str, "output")
        self.platform: Platform = _Ensure.instance(platform, Platform, "platform")


class BuildType(Enum):
    AAR = _BuildTypeItem("aar", "aar", Platform.ANDROID)
    APK = _BuildTypeItem("apk", "apk", Platform.ANDROID)
    BUNDLE = _BuildTypeItem("appbundle", "aab", Platform.ANDROID)
    IPA = _BuildTypeItem("ios", "ipa", Platform.IOS)

    @property
    def flutter(self) -> str:
        return self.value.flutter

    @property
    def output(self) -> str:
        return self.value.output

    @property
    def platform(self) -> Platform:
        return self.value.platform

    @staticmethod
    def from_flutter(value: str) -> BuildType:
        _Ensure.not_none(value, "value")
        return _Enum.parse_value(BuildType, value, lambda x: x.flutter)

    @staticmethod
    def from_output(value: str) -> BuildType:
        _Ensure.not_none(value, "value")
        return _Enum.parse_value(BuildType, value, lambda x: x.output)
