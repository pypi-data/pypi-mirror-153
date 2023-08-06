from .....core.config import Config
from .....model.error import Err
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.identity import AflutterTaskIdentity

__all__ = ["AflutterSetupSaveTask"]


class AflutterSetupSaveTask(Task):
    identity = AflutterTaskIdentity(
        "-aflutter-setup-save",
        "Save current environment config",
        [],
        lambda: AflutterSetupSaveTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Saving environment config"

    def execute(self, args: Args) -> TaskResult:
        try:
            Config.save()
        except BaseException as error:
            return TaskResult(
                args,
                error=Err(RuntimeError("Failed to save environment config"), error),
            )
        return TaskResult(args)
