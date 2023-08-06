from __future__ import annotations

from abc import ABC
from typing import Dict, Iterable, List, Optional, Tuple, Union

from ...core.utils import _Ensure, _Iterable
from ...model.task.identity import TaskId, TaskIdentity

__all__ = ["TaskGroup", "TaskIdentity"]


class TaskGroup(ABC):
    def __init__(
        self,
        subtasks: Union[Dict[TaskId, TaskIdentity], List[TaskIdentity]],
        parent: Optional[TaskGroup] = None,
    ) -> None:
        super().__init__()
        self.subtasks: Dict[TaskId, TaskIdentity] = {}
        self.parent: Optional[TaskGroup] = parent
        if isinstance(subtasks, List):
            self.register_subtask(subtasks)
        elif isinstance(subtasks, Dict):
            self.register_subtask(map(lambda x: x[1], subtasks.items()))
        else:
            raise TypeError(
                "Field `subtask` must be instance of `List[TaskIdentity]` or `Dict[Any,TaskIdentity]`,"
                + f" but `{type(subtasks).__name__}` was used"
            )

    def register_subtask(self, task: Union[TaskIdentity, Iterable[TaskIdentity]]):
        if isinstance(task, TaskIdentity):
            self.__register_subtask_tuple([task.to_map()])
        elif isinstance(task, Iterable):
            self.__register_subtask_tuple(_Ensure.instance(x, TaskIdentity, "task").to_map() for x in task)
        else:
            raise TypeError(f"Unexpected type received `{type(task).__name__}`")

    def __register_subtask_tuple(self, tasks: Iterable[Tuple[TaskId, TaskIdentity]]):
        self.__insert_sorted(_Iterable.Merge(self.subtasks.items(), tasks))

    def __insert_sorted(self, tasks: Iterable[Tuple[TaskId, TaskIdentity]]):
        w_parent = _Iterable.Apply(tasks, _SetParent(self).apply)
        w_order = sorted(w_parent, key=lambda x: x[0])
        self.subtasks = dict(w_order)


class _SetParent:
    def __init__(self, parent: TaskGroup) -> None:
        self.parent = parent

    def apply(self, task: Tuple[TaskId, TaskIdentity]):
        task[1].parent = self.parent
