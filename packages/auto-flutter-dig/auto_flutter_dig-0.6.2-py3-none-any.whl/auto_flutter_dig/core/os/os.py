from __future__ import annotations

from enum import Enum
from sys import platform


class OS(Enum):
    UNKNOWN = 0
    WINDOWS = 1
    LINUX = 2
    MAC = 3

    @staticmethod
    def current() -> OS:
        if platform.startswith("win32") or platform.startswith("cygwin"):
            return OS.WINDOWS
        if platform.startswith("linux"):
            return OS.LINUX
        if platform.startswith("darwin"):
            return OS.MAC
        return OS.UNKNOWN
