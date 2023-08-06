from ........model.error import Err, SilentWarning
from ........model.platform.platform import Platform
from ........model.project.project import Project
from ........model.task.task import *  # pylint: disable=wildcard-import
from ........module.aflutter.task.project.init.find.flavor.base import (
    BaseProjectInitFindFlavorIdentity,
    BaseProjectInitFindFlavorTask,
)


class ProjectInitFindFlavorIosTask(BaseProjectInitFindFlavorTask):
    identity = BaseProjectInitFindFlavorIdentity(
        "-project-init-find-flavor-1-ios",
        "",
        [],
        lambda: ProjectInitFindFlavorIosTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Detect flavor config via iOS"

    def execute(self, args: Args) -> TaskResult:
        project = Project.current
        if not Platform.IOS in project.platforms:
            self._uptade_description("")
            return TaskResult(args, Err(SilentWarning("Project does not support ios platform")), success=True)

        return TaskResult(args, Err(NotImplementedError("Not implemented yet")), success=True)
