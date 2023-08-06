from .....core.config import Config
from .....model.argument.options import LongOption
from .....model.error import Err
from .....model.task.result import TaskResultHelp
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.config.const import AFLUTTER_CONFIG_ENABLE_STACK_STRACE
from .....module.aflutter.identity import AflutterTaskIdentity
from .....module.aflutter.task.setup.save import AflutterSetupSaveTask


class AflutterSetupStackTraceTask(Task):
    __opt_on = LongOption("on", "Show stack trace when showing errors")
    __opt_off = LongOption("off", "Show only the deescription of errors")
    __opt_default = LongOption("default", "Use default value")

    identity = AflutterTaskIdentity(
        "stack-trace",
        "Configure if errors are displayed with stack trace",
        [__opt_on, __opt_off, __opt_default],
        lambda: AflutterSetupStackTraceTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Configure error details"

    def execute(self, args: Args) -> TaskResult:
        if args.contains(self.__opt_on):
            if args.contains(self.__opt_off):
                return TaskResult(
                    args,
                    error=Err(ValueError("Can not enable and disable stack trace simultaneously")),
                )
            Config.put_bool(AFLUTTER_CONFIG_ENABLE_STACK_STRACE, True)
        elif args.contains(self.__opt_off):
            Config.put_bool(AFLUTTER_CONFIG_ENABLE_STACK_STRACE, False)
        elif args.contains(self.__opt_default):
            Config.remove(AFLUTTER_CONFIG_ENABLE_STACK_STRACE)
        else:
            return TaskResultHelp(args, error=Err(ValueError("This task require one option")))
        self._append_task(AflutterSetupSaveTask.identity)
        return TaskResult(args)
