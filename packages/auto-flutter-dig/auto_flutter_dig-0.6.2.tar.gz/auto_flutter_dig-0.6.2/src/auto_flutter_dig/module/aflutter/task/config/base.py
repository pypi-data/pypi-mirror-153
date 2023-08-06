from .....model.project.project import Project
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.project.read import ProjectRead
from .....module.aflutter.task.project.save import ProjectSave

__all__ = ["Project", "BaseConfigTask"]


class BaseConfigTask(Task):
    def require(self) -> List[TaskId]:
        return [ProjectRead.identity.task_id]

    def _add_save_project(self):
        self._append_task(ProjectSave.identity)
