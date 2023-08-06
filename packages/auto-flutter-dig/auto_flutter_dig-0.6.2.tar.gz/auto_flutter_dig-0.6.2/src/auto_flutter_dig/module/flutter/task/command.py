from typing import Optional

from ....core.config import Config
from ....core.utils.task.process.process import BaseProcessTask, Process, ProcessOrResult
from ....model.error import Err
from ....model.task.task import *  # pylint: disable=wildcard-import
from ....module.flutter.model._const import FLUTTER_CONFIG_KEY_PATH, FLUTTER_DISABLE_VERSION_CHECK


class FlutterCommandTask(BaseProcessTask):
    def __init__(
        self,
        command: List[str],
        describe: str = "",
        ignore_failure: bool = False,
        show_output_at_end: bool = False,
        put_output_args: bool = False,
        require_project: bool = True,
    ) -> None:
        super().__init__(ignore_failure, show_output_at_end)
        self._command: List[str] = command
        self._put_output_args: bool = put_output_args
        self._describe: str = describe
        self._require_project: bool = require_project

    def describe(self, args: Args) -> str:
        return self._describe

    def require(self) -> List[TaskId]:
        # pylint: disable=import-outside-toplevel,cyclic-import
        from ....module.aflutter.task.project.read import ProjectRead

        parent = super().require()
        if self._require_project:
            parent.append(ProjectRead.identity.task_id)
        return parent

    def _create_process(self, args: Args) -> ProcessOrResult:
        if len(self._command) <= 0:
            return TaskResult(
                args,
                error=Err(AssertionError("Flutter command require at least one command")),
            )
        flutter = Config.get_path(FLUTTER_CONFIG_KEY_PATH)
        self._command.insert(0, FLUTTER_DISABLE_VERSION_CHECK)

        return Process.create(
            executable=flutter,
            arguments=self._command,
            writer=self._print_content,
        )

    def _handle_process_finished(
        self, args: Args, process: Process, output: bool, message: Optional[str] = None
    ) -> TaskResult:
        if self._put_output_args:
            args.global_add("output", process.output)
        return super()._handle_process_finished(args, process, output, message)
