from json import load as json_load

from .....model.error import Err, SilentWarning
from .....model.project.project import Project
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.identity import AflutterTaskIdentity
from .....module.aflutter.task.project.inport import ProjectTaskImport


class ProjectRead(Task):
    identity = AflutterTaskIdentity("-project-read", "Reading project file", [], lambda: ProjectRead(False))

    identity_skip = AflutterTaskIdentity("-project-read-skip", "Reading project file", [], lambda: ProjectRead(True))

    def __init__(self, warn_if_fail: bool) -> None:
        super().__init__()
        self._warn_if_fail = warn_if_fail

    def describe(self, args: Args) -> str:
        if not Project.current is None:
            return ""
        return super().describe(args)

    def execute(self, args: Args) -> TaskResult:
        if not Project.current is None:
            return TaskResult(args)
        try:
            with open("aflutter.json", "r", encoding="utf-8") as file:
                try:
                    json = json_load(file)
                except BaseException as error:
                    return self.__return_error(
                        args,
                        Err(RuntimeError('Failed to read file "afutter.json"'), error),
                    )

                try:
                    Project.current = Project.from_json(json)
                except BaseException as error:
                    return self.__return_error(
                        args,
                        Err(ValueError('Failed to parse project from "aflutter.json"'), error),
                    )

        except BaseException as error:
            if self._warn_if_fail:
                return self.__return_error(
                    args,
                    Err(SilentWarning('Failed to open file "aflutter.json"'), error),
                )
            return self.__return_error(
                args,
                Err(FileNotFoundError('Failed to open file "aflutter.json"'), error),
            )

        if not Project.current.tasks is None:
            self._append_task(ProjectTaskImport())

        return TaskResult(args)

    def __return_error(self, args: Args, error: BaseException) -> TaskResult:
        return TaskResult(args, error, success=self._warn_if_fail)
