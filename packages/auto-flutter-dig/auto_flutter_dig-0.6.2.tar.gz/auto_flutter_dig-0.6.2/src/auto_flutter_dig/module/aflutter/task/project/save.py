from json import dump as json_dump

from .....core.json.codec import JsonEncode
from .....model.project.project import Project
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.identity import AflutterTaskIdentity


class ProjectSave(Task):
    identity = AflutterTaskIdentity(
        "-project-save",
        "Saving project file",
        [],
        lambda: ProjectSave(),  # pylint: disable=unnecessary-lambda
    )

    def execute(self, args: Args) -> TaskResult:
        project = Project.current
        if project is None:
            raise ValueError("There is no project to save")
        try:
            with open("aflutter.json", "wt", encoding="utf-8") as file:
                try:
                    json = JsonEncode.clear_nones(project.to_json())
                except BaseException as error:
                    raise RuntimeError("Failed to serialize project") from error
                json_dump(json, file, indent=2)
        except BaseException as error:
            return TaskResult(args, error=error)
        return TaskResult(args)
