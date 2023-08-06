from typing import Callable

from ........core.utils.task.subtask_run_all import BaseSubtaskRunAll
from ........model.task.group import TaskGroup
from ........model.task.identity import TaskIdentity
from ........model.task.init.project_identity import InitProjectTaskIdentity
from ........model.task.task import *  # pylint: disable=wildcard-import
from ........module.aflutter.identity import AflutterTaskIdentity
from ........module.aflutter.task.project.init.find.flavor.android_gradle import ProjectInitFindFlavorAndroidGradleTask
from ........module.aflutter.task.project.init.find.flavor.intellij import ProjectInitFindFlavorIntellijTask
from ........module.aflutter.task.project.init.find.flavor.ios import ProjectInitFindFlavorIosTask
from ........module.aflutter.task.project.init.find.flavor.web import ProjectInitFindFlavorWebTask
from ........module.aflutter.task.project.init.find.platform import ProjectInitFindPlatformTask


class _ProjectInitFindFlavorIdentity(AflutterTaskIdentity, InitProjectTaskIdentity, TaskGroup):
    def __init__(self, creator: Callable[[], Task]) -> None:
        InitProjectTaskIdentity.__init__(self, "", "", "", [], creator)
        AflutterTaskIdentity.__init__(self, "-project-init-find-flavor", "", [], creator)
        TaskGroup.__init__(
            self,
            [
                ProjectInitFindFlavorIntellijTask.identity,
                ProjectInitFindFlavorAndroidGradleTask.identity,
                ProjectInitFindFlavorIosTask.identity,
                ProjectInitFindFlavorWebTask.identity,
            ],
        )

    @property
    def require_before(self) -> List[TaskIdentity]:
        return [ProjectInitFindPlatformTask.identity]


ProjectInitFindFlavorIdentity: _ProjectInitFindFlavorIdentity = _ProjectInitFindFlavorIdentity(
    lambda: BaseSubtaskRunAll(ProjectInitFindFlavorIdentity)
)
