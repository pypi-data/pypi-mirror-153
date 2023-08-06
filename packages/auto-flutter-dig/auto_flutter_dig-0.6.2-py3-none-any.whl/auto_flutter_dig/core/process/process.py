from __future__ import annotations

from abc import ABC, abstractmethod
from os import environ
from pathlib import PurePath, PurePosixPath
from typing import Callable, Dict, List, Optional, Union

from ...core.os.path_converter import PathConverter
from ...core.utils import _Ensure, _EnsureCallable


class Process(ABC):
    active: List[Process] = []

    @staticmethod
    def create(
        executable: Union[str, PurePath],
        arguments: Optional[List[str]] = None,
        environment: Optional[Dict[str, str]] = None,
        writer: Optional[Callable[[str], None]] = None,
        inherit_environment: bool = True,
    ) -> Process:
        # Avoid circular import
        from .subprocess import _SubProcess  # pylint: disable=import-outside-toplevel,cyclic-import

        return _SubProcess(executable, arguments, environment, writer, inherit_environment)

    def __init__(
        self,
        executable: Union[str, PurePath],
        arguments: Optional[List[str]] = None,
        environment: Optional[Dict[str, str]] = None,
        writer: Optional[Callable[[str], None]] = None,
        inherit_environment: bool = True,
    ) -> None:
        _Ensure.not_none(executable, "executable")
        _Ensure.type(executable, (str, PurePath), "executable")
        _Ensure.type(arguments, List, "arguments")
        _Ensure.type(environment, Dict, "environment")
        _EnsureCallable.type(writer, "writer")
        _Ensure.type(inherit_environment, bool, "inherit_environment")
        self.output: Optional[str] = None
        self.exit_code: int = -1

        self._executable: PurePath = PathConverter.from_path(
            executable if isinstance(executable, PurePath) else PurePosixPath(executable)
        ).to_machine()
        environment = {} if environment is None else environment
        if inherit_environment:
            current_env = environ.copy()
            self._environment = {**current_env, **environment}
        else:
            self._environment = environment
        self._arguments = [] if arguments is None else arguments
        self._writer = writer
        self.__writer_buffer: str = ""

    def _write_output(self, message: str):
        if self._writer is None:
            return
        self.__writer_buffer += message
        index = self.__writer_buffer.rfind("\n")
        if index != -1:
            self._writer(self.__writer_buffer[:index])
            if index + 1 >= len(self.__writer_buffer):
                self.__writer_buffer = ""
            else:
                self.__writer_buffer = self.__writer_buffer[index + 1]

    def try_run(self) -> Union[bool, BaseException]:
        try:
            self.run()
        except BaseException as error:
            return error
        return self.exit_code == 0

    @abstractmethod
    def run(self):
        raise NotImplementedError("This method must be implemented")

    @abstractmethod
    def stop(self):
        raise NotImplementedError("This method must be implemented")

    @abstractmethod
    def kill(self):
        raise NotImplementedError("This method must be implemented")

    @property
    @abstractmethod
    def is_running(self) -> bool:
        raise NotImplementedError("This method must be implemented")

    def _process_started(self):
        Process.active.append(self)

    def _process_stopped(self):
        Process.active.remove(self)

    class ChildProcessStopped(ChildProcessError):
        ...

    class ChildProcessKilled(ChildProcessStopped):
        ...
