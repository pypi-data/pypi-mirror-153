from typing import Optional

from .....core.config import Config
from .....core.string import SB
from .....core.utils.task.process.check import BaseProcessCheckTask, Process, ProcessOrResult
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.flutter.identity import FlutterTaskIdentity
from .....module.flutter.model._const import FLUTTER_CONFIG_KEY_PATH, FLUTTER_DISABLE_VERSION_CHECK


class FlutterSetupCheckTask(BaseProcessCheckTask):
    identity = FlutterTaskIdentity(
        "-flutter-check",
        "Checking flutter",
        [],
        lambda: FlutterSetupCheckTask(),  # pylint: disable=unnecessary-lambda
    )

    def __init__(self, skip_on_failure: bool = False) -> None:
        super().__init__(ignore_failure=skip_on_failure, interval=5, timeout=30)

    def _create_process(self, args: Args) -> ProcessOrResult:
        return Process.create(
            Config.get_path(FLUTTER_CONFIG_KEY_PATH),
            arguments=[FLUTTER_DISABLE_VERSION_CHECK, "--version"],
        )

    def _handle_process_exception(
        self,
        args: Args,
        process: Process,
        output: BaseException,
        message: Optional[str] = None,
    ) -> TaskResult:
        if isinstance(output, Process.ChildProcessStopped):
            builder = SB()
            if not message is None:
                builder.append(message, end="\n")
            builder.append("  Flutter take too much time to run. Re-configure with task ")
            builder.append("setup", SB.Color.CYAN, True)
            message = builder.str()
        return super()._handle_process_exception(args, process, output, message)
