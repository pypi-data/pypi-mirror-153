from ...model.task.identity import *  # pylint: disable=wildcard-import
from ...model.task.task import Task

GROUP_AFLUTTER = "aflutter"


class AflutterTaskIdentity(TaskIdentity):
    def __init__(
        self,
        task_id: TaskId,
        name: str,
        options: List[Option],
        creator: Callable[[], Task],
        allow_more: bool = False,
    ) -> None:
        super().__init__(GROUP_AFLUTTER, task_id, name, options, creator, allow_more)
