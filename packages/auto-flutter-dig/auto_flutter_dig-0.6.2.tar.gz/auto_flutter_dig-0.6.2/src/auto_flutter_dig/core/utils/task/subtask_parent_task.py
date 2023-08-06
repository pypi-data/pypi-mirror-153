from ....core.string import SB
from ....core.utils import _Ensure
from ....model.error import SilentWarning
from ....model.task.task import *  # pylint: disable=wildcard-import
from ....model.task.group import TaskGroup
from ....model.task.identity import TaskIdentity
from ....module.aflutter.task.help import HelpTask

__all__ = ["BaseSubtaskParentTask"]


class BaseSubtaskParentTask(Task):
    def __init__(self, identity: TaskIdentity, subtask: TaskGroup) -> None:
        super().__init__()
        self.identity = _Ensure.instance(identity, TaskIdentity, "identity")
        self._subtask: TaskGroup = _Ensure.instance(subtask, TaskGroup, "subtask")

    def describe(self, args: Args) -> str:
        # Basically will show help for subtasks
        return ""

    def execute(self, args: Args) -> TaskResult:
        self._append_task(
            HelpTask.Stub(
                self.identity,
                SB()
                .append("Task ", SB.Color.YELLOW)
                .append(self.identity.task_id, SB.Color.CYAN)
                .append(" require subtask!", SB.Color.YELLOW)
                .str(),
            )
        )
        return TaskResult(args, SilentWarning("Task require subtask"), success=True)
