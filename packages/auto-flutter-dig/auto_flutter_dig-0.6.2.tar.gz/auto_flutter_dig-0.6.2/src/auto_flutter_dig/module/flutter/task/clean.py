from os import path, remove

from ....model.task.task import *  # pylint: disable=wildcard-import
from ..identity import FlutterTaskIdentity
from .command import FlutterCommandTask


class FlutterClean(Task):
    identity = FlutterTaskIdentity(
        "clean", "Clean project files", [], lambda: FlutterClean()  # pylint: disable=unnecessary-lambda
    )

    def require(self) -> List[TaskId]:
        # pylint: disable=import-outside-toplevel,cyclic-import
        from ...aflutter.task.project.read import ProjectRead

        return [ProjectRead.identity.task_id]

    def execute(self, args: Args) -> TaskResult:
        filename = "pubspec.lock"
        if path.exists(filename):
            remove(filename)
        self._append_task(FlutterCommandTask(["clean"], "Clean flutter files"))
        return TaskResult(args)
