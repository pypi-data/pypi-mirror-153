from __future__ import annotations

from abc import ABC
from collections import deque
from typing import Deque, Iterable, List, Optional, Union

from ...core.task._unique_identity import _TaskUniqueIdentity
from ...core.utils import _If
from ...model.error import TaskNotFound
from ...model.task.base_task import BaseTask
from ...model.task.group import TaskGroup
from ...model.task.id import TaskId
from ...model.task.identity import TaskIdentity


class TaskResolver(ABC):
    @staticmethod
    def resolve(
        task: Union[BaseTask, Iterable[BaseTask], TaskIdentity, Iterable[TaskIdentity]],
        previous: Optional[List[TaskIdentity]] = None,
        origin: Optional[TaskGroup] = None,
    ) -> Deque[TaskIdentity]:
        temp: List[TaskIdentity] = []
        if isinstance(task, BaseTask):
            t_identity = _TaskUniqueIdentity(task)
            if hasattr(task, "identity") and not task.identity is None:
                t_identity.parent = task.identity.parent
            temp = [t_identity]
        elif isinstance(task, TaskIdentity):
            temp = [task]
        elif isinstance(task, Iterable):
            for item in task:
                if isinstance(item, BaseTask):
                    it_identity = _TaskUniqueIdentity(item)
                    if hasattr(item, "identity") and not item.identity is None:
                        it_identity.parent = item.identity.parent
                    temp.append(it_identity)
                elif isinstance(item, TaskIdentity):
                    temp.append(item)
                else:
                    raise TypeError(f"Trying to resolve task, but received {type(task).__name__}")
        else:
            raise TypeError(f"Trying to resolve task, but received {type(task).__name__}")
        temp = TaskResolver.__resolve_dependencies(temp, origin)
        temp.reverse()
        temp = TaskResolver.__clear_repeatable(temp, previous)
        output: Deque[TaskIdentity] = deque()
        for identity in temp:
            output.appendleft(identity)
        return output

    @staticmethod
    def __resolve_dependencies(
        items: List[TaskIdentity],
        origin: Optional[TaskGroup] = None,
    ) -> List[TaskIdentity]:
        if len(items) <= 0:
            raise IndexError("Require at least one TaskIdentity")
        i = 0
        while i < len(items):
            current = items[i]
            _task = current.creator()
            for task_id in _task.require():
                identity = TaskResolver.find_task(
                    task_id,
                    _If.not_none(origin, lambda x: x, lambda: current.parent),
                )
                j = i + 1
                items[j:j] = [identity]
            i += 1
        return items

    @staticmethod
    def __clear_repeatable(
        new: List[TaskIdentity],
        previous: Optional[List[TaskIdentity]] = None,
    ) -> List[TaskIdentity]:
        if previous is None:
            previous = []
        items = previous.copy()
        items.extend(new)
        start = len(previous)
        i = start
        while i < len(items):
            n_item = items[i]
            if n_item.allow_more:
                pass
            else:
                j = i - 1
                while j >= 0:
                    p_item = items[j]
                    if p_item.task_id == n_item.task_id:
                        del items[i]
                        i -= 1
                        break
                    j -= 1
            i += 1
        return items[start:]

    @staticmethod
    def find_task(task_id: TaskId, origin: Optional[TaskGroup] = None) -> TaskIdentity:
        if origin is None:
            from ...module.aflutter.task.root import Root  # pylint: disable=import-outside-toplevel,cyclic-import

            origin = Root
        if task_id in origin.subtasks:
            return origin.subtasks[task_id]
        if not origin.parent is None:
            # Recursive, not good, but not expexct to have more than 3 level
            return TaskResolver.find_task(task_id, origin.parent)
        raise TaskNotFound(task_id, origin)
