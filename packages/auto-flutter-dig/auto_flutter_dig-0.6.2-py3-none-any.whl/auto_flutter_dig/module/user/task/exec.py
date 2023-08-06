from typing import List

from ....module.flutter.task.exec import FlutterExecTask
from ....module.user.identity import TaskId, UserTaskIdentity


class UserExecTaskIdentity(UserTaskIdentity):
    def __init__(self, task_id: TaskId, name: str, arguments: List[str]) -> None:
        super().__init__(task_id, name, [], lambda: FlutterExecTask(arguments))
