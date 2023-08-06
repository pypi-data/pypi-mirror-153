from .....core.config import Config
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.identity import AflutterTaskIdentity


class AflutterSetupShow(Task):
    identity = AflutterTaskIdentity(
        "show",
        "Show current environment config",
        [],
        lambda: AflutterSetupShow(),  # pylint: disable=unnecessary-lambda
    )

    def execute(self, args: Args) -> TaskResult:
        return TaskResult(args, message=str(Config), success=True)
