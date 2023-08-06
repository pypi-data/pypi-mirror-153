from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from ...core.utils import _Ensure, _EnsureCallable
from ...model.argument.options import Option
from ...model.task.id import TaskId

__all__ = ["TaskIdentity", "TaskId", "List", "Callable", "Option"]


class TaskIdentity:
    def __init__(
        self,
        group: str,
        task_id: TaskId,
        name: str,
        options: List[Option],
        creator: Callable[[], "BaseTask"],  # type: ignore[name-defined]
        allow_more: bool = False,  # Allow more tasks with same id
    ) -> None:
        from .base_task import BaseTask  # pylint: disable=import-outside-toplevel,cyclic-import
        from .group import TaskGroup  # pylint: disable=import-outside-toplevel,cyclic-import

        self.group: str = _Ensure.instance(group, str, "group")
        self.task_id: TaskId = _Ensure.instance(task_id, TaskId, "id")
        self.name: str = _Ensure.instance(name, str, "name")
        if not isinstance(options, List):
            _Ensure.raise_error_instance("options", List, type(options))
        self.options: List[Option] = _Ensure.not_none(options, "options")
        self.creator: Callable[[], BaseTask] = _EnsureCallable.instance(creator, "creator")
        self.allow_more: bool = _Ensure.instance(allow_more, bool, "allow_more")
        self.parent: Optional[TaskGroup] = None

    def to_map(self) -> Tuple[TaskId, TaskIdentity]:
        return (self.task_id, self)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(id={self.task_id}, group={self.group}, "
            + f"name={self.name}, options={self.options}, creator={self.creator}, "
            + f"parent={self.parent}, allow_more={self.allow_more})"
        )
