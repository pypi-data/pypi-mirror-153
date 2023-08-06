from ...model.task.base_task import BaseTask
from ...model.task.identity import TaskIdentity

__all__ = ["_TaskUniqueIdentity"]


class _TaskUniqueIdentity(TaskIdentity):
    def __init__(self, task: BaseTask) -> None:
        super().__init__("-#-#-", "-#-#-", "", [], lambda: task, True)
        self.__task = task

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(id={self.task_id}, group={self.group}, "
            + f"name={self.name}, options={self.options}, creator={self.__task}, "
            + f"parent={self.parent}, allow_more={self.allow_more})"
        )
