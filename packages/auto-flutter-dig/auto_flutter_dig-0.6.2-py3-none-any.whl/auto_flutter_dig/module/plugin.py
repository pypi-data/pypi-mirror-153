from abc import ABC, abstractmethod
from typing import Callable

from ..model.task.identity import TaskIdentity
from ..model.task.group import TaskGroup

__all__ = ["AflutterModulePlugin", "TaskIdentity", "TaskGroup", "Callable"]


class AflutterModulePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    ### Called when environment config is empty before any setup
    def initialize_config(self):
        pass

    def initialize(self):
        pass

    def register_setup(
        self,
        setup: TaskGroup,
        check: Callable[[str, TaskIdentity], None],
    ):
        pass

    def register_config(self, config: TaskGroup):
        pass

    def register_tasks(self, root: TaskGroup):
        pass
