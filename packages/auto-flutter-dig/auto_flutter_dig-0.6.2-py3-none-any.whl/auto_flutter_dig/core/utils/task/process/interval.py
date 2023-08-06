from abc import abstractmethod
from threading import Thread
from time import time
from typing import Union

from .....core.utils.task.process.process import BaseProcessTask, Process, ProcessOrResult
from .....model.task.task import *  # pylint: disable=wildcard-import

__all__ = [
    "Task",
    "List",
    "TaskIdentity",
    "TaskResult",
    "TaskId",
    "Args",
    "BaseProcessIntervalTask",
    "ProcessOrResult",
]


class BaseProcessIntervalTask(BaseProcessTask):
    def __init__(
        self,
        ignore_failure: bool = False,
        show_output_at_end: bool = False,
        interval: float = 5,
    ) -> None:
        super().__init__(ignore_failure, show_output_at_end)
        self._interval = interval
        self.__output: Union[bool, BaseException, None] = None

    def execute(self, args: Args) -> TaskResult:
        process = self._create_process(args)
        if isinstance(process, TaskResult):
            return process
        self._process = process
        thread = Thread(target=BaseProcessIntervalTask.__run, args=[self])
        time_start = time()
        count = 0
        thread.start()
        while thread.is_alive():
            thread.join(self._interval)
            if thread.is_alive():
                count += 1
                self._on_interval(self._process, time() - time_start, count)
        thread.join()
        output = self.__output
        if output is None:
            return self._handle_process_exception(
                args, self._process, ChildProcessError("No return from child process")
            )
        return self._handle_process_output(args, self._process, output)

    @abstractmethod
    def _on_interval(self, process: Process, elapsed: float, count: int) -> None:
        ## Be carefull, `process` content are in other thread, but it is safe to call `stop` or `kill`
        pass

    def __run(self):
        self.__output = self._process.try_run()
