from typing import Callable

from ...model.task.group import TaskGroup
from ...model.task.identity import TaskIdentity
from ...module.firebase.task.config import FirebaseConfigTask
from ...module.firebase.task.setup.check import FirebaseCheck
from ...module.firebase.task.setup.setup import FirebaseSetupTask
from ...module.firebase.task.upload import FirebaseBuildUpload
from ...module.firebase.task.validate import FirebaseBuildValidate
from ...module.plugin import AflutterModulePlugin


class FirebaseModulePlugin(AflutterModulePlugin):
    @property
    def name(self) -> str:
        return "Firebase"

    def register_setup(
        self,
        setup: TaskGroup,
        check: Callable[[str, TaskIdentity], None],
    ):
        setup.register_subtask(FirebaseSetupTask.identity)
        check("firebase", FirebaseCheck.identity)

    def register_config(self, config: TaskGroup):
        config.register_subtask(FirebaseConfigTask.identity)

    def register_tasks(self, root: TaskGroup):
        root.register_subtask(
            [
                FirebaseBuildUpload.identity,
                FirebaseBuildValidate.identity,
                FirebaseCheck.identity,
            ]
        )
