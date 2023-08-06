from ........model.error import Err, SilentWarning
from ........model.platform.platform import Platform
from ........model.project.project import Project
from ........model.task.task import *  # pylint: disable=wildcard-import
from ........module.aflutter.task.project.init.find.flavor.base import (
    BaseProjectInitFindFlavorIdentity,
    BaseProjectInitFindFlavorTask,
)


class ProjectInitFindFlavorWebTask(BaseProjectInitFindFlavorTask):
    identity = BaseProjectInitFindFlavorIdentity(
        "-project-init-find-flavor-1-web",
        "",
        [],
        lambda: ProjectInitFindFlavorWebTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Detect flavor config via web"

    def execute(self, args: Args) -> TaskResult:
        project = Project.current
        if not Platform.WEB in project.platforms:
            self._uptade_description("")
            return TaskResult(args, Err(SilentWarning("Project does not support web platform")), success=True)

        return TaskResult(args, Err(NotImplementedError("Not implemented yet")), success=True)
