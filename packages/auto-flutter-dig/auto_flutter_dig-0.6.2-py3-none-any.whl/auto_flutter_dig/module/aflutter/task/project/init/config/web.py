from .......model.error import Err, SilentWarning
from .......model.platform.platform import Platform
from .......model.project.project import Project
from .......model.task.task import *  # pylint: disable=wildcard-import
from .......module.aflutter.identity import AflutterTaskIdentity


class ProjectInitConfigWebTask(Task):
    identity = AflutterTaskIdentity(
        "-project-init-config-web",
        "",
        [],
        lambda: ProjectInitConfigWebTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Apply web base config"

    def execute(self, args: Args) -> TaskResult:
        project = Project.current
        if not Platform.WEB in project.platforms:
            self._uptade_description("")
            return TaskResult(args, Err(SilentWarning("Project does not support web platform")), success=True)

        return TaskResult(args, Err(NotImplementedError("Sorry, not implemented yet")), success=True)
