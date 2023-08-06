from .....core.config import Config
from .....core.os.executable_resolver import ExecutableResolver
from .....core.os.path_converter import PathConverter
from .....core.string import SB
from .....model.argument.options import LongPositionalOption
from .....model.error import Err
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.setup.save import AflutterSetupSaveTask
from .....module.flutter.identity import FlutterTaskIdentity
from .....module.flutter.model._const import FLUTTER_CONFIG_KEY_PATH
from .....module.flutter.task.setup.check import FlutterSetupCheckTask


class FlutterSetupTask(Task):
    __opt_executable = LongPositionalOption("command", 0, "Set flutter command, will be absolute if not in PATH")
    identity = FlutterTaskIdentity(
        "flutter",
        "Configure flutter environment",
        [__opt_executable],
        lambda: FlutterSetupTask(),  # pylint: disable=unnecessary-lambda
    )

    def execute(self, args: Args) -> TaskResult:
        had_change = False
        if args.contains(self.__opt_executable):
            flutter_cmd = args.get(self.__opt_executable)
            if flutter_cmd is None or len(flutter_cmd) <= 0:
                return TaskResult(args, Err(ValueError("Invalid flutter command")))
            flutter_path = PathConverter.from_path(flutter_cmd)
            try:
                flutter_exec = ExecutableResolver.resolve_executable(flutter_path.to_machine())
                Config.put_path(FLUTTER_CONFIG_KEY_PATH, flutter_exec)
                had_change = True
            except BaseException as error:
                return TaskResult(
                    args,
                    error=Err(FileNotFoundError(f'Can not find flutter command as "{flutter_cmd}"'), error),
                    message=(
                        SB()
                        .append("Resolved as: ", SB.Color.YELLOW)
                        .append(str(flutter_path.to_posix()), SB.Color.YELLOW, True)
                        .str()
                    ),
                    success=False,
                )

        if not had_change:
            return TaskResult(args, Warning("Nothing was changed"), success=True)

        self._append_task([AflutterSetupSaveTask.identity, FlutterSetupCheckTask.identity])
        return TaskResult(args)
