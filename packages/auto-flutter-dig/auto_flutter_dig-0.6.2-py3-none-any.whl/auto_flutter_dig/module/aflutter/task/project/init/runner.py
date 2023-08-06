from typing import Iterable

from ......core.task.resolver import TaskNotFound, TaskResolver
from ......model.error import Err
from ......model.task.identity import TaskIdentity
from ......model.task.init.project_identity import InitProjectTaskIdentity
from ......model.task.task import *  # pylint: disable=wildcard-import
from ......module.aflutter.identity import AflutterTaskIdentity
from ......module.aflutter.task.project.init.config.config import ProjectInitConfigIdentity
from ......module.aflutter.task.project.init.create import ProjectInitCreateTask
from ......module.aflutter.task.project.init.find.flavor.flavor import ProjectInitFindFlavorIdentity
from ......module.aflutter.task.project.init.find.platform import ProjectInitFindPlatformTask
from ......module.aflutter.task.project.init.gitignore import ProjectInitGitIgnoreTask
from ......module.aflutter.task.project.save import ProjectSave


class _ExtendedInitProjectTaskIdentity:
    def __init__(
        self, identity: TaskIdentity, require_before: List[TaskIdentity], require_after: List[TaskIdentity]
    ) -> None:
        self.identity = identity
        self.require_before = require_before
        self.require_after = require_after

    def __repr__(self) -> str:
        return f"{len(self.require_before)} {len(self.require_after)} :: {self.identity}"


class ProjectInitRunnerTask(Task):
    identity = AflutterTaskIdentity(
        "init",
        "Initialize Auto-Flutter project",
        [ProjectInitCreateTask.opt_name, ProjectInitCreateTask.opt_force],
        lambda: ProjectInitRunnerTask(),  # pylint: disable=unnecessary-lambda
    )
    external_tasks: List[InitProjectTaskIdentity] = [
        ProjectInitFindPlatformTask.identity,
        ProjectInitFindFlavorIdentity,
        ProjectInitConfigIdentity,
        ProjectInitGitIgnoreTask.identity,
    ]

    def describe(self, args: Args) -> str:
        return "Prepare to init project"

    def execute(self, args: Args) -> TaskResult:
        tasks: List[TaskIdentity] = [ProjectInitCreateTask.identity]
        resolved = list(map(self._resolve_init_project, self.external_tasks))
        while len(resolved) > 0:
            possible = filter(lambda x: self._all_in(x.require_before, tasks), resolved)
            ordered = sorted(possible, key=lambda x: len(x.require_after), reverse=True)
            if len(ordered) <= 0:
                self.log.warning(" === DUMP START ===")
                self.log.info(str(tasks))
                self.log.warning(" --- RESOLVED ---")
                self.log.info(str(resolved))
                return TaskResult(
                    args, Err(LookupError("Has task to include, but all require_before are not available"))
                )
            found = False
            for item in ordered:
                if not self._any_in(item.require_after, tasks):
                    found = True
                    tasks.append(item.identity)
                    resolved.remove(item)
            if not found:
                self.log.warning(" === DUMP START ===")
                self.log.info(str(tasks))
                self.log.warning(" --- RESOLVED ---")
                self.log.info(str(resolved))
                self.log.warning(" --- FILTERED ---")
                self.log.info(str(ordered))
                return TaskResult(args, Err(LookupError("Has task to include, but all require_after does not apply")))

        tasks.append(ProjectSave.identity)
        tasks.reverse()
        self._append_task(tasks)
        return TaskResult(args)

    @staticmethod
    def _resolve_init_project(identity: InitProjectTaskIdentity) -> _ExtendedInitProjectTaskIdentity:
        output = _ExtendedInitProjectTaskIdentity(
            identity,
            identity.require_before.copy(),
            identity.require_after.copy(),
        )
        for task_id in identity.optional_before:
            try:
                output.require_before.append(TaskResolver.find_task(task_id, ProjectInitRunnerTask.identity.parent))
            except TaskNotFound:
                pass
        for task_id in identity.optional_after:
            try:
                output.require_after.append(TaskResolver.find_task(task_id, ProjectInitRunnerTask.identity.parent))
            except TaskNotFound:
                pass
        return output

    @staticmethod
    def _all_in(origin: Iterable[TaskIdentity], destiny: Iterable[TaskIdentity]) -> bool:
        for identity in origin:
            if not identity in destiny:
                return False
        return True

    @staticmethod
    def _any_in(origin: Iterable[TaskIdentity], destiny: Iterable[TaskIdentity]) -> bool:
        for identity in origin:
            if identity in destiny:
                return True
        return False
