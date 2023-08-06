from sys import argv as sys_argv
from typing import Iterable, Optional, Tuple

from .....core.string import SB
from .....model.error import Err, SilentWarning, TaskNotFound
from .....model.task.group import TaskGroup
from .....model.task.identity import TaskIdentity
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.config.config import AflutterConfigIdentity
from .....module.aflutter.task.help import HelpTask
from .....module.aflutter.task.init.options import ParseOptionsTask
from .....module.aflutter.task.init.read_config import ReadConfigTask
from .....module.aflutter.task.project.read import ProjectRead
from .....module.aflutter.task.root import Root
from .....module.aflutter.task.setup.check import AflutterSetupCheckTask
from .....module.aflutter.task.setup.setup import AflutterSetupIdentity
from .....module.firebase.firebase import FirebaseModulePlugin
from .....module.flutter.flutter import FlutterModulePlugin
from .....module.plugin import AflutterModulePlugin


class AflutterInitTask(Task):
    def describe(self, args: Args) -> str:
        return "Initialize Aflutter"

    def execute(self, args: Args) -> TaskResult:
        read_config = ReadConfigTask()
        self._uptade_description(read_config.describe(args))
        read_config_result = read_config.execute(args)
        if read_config_result.is_error:
            return read_config_result

        read_project = ProjectRead(warn_if_fail=True)
        self._uptade_description(
            read_project.describe(args),
            read_config_result if read_config_result.is_warning else None,
        )
        read_project_result = read_project.execute(args)
        if read_project_result.is_error:
            return read_project_result

        self._uptade_description(
            "Loading modules",
            read_project_result if read_project_result.is_warning else None,
        )

        modules: Iterable[AflutterModulePlugin] = [
            FlutterModulePlugin(),
            FirebaseModulePlugin(),
        ]

        if read_config_result.is_warning:
            for module in modules:
                module.initialize_config()

        for module in modules:
            self._uptade_description(f"Initialize module {module.name}")
            try:
                module.initialize()
                module.register_setup(
                    AflutterSetupIdentity,
                    AflutterSetupCheckTask.identity.add,
                )
                module.register_config(AflutterConfigIdentity)
                module.register_tasks(Root)
            except BaseException as error:
                return TaskResult(
                    args,
                    Err(RuntimeError(f"Failed to initialize module {module.name}"), error),
                )

        self._uptade_description("Finding task")

        if len(sys_argv) <= 1:
            task: TaskIdentity = HelpTask.Stub(message=SB().append("Require one task to run", SB.Color.RED).str())
            offset = 1
        else:
            try:
                task, offset = self.__find_task(Root)
            except TaskNotFound as error:
                self._append_task(HelpTask.Stub(error.task_id))
                return TaskResult(args, Err(SilentWarning(), error), success=True)
            except BaseException as error:
                return TaskResult(
                    args,
                    error=Err(LookupError("Failed to find task"), error),
                )

        try:
            self._append_task(task)
        except BaseException as error:
            return TaskResult(
                args,
                error=Err(RuntimeError("Failed to create task tree"), error),
            )

        parse_options = ParseOptionsTask(task, sys_argv[offset:])
        self._uptade_description(parse_options.describe(args))
        parse_options_result = parse_options.execute(args)
        return parse_options_result

    @staticmethod
    def __find_task(root: TaskGroup) -> Tuple[TaskIdentity, int]:
        task: Optional[TaskIdentity] = None
        offset = 1
        limit = len(sys_argv)
        while offset < limit:
            task_id = sys_argv[offset]
            if task_id.startswith("-"):
                break
            if not task_id in root.subtasks:
                break
            task = root.subtasks[task_id]
            offset += 1
            if isinstance(task, TaskGroup):
                root = task
            else:
                break

        if not task is None:
            return (task, offset)
        raise TaskNotFound(task_id, root)
