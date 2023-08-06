from pathlib import Path, PurePosixPath
from re import compile as re_compile

from ........core.os.path_converter import PathConverter
from ........model.error import Err, SilentWarning
from ........model.platform.platform import Platform
from ........model.project.project import Project
from ........model.result import Result
from ........model.task.task import *  # pylint: disable=wildcard-import
from ........module.aflutter.task.project.init.find.flavor.base import (
    BaseProjectInitFindFlavorIdentity,
    BaseProjectInitFindFlavorTask,
)


class ProjectInitFindFlavorAndroidGradleTask(BaseProjectInitFindFlavorTask):
    identity = BaseProjectInitFindFlavorIdentity(
        "-project-init-find-flavor-1-android-gradle",
        "",
        [],
        lambda: ProjectInitFindFlavorAndroidGradleTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Detect flavor config via Android gradle"

    def execute(self, args: Args) -> TaskResult:
        project = Project.current
        if not Platform.ANDROID in project.platforms:
            self._uptade_description("")
            return TaskResult(args, Err(SilentWarning("Project does not support android platform")), success=True)

        gradle = Path(PathConverter.from_posix(PurePosixPath("android/app/build.gradle")).to_machine())
        if not gradle.exists():
            self._uptade_description("", Result(Err(FileNotFoundError("Can not found android app gradle file"))))
            return TaskResult(args)
        found = False
        try:
            with open(gradle, "r", encoding="utf-8") as file:
                content = "".join(file.readlines())
            try:
                start = content.index("productFlavors")
                start = content.index("{", start)
            except BaseException as error:
                raise LookupError("Failed to find flavor section in build.gradle.") from error
            end = 0
            count = 0
            for i in range(start, len(content)):
                if content[i] == "{":
                    count += 1
                elif content[i] == "}":
                    count -= 1
                    if count <= 0:
                        end = i
                        break
            if end < start:
                raise LookupError("Failed to find flavor section in build.gradle.") from Err(
                    IndexError("End of string is before start")
                )
            flavors = content[start + 1 : end]
            count = 0
            buffer = ""
            space = re_compile(r"\s")
            for i, char in enumerate(flavors):
                if not space.match(char) is None:
                    continue
                if char == "{":
                    count += 1
                    if count == 1:
                        found = True
                        self._append_flavor(project, Platform.ANDROID, buffer, None)
                        buffer = ""
                    continue
                if char == "}":
                    count -= 1
                elif count == 0:
                    buffer += char
        except BaseException as error:
            self._uptade_description("", Result(Err(LookupError("Failed to find flavor"), error)))
            return TaskResult(args)

        if not found:
            return TaskResult(args, error=Err(LookupError("No flavor was found")), success=True)
        return TaskResult(args)
