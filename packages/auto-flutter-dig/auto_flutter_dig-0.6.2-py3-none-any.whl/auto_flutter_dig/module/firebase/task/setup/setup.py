from .....core.config import Config
from .....core.os.executable_resolver import ExecutableResolver
from .....core.os.path_converter import PathConverter
from .....core.string import SB
from .....model.argument.options import LongOption, LongPositionalOption
from .....model.error import Err
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.setup.save import AflutterSetupSaveTask
from .....module.firebase.identity import FirebaseTaskIdentity
from .....module.firebase.model._const import FIREBASE_CONFIG_KEY_PATH, FIREBASE_CONFIG_KEY_STANDALONE
from .....module.firebase.task.setup.check import FirebaseCheck


class FirebaseSetupTask(Task):
    __opt_executable = LongPositionalOption("command", 0, "Set firebase command, will be absolute if not in PATH")
    __opt_standalone_on = LongOption("standalone", "Set flag to handle firebase as standalone build")
    __opt_standalone_off = LongOption("no-standalone", "Remove flag of firebase standalone")
    identity = FirebaseTaskIdentity(
        "firebase",
        "Configure firebase environment",
        [__opt_executable, __opt_standalone_on, __opt_standalone_off],
        lambda: FirebaseSetupTask(),  # pylint: disable=unnecessary-lambda
    )

    def execute(self, args: Args) -> TaskResult:
        had_change = False
        if args.contains(self.__opt_executable):
            firebase_cmd = args.get(self.__opt_executable)
            if firebase_cmd is None or len(firebase_cmd) <= 0:
                return TaskResult(args, ValueError("Invalid firebase command"))
            firebase_path = PathConverter.from_path(firebase_cmd)
            try:
                firebase_exec = ExecutableResolver.resolve_executable(firebase_path.to_machine())
                Config.put_path(FIREBASE_CONFIG_KEY_PATH, firebase_exec)
                had_change = True
            except BaseException as error:
                return TaskResult(
                    args,
                    error=Err(FileNotFoundError(f'Can not find firebase command as "{firebase_cmd}"'), error),
                    message=(
                        SB()
                        .append("Resolved as: ", SB.Color.YELLOW)
                        .append(str(firebase_path.to_posix()), SB.Color.YELLOW, True)
                        .str()
                    ),
                    success=False,
                )

        if args.contains(self.__opt_standalone_on):
            if args.contains(self.__opt_standalone_off):
                self._print(
                    SB()
                    .append(
                        "Can not enable and disable standalone mode simultaneously",
                        SB.Color.YELLOW,
                    )
                    .str()
                )
            Config.put_bool(FIREBASE_CONFIG_KEY_STANDALONE, True)
            had_change = True
        elif args.contains(self.__opt_standalone_off):
            Config.remove(FIREBASE_CONFIG_KEY_STANDALONE)
            had_change = True

        if not had_change:
            return TaskResult(args, Warning("Nothing was changed"), success=True)

        self._append_task([AflutterSetupSaveTask.identity, FirebaseCheck.identity])
        return TaskResult(args)
