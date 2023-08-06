from .....core.utils.task.subtask_parent_task import BaseSubtaskParentTask
from .....model.task.group import TaskGroup
from .....module.aflutter.identity import AflutterTaskIdentity
from .....module.aflutter.task.setup.check import AflutterSetupCheckTask
from .....module.aflutter.task.setup.save import AflutterSetupSaveTask
from .....module.aflutter.task.setup.show import AflutterSetupShow
from .....module.aflutter.task.setup.stack_trace import AflutterSetupStackTraceTask

__all__ = ["AflutterSetupIdentity"]


class _AflutterSetupIdentity(AflutterTaskIdentity, TaskGroup):
    def __init__(self) -> None:
        AflutterTaskIdentity.__init__(
            self,
            "setup",
            "Configure environment",
            [],
            lambda: BaseSubtaskParentTask(self, self),
        )
        TaskGroup.__init__(
            self,
            [
                AflutterSetupShow.identity,
                AflutterSetupSaveTask.identity,
                AflutterSetupStackTraceTask.identity,
                AflutterSetupCheckTask.identity,
            ],
        )


AflutterSetupIdentity = _AflutterSetupIdentity()
