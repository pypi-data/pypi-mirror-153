from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.config.base import BaseConfigTask
from .....module.aflutter.task.config.project import ProjectConfigTaskIdentity


class AflutterConfigRefreshTask(BaseConfigTask):
    identity = ProjectConfigTaskIdentity(
        "refresh",
        "Update aflutter.json with aflutter style. Usefully after manually editing aflutter.json",
        [],
        lambda: AflutterConfigRefreshTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Refresh project file"

    def execute(self, args: Args) -> TaskResult:
        self._add_save_project()
        return TaskResult(args)
