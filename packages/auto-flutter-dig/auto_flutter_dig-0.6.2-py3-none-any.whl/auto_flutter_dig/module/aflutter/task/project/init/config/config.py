from typing import Callable

from .......core.utils.task.subtask_run_all import BaseSubtaskRunAll
from .......model.task.group import TaskGroup, TaskIdentity
from .......model.task.init.project_identity import InitProjectTaskIdentity
from .......model.task.task import *  # pylint: disable=wildcard-import
from .......module.aflutter.identity import AflutterTaskIdentity
from .......module.aflutter.task.project.init.config.android import ProjectInitConfigAndroidTask
from .......module.aflutter.task.project.init.config.ios import ProjectInitConfigIosTask
from .......module.aflutter.task.project.init.config.web import ProjectInitConfigWebTask
from .......module.aflutter.task.project.init.find.flavor.flavor import ProjectInitFindFlavorIdentity


class _ProjectInitConfigIdentity(AflutterTaskIdentity, InitProjectTaskIdentity, TaskGroup):
    def __init__(self, creator: Callable[[], Task]) -> None:
        InitProjectTaskIdentity.__init__(self, "", "", "", [], creator)
        AflutterTaskIdentity.__init__(self, "-project-init-config", "", [], creator)
        TaskGroup.__init__(
            self,
            [
                ProjectInitConfigAndroidTask.identity,
                ProjectInitConfigIosTask.identity,
                ProjectInitConfigWebTask.identity,
            ],
        )

    @property
    def require_before(self) -> List[TaskIdentity]:
        return [ProjectInitFindFlavorIdentity]


ProjectInitConfigIdentity: _ProjectInitConfigIdentity = _ProjectInitConfigIdentity(
    lambda: BaseSubtaskRunAll(ProjectInitConfigIdentity)
)
