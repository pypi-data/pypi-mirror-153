from __future__ import annotations

from queue import Queue
from sys import stdout as sys_stdout
from threading import Lock, Thread
from time import sleep, time

from ....core.string import SB
from ....core.task.printer.operation import *  # pylint: disable=wildcard-import
from ....core.utils import _Ensure
from ....model.error import SilentWarning
from ....model.error.formater import format_exception
from ....model.task.result import TaskResult


class TaskPrinter:
    __COUNTER = "⡀⡄⡆⡇⡏⡟⡿⣿⢿⢻⢹⢸⢰⢠⢀"
    __COUNTER_LEN = len(__COUNTER)

    def __init__(self) -> None:
        self.__thread = Thread(target=TaskPrinter.__run, args=[self])
        self._operations: Queue[Operation] = Queue()
        self.__stop_mutex = Lock()
        self.__stop = False
        self._current_description: str = ""

    def start(self):
        self.__thread.start()

    def stop(self):
        with self.__stop_mutex:
            self.__stop = True
        self.__thread.join()

    def append(self, operation: Operation):
        self._operations.put(_Ensure.instance(operation, Operation, "operation"))

    def __run(self):
        while True:
            with self.__stop_mutex:
                if self.__stop:
                    if self._operations.empty():
                        break

            if not self._operations.empty():
                while not self._operations.empty():
                    self.__handle_operation(self._operations.get())

            else:
                TaskPrinter.__print_description(self._current_description)
                sleep(0.008)

    def __handle_operation(self, operation: Operation):
        if isinstance(operation, OpMessage):
            self.__handle_operation_message(operation)
        elif isinstance(operation, OpDescription):
            self.__handle_operation_description(operation)
        elif isinstance(operation, OpResult):
            self.__handle_operation_result(operation)
        else:
            print(format_exception(TypeError(f"Unknown Operation type: {type(operation).__name__}")))

    def __handle_operation_result(self, operation: OpResult):
        result = operation.result
        has_description = len(self._current_description) > 0
        if not result.success:
            if has_description:
                TaskPrinter.__print_description(self._current_description, failure=True)
            if not result.error is None:
                builder = SB()
                if has_description:
                    builder.append("\n")
                builder.append(
                    format_exception(result.error),
                    SB.Color.RED,
                )
                print(builder.str())
            elif has_description:
                print("")
        else:
            has_warning = not result.error is None
            print_warning = not result.error is None and not isinstance(result.error, SilentWarning)
            if has_description:
                TaskPrinter.__print_description(
                    self._current_description,
                    success=not has_warning,
                    warning=has_warning,
                )
                if not print_warning:
                    print("")
            if print_warning:
                assert not result.error is None
                print(
                    SB()
                    .append("\n")
                    .append(
                        format_exception(result.error),
                        SB.Color.YELLOW,
                    )
                    .str()
                )
        self._current_description = ""
        if isinstance(result, TaskResult):
            if not result.message is None:
                print(result.message)

    def __handle_operation_description(self, operation: OpDescription):
        self.__clear_line(self._current_description)
        self._current_description = operation.description
        TaskPrinter.__print_description(self._current_description)

    def __handle_operation_message(self, operation: OpMessage):
        TaskPrinter.__clear_line(self._current_description)
        print(operation.message)
        TaskPrinter.__print_description(self._current_description)

    @staticmethod
    def __clear_line(description: str):
        print("\r" + (" " * (len(description) + 8)), end="\r")

    @staticmethod
    def __print_description(
        description: str,
        success: bool = False,
        failure: bool = False,
        warning: bool = False,
    ):
        if description is None or len(description) == 0:
            return
        builder = SB()
        builder.append("\r")
        if success:
            builder.append("[√] ", SB.Color.GREEN, True)
        elif failure:
            builder.append("[X] ", SB.Color.RED, True)
        elif warning:
            builder.append("[!] ", SB.Color.YELLOW, True)
        else:
            icon = TaskPrinter.__COUNTER[int(time() * 10) % TaskPrinter.__COUNTER_LEN]
            builder.append("[" + icon + "] ", SB.Color.DEFAULT, True)

        print(builder.append(description).str(), end="")
        sys_stdout.flush()
