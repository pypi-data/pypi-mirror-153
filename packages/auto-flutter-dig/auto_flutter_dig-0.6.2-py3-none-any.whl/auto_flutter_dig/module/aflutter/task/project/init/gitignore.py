from ......model.error import Err, SilentWarning
from ......model.task.task import *  # pylint: disable=wildcard-import
from ......model.task.init.project_identity import InitProjectTaskIdentity
from ......module.aflutter.identity import AflutterTaskIdentity

__all__ = ["ProjectInitGitIgnoreTask"]


class _ProjectInitGistIgnoreTaskIdentity(AflutterTaskIdentity, InitProjectTaskIdentity):
    ...


class ProjectInitGitIgnoreTask(Task):
    identity = _ProjectInitGistIgnoreTaskIdentity(
        "-project-init-git-ignore",
        "",
        [],
        lambda: ProjectInitGitIgnoreTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Configure .gitignore"

    def execute(self, args: Args) -> TaskResult:
        try:
            with open(".gitignore", "r+", encoding="utf-8") as file:
                found = False
                for line in file:
                    if not isinstance(line, str):
                        continue
                    line = line.strip("\n")
                    if line == "*.log" or line.startswith(("*.log ", "*.log#")):
                        found = True
                        break
                    if line == "aflutter.log" or line.startswith(("aflutter.log ", "aflutter.log#")):
                        found = True
                        break

                if found:
                    return TaskResult(args)

                file.writelines(("aflutter.log"))

        except BaseException as error:
            return TaskResult(
                args,
                error=Err(SilentWarning(".gitignore can not be open"), error),
                success=True,
            )

        return TaskResult(args)
