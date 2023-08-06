from ...model.task.identity import *  # pylint: disable=wildcard-import
from ...model.task.task import Task


class UserTaskIdentity(TaskIdentity):
    def __init__(
        self,
        task_id: TaskId,
        name: str,
        options: List[Option],
        creator: Callable[[], Task],
        allow_more: bool = False,
    ) -> None:
        super().__init__("user", task_id, name, options, creator, allow_more)
