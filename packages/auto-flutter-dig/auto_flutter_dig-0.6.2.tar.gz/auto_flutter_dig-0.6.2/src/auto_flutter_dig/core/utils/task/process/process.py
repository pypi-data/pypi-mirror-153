from abc import abstractmethod
from pathlib import Path, PurePath, PurePosixPath
from typing import Dict, Iterable, Optional, Union

from .....core.config import Config
from .....core.os.path_converter import PathConverter
from .....core.process.process import Process
from .....core.string import SF
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.config.const import AFLUTTER_CONFIG_PRINT_PROCESS_CONTENT

__all__ = [
    "Process",
    "BaseProcessTask",
    "ProcessOrResult",
]

ProcessOrResult = Union[Process, TaskResult]


class BaseProcessTask(Task):
    def __init__(self, ignore_failure: bool = False, show_output_at_end: bool = False) -> None:
        super().__init__()
        self._process: Process
        self._ignore_failure: bool = ignore_failure
        self._show_output_at_end: bool = show_output_at_end
        self._can_print_content = Config.get_bool(AFLUTTER_CONFIG_PRINT_PROCESS_CONTENT)

    def execute(self, args: Args) -> TaskResult:
        process = self._create_process(args)
        if isinstance(process, TaskResult):
            return process
        self._process = process
        output = self._process.try_run()
        return self._handle_process_output(args, self._process, output)

    def _print_content(self, message: Optional[str]):
        if message is None:
            return
        if self._can_print_content:
            self._print(message)
        else:
            self.log.debug(message)

    @staticmethod
    def _sanitize_arguments(
        arguments: Iterable[str],
        args: Args,
        extras: Optional[Dict[str, str]] = None,
        expand_args: bool = True,
        expand_path: bool = False,
    ) -> List[str]:
        output: List[str] = []
        for argument in arguments:
            if expand_args:
                argument = SF.format(argument, args, extras)
            if argument.startswith("./"):
                path: PurePath = PurePosixPath(argument)
                path = PathConverter.from_path(path).to_machine()
                if expand_path:
                    path = Path(path).absolute()
                argument = str(path)
            output.append(argument)
        return output

    @abstractmethod
    def _create_process(self, args: Args) -> ProcessOrResult:
        ## Use self._sanitize_arguments() before passing to Process
        ## Use self._print_content() as process write
        raise NotImplementedError(f"{type(self).__name__} requires to implement _create_process")

    def _handle_process_output(self, args: Args, process: Process, output: Union[bool, BaseException]) -> TaskResult:
        if isinstance(output, bool):
            return self._handle_process_finished(args, process, output)
        if isinstance(output, BaseException):
            return self._handle_process_exception(args, process, output)
        raise ValueError(f"Expected `bool` or `BaseException`, but process returned `{type(output).__name__}`")

    def _handle_process_finished(
        self,
        args: Args,
        process: Process,
        output: bool,
        message: Optional[str] = None,
    ) -> TaskResult:
        # pylint: disable=too-many-boolean-expressions
        if (
            message is None
            and ((output and self._show_output_at_end) or (not output and not self._can_print_content))
            and not process.output is None
            and len(process.output) > 0
        ):
            message = process.output
        return TaskResult(args, message=message, success=self._ignore_failure or output)

    def _handle_process_exception(
        self,
        args: Args,
        process: Process,  # pylint:disable=unused-argument
        output: BaseException,
        message: Optional[str] = None,
    ) -> TaskResult:
        return TaskResult(args, error=output, message=message, success=self._ignore_failure)
