from typing import List

from ....model.task.identity import TaskId, TaskIdentity


class InitProjectTaskIdentity(TaskIdentity):
    @property
    def require_before(self) -> List[TaskIdentity]:
        return []

    @property
    def require_after(self) -> List[TaskIdentity]:
        return []

    @property
    def optional_before(self) -> List[TaskId]:
        return []

    @property
    def optional_after(self) -> List[TaskId]:
        return []
