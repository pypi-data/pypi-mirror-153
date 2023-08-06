from __future__ import annotations

from ...model.task.group import TaskGroup
from ...model.task.id import TaskId


class TaskNotFound(LookupError):
    def __init__(self, task_id: TaskId, parent: TaskGroup, *args: object) -> None:
        super().__init__(*args)
        self.task_id: TaskId = task_id
        self.parent: TaskGroup = parent
