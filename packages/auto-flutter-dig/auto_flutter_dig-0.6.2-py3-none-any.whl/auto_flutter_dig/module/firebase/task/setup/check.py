from typing import Optional

from .....core.config import Config
from .....core.string import SB
from .....core.utils.task.process.check import BaseProcessCheckTask, Process, ProcessOrResult
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.firebase.identity import FirebaseTaskIdentity
from .....module.firebase.model._const import *  # pylint: disable=wildcard-import


class FirebaseCheck(BaseProcessCheckTask):
    identity = FirebaseTaskIdentity(
        "-firebase-check",
        "Checking firebase-cli",
        [],
        lambda: FirebaseCheck(),  # pylint: disable=unnecessary-lambda
    )

    def __init__(self, skip_on_failure: bool = False) -> None:
        super().__init__(ignore_failure=skip_on_failure, interval=5, timeout=30)

    def _create_process(self, args: Args) -> ProcessOrResult:
        return Process.create(
            Config.get_path(FIREBASE_CONFIG_KEY_PATH),
            arguments=[FIREBASE_DISABLE_INTERACTIVE_MODE.value, "--version"],
            environment=FIREBASE_ENV.value,
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
            builder.append("  Check if firebase-cli is standalone and configure correctly with task ")
            builder.append("setup", SB.Color.CYAN, True)
            message = builder.str()
        return super()._handle_process_exception(args, process, output, message)
