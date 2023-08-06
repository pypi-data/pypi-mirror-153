from pathlib import Path
from typing import Optional

from ......core.string import SB
from ......model.argument.options import LongOptionWithValue, LongShortOption
from ......model.error import Err, SilentWarning
from ......model.project.project import Project
from ......model.task.task import *  # pylint: disable=wildcard-import
from ......module.aflutter.identity import AflutterTaskIdentity


class ProjectInitCreateTask(Task):
    opt_name = LongOptionWithValue("name", "Name of project")
    opt_force = LongShortOption("f", "force", "Ignore existing project file")
    identity = AflutterTaskIdentity(
        "-project-init-create",
        "Create aflutter.json",
        [
            opt_name,
            opt_force,
        ],
        lambda: ProjectInitCreateTask(),  # pylint: disable=unnecessary-lambda
    )

    def execute(self, args: Args) -> TaskResult:
        if Path("aflutter.json").exists():
            if not args.contains(self.opt_force):
                return TaskResult(
                    args,
                    Err(FileExistsError("Project already initialized")),
                    message=SB()
                    .append(" Use task ")
                    .append("config", SB.Color.CYAN, True)
                    .append(" to configure current project. Or use option ")
                    .append(self.opt_force.describe()[0], SB.Color.MAGENTA)
                    .append(" to overwrite existing project.")
                    .str(),
                )
            self._uptade_description("Overwriting aflutter.json")
            self._reset_description(args, TaskResult(args, error=SilentWarning(), success=True))
        pubspec = Path("pubspec.yaml")
        if not pubspec.exists():
            return TaskResult(args, Err(FileNotFoundError("Can not initialize project outside a flutter project")))

        name = self._project_name_from_pubspec(pubspec)
        if args.contains(self.opt_name):
            name = args.get(self.opt_name)
        if name is None:
            return TaskResult(
                args,
                Err(NameError("Can not find project name")),
                message=SB()
                .append(" Provide poject name with option ")
                .append(self.opt_name.describe()[0], SB.Color.MAGENTA)
                .str(),
            )
        Project.current = Project(name, [], None, {})

        return TaskResult(args)

    @staticmethod
    def _project_name_from_pubspec(pubspec: Path) -> Optional[str]:
        try:
            # pylint: disable=import-outside-toplevel,cyclic-import
            from yaml import safe_load as yaml_load  # type: ignore
        except ImportError:
            return None
        try:
            with open(pubspec, "r", encoding="utf-8") as file:
                content = yaml_load(file)
            name = content["name"]
            if isinstance(name, str):
                return name
        except BaseException:
            pass
        return None
