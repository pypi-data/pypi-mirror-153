import os
from abc import ABC, abstractmethod
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from typing import Iterable, Optional

from ...core.os.os import OS
from ...core.utils import _Iterable

__all__ = ["ExecutableResolver"]


class ExecutableResolver(ABC):
    @abstractmethod
    def __none(self) -> None:  # pylint: disable=unused-private-member
        # Just prevent to someone try to instantiate this class directly
        pass

    @staticmethod
    def is_executable(path: PurePath) -> bool:
        if OS.current() == OS.WINDOWS:
            return path.suffix.lower() in (".exe", ".bat", ".cmd")
        return os.access(path, os.X_OK)

    @staticmethod
    def get_executable(path: PurePath) -> Path:
        _path = Path(path)
        ## Fast mode
        if ExecutableResolver.is_executable(_path):
            print(type(path))
            if _path.exists():
                return _path
            raise FileNotFoundError(f"Executable not found: {_path}")

        ## Test others variants for windows
        if OS.current() == OS.WINDOWS:
            for suffix in (".exe", ".bat", ".cmd"):
                _path = _path.with_suffix(suffix)
                if _path.exists():
                    return _path
            raise FileNotFoundError(f"Executable not found: {_path}")

        ## Test others variants
        for suffix in ("", ".sh"):
            _path = _path.with_suffix(suffix)
            if _path.exists() and ExecutableResolver.is_executable(_path):
                return _path
        raise FileNotFoundError(f"Executable not found: {_path}")

    @staticmethod
    def resolve_executable(path: PurePath) -> PurePath:
        if path.is_absolute():
            # Already absolute
            try:
                return ExecutableResolver.get_executable(path)
            except BaseException as error:
                raise LookupError(f'Failed to get absolute executable for "{path}"') from error

        if (isinstance(path, PurePosixPath) and path.parent != PurePosixPath(".")) or (
            isinstance(path, PureWindowsPath) and path.parent != PureWindowsPath(".")
        ):
            # Is relative
            try:
                _path = ExecutableResolver.get_executable(path)
                return _path.resolve()
            except BaseException as error:
                raise LookupError(f'Failed to get relative executable for "{path}"') from error

        # Then can be at current local or in sys path
        # First try sys path
        for root in ExecutableResolver.get_sys_path():
            try:
                _path = ExecutableResolver.get_executable(root / path)
                # Executable is in path
                return PurePath(_path.name)
            except BaseException:
                pass

        # Not in path, try at current local
        try:
            _path = ExecutableResolver.get_executable(path)
            return _path.absolute()
        except BaseException as error:
            raise LookupError(f'Failed to get current local executable for "{path}"') from error

    @staticmethod
    def get_sys_path() -> Iterable[Path]:
        splitted = ExecutableResolver.__get_sys_path().split(os.pathsep)
        mapped = map(ExecutableResolver.__try_create_path, splitted)
        not_none = _Iterable.FilterOptional(mapped)
        return filter(lambda x: x.exists(), not_none)

    @staticmethod
    def __try_create_path(path: str) -> Optional[Path]:
        try:
            return Path(path)
        except BaseException:
            return None

    @staticmethod
    def __get_sys_path() -> str:
        if "PATH" in os.environ:
            return os.environ["PATH"]
        if "path" in os.environ:
            return os.environ["path"]
        if "Path" in os.environ:
            return os.environ["Path"]
        for key, value in os.environ.items():
            if key.lower() == "path":
                return value
        return ""
