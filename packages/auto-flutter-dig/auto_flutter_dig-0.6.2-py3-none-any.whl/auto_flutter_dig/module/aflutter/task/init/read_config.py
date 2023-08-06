from .....core.config import Config
from .....core.string import SB
from .....model.error import Err
from .....model.task.task import *  # pylint: disable=wildcard-import


class ReadConfigTask(Task):
    def describe(self, args: Args) -> str:
        return "Reading config"

    def execute(self, args: Args) -> TaskResult:
        loaded = False
        base_error = Warning("Failed to read config. Using default values.")
        try:
            loaded = Config.load()
        except BaseException as error:
            base_error = Err(base_error, error)
        if loaded:
            return TaskResult(args)
        return TaskResult(
            args,
            error=base_error,
            message=SB()
            .append("Use task ", end="")
            .append("setup", SB.Color.CYAN, True)
            .append(" to configure your environment")
            .str(),
            success=True,
        )
