from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Union

from ...core.os.os import OS
from ...core.utils import _Ensure

__all__ = ["PathConverter"]


class PathConverter(ABC):
    def __init__(self, path: PurePosixPath) -> None:
        self._path: PurePosixPath = _Ensure.instance(path, PurePosixPath, "path")

    @staticmethod
    def from_posix(path: PurePosixPath) -> PathConverter:
        _Ensure.not_none(path, "path")
        if isinstance(path, PurePosixPath):
            return _PathConverter(path)
        return PathConverter.from_path(path)

    @staticmethod
    def from_machine(path: PurePath) -> PathConverter:
        if isinstance(path, PurePosixPath):
            return _PathConverter(path)

        if not path.is_absolute():
            return _PathConverter(PurePosixPath(path.as_posix()))

        output = PurePosixPath("/" + path.drive[:1])
        for i, segment in enumerate(path.parts):
            if i == 0:
                continue
            output = output.joinpath(segment)
        return _PathConverter(output)

    @staticmethod
    def from_path(path: Union[str, PurePath]) -> PathConverter:
        _Ensure.not_none(path, "path")
        if isinstance(path, str):
            path = PurePath(path)
        if isinstance(path, PurePosixPath):
            return _PathConverter(path)
        return PathConverter.from_machine(path)

    def to_posix(self) -> PurePosixPath:
        return self._path

    def to_machine(self) -> PurePath:
        if OS.current() != OS.WINDOWS:
            return self._path

        if not self._path.is_absolute():
            if len(self._path.parts) == 1:
                return PureWindowsPath(self._path)

            first = self._path.parts[0]
            if not (len(first) == 2 and first[1] == ":"):
                return PureWindowsPath(self._path)

        output = PureWindowsPath()
        for segment in self._path.parts:
            if len(output.drive) == 0:
                if segment == "/":
                    pass
                if len(segment) > 2:
                    raise AssertionError(f'Can not find driver letter from path "{self._path}"')
                if len(segment) == 1:
                    output = PureWindowsPath(segment + ":")
                elif segment[1] != ":":
                    raise AssertionError(f'Unrecognized driver letter from path "{self._path}"')
                else:
                    output = PureWindowsPath(segment)
                continue

            if len(output.parts) == 1:
                # First join path does not include separator.. why?
                output = output.joinpath("/" + segment)
            else:
                output = output.joinpath(segment)
        return output

    @abstractmethod
    def __none(self) -> None:  # pylint:disable=unused-private-member
        # Used to avoid user instantiate class wthout creators
        pass


class _PathConverter(PathConverter):
    def __none(self) -> None:  # pylint:disable=unused-private-member
        pass
