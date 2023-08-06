from typing import Callable

from .....model.argument.options import Option
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....model.task.identity import TaskIdentity


class ProjectConfigTaskIdentity(TaskIdentity):
    def __init__(
        self,
        task_id: TaskId,
        name: str,
        options: List[Option],
        creator: Callable[[], Task],
        allow_more: bool = False,
    ) -> None:
        super().__init__("project", task_id, name, options, creator, allow_more)
