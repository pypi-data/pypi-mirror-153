from .....core.utils.task.subtask_parent_task import BaseSubtaskParentTask
from .....model.task.group import TaskGroup
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.identity import AflutterTaskIdentity
from .....module.aflutter.task.config.flavor import AflutterFlavorConfigTask
from .....module.aflutter.task.config.platform import AflutterPlatformConfigTask
from .....module.aflutter.task.config.refresh import AflutterConfigRefreshTask

__all__ = ["AflutterConfigIdentity"]


class _AflutterConfigIdentity(AflutterTaskIdentity, TaskGroup):
    def __init__(self) -> None:
        AflutterTaskIdentity.__init__(
            self,
            "config",
            "Configure project",
            [],
            lambda: BaseSubtaskParentTask(self, self),
        )
        TaskGroup.__init__(
            self,
            [
                AflutterConfigRefreshTask.identity,
                AflutterPlatformConfigTask.identity,
                AflutterFlavorConfigTask.identity,
            ],
        )


AflutterConfigIdentity = _AflutterConfigIdentity()
