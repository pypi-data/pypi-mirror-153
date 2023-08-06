from __future__ import annotations

from typing import Deque, Iterable, List, Optional, Union

from ...core.task.printer.operation import *  # pylint: disable=wildcard-import
from ...core.task.printer.printer import TaskPrinter
from ...core.task.resolver import TaskResolver
from ...core.task.watcher import ProcessTerminateWatcher
from ...model.argument.arguments import Args
from ...model.error.chain import Err
from ...model.result import Result
from ...model.task.base_task import BaseTask
from ...model.task.group import TaskGroup
from ...model.task.id import TaskId
from ...model.task.identity import TaskIdentity
from ...model.task.result import TaskResult, TaskResultHelp

__all__ = ["TaskManager"]


class _TaskManager:
    def __init__(self) -> None:
        self._task_stack: Deque[TaskIdentity] = Deque()
        self._task_done: List[TaskIdentity] = []
        self._printer = TaskPrinter()
        self._terminate_watcher: Optional[ProcessTerminateWatcher] = None
        self._terminate = False
        self._kill = False

    def add(
        self,
        tasks: Union[BaseTask, Iterable[BaseTask], TaskIdentity, Iterable[TaskIdentity]],
    ):
        if not isinstance(tasks, BaseTask) and not isinstance(tasks, TaskIdentity) and not isinstance(tasks, Iterable):
            raise TypeError(
                "Field `tasks` must be instance of `BaseTask` or `TaskIdentity` or `Iterable` of both, "
                + f"but `{type(tasks).__name__}` was received"
            )
        self._task_stack.extend(TaskResolver.resolve(tasks, self._task_done))

    def add_id(
        self,
        ids: Union[TaskId, Iterable[TaskId]],
        origin: Optional[TaskGroup] = None,
    ):
        if isinstance(ids, TaskId):
            self.add(TaskResolver.find_task(ids, origin))
        elif isinstance(ids, Iterable):
            self.add(map(lambda task_id: TaskResolver.find_task(task_id, origin), ids))
        else:
            raise TypeError(
                "Field `ids` must be instance of `TaskId` or `Iterable[TaskId]`, "
                + f"but `{type(ids).__name__}` was received"
            )

    def start_printer(self):
        self._printer.start()

    def stop_printer(self):
        self._printer.stop()
        if not self._terminate_watcher is None:
            self._terminate_watcher.join()

    def print(self, message: str):
        self._printer.append(OpMessage(message))

    def update_description(
        self,
        description: Optional[str],
        result: Optional[Result] = None,
    ):
        if not result is None:
            self._printer.append(OpResult(result))
        self._printer.append(OpDescription(description))

    def execute(self) -> bool:
        args = Args()
        had_failure = False
        while len(self._task_stack) > 0:
            identity = self._task_stack.pop()
            task = identity.creator()
            args.select_group(identity.group)
            task.log.info("Starting task")

            self._printer.append(OpDescription(task.describe(args)))

            try:
                output = task.execute(args)
            except BaseException as error:
                output = TaskResult(args, error, success=False)
            if not isinstance(output, TaskResult):
                output = TaskResult(
                    args,
                    AssertionError(f"Task {type(task).__name__} returned without result"),
                    success=False,
                )

            self._task_done.append(identity)
            if self._terminate or self._kill:
                output.message = None
            self._printer.append(OpResult(output))

            if not output.message is None:
                task.log.debug(output.message)
            if output.is_success:
                task.log.info("Finished successfully")
            elif output.is_warning:
                task.log.warning("Finished with warning", exc_info=output.error)
            elif output.is_error:
                task.log.error("Failed", exc_info=output.error)

            if self._kill:
                self._printer.append(OpResult(Result(Err(InterruptedError("Process received SIGKILL")))))
                return False
            if self._terminate:
                self._printer.append(OpResult(Result(Err(InterruptedError("Process received SIGTERM")))))
                return False

            if not output.success:
                if isinstance(output, TaskResultHelp):
                    # pylint:disable=import-outside-toplevel,cyclic-import
                    from ...module.aflutter.task.help import HelpTask

                    self._task_stack.clear()
                    self.add(HelpTask.Stub(identity))
                    had_failure = True
                    continue
                return False
            args = output.args

        return not had_failure

    def terminate(self):
        self._terminate = True
        # pylint:disable=import-outside-toplevel,cyclic-import
        from ...core.process.process import Process

        for process in Process.active:
            process.stop()
        if len(Process.active) > 0:
            self._terminate_watcher = ProcessTerminateWatcher()

    def kill(self):
        self._kill = True
        # pylint:disable=import-outside-toplevel,cyclic-import
        from ...core.process.process import Process

        for process in Process.active:
            process.stop()

    def __repr__(self) -> str:
        return (
            f"TaskManager(stack_size={len(self._task_stack)}, done_size={len(self._task_done)}, "
            + f"stack={self._task_stack}, done={self._task_done})"
        )


TaskManager = _TaskManager()
