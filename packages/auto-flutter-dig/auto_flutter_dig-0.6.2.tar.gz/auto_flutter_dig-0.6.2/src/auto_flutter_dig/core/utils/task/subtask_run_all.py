from ....core.utils import _Dict
from ....model.task.group import TaskGroup
from ....model.task.task import *  # pylint: disable=wildcard-import


class BaseSubtaskRunAll(Task):
    def __init__(self, subtask: TaskGroup) -> None:
        super().__init__()
        self._subtask = subtask

    def describe(self, args: Args) -> str:
        return ""

    def execute(self, args: Args) -> TaskResult:
        tasks = _Dict.flatten(self._subtask.subtasks)
        tasks.reverse()
        self._append_task(tasks)
        return TaskResult(args)
