from typing import Optional

from ........model.platform.platform import Platform
from ........model.project.flavor import Flavor
from ........model.project.project import Project
from ........model.task.identity import TaskIdentity
from ........model.task.init.project_identity import InitProjectTaskIdentity
from ........model.task.task import *  # pylint: disable=wildcard-import
from ........module.aflutter.identity import AflutterTaskIdentity
from ........module.aflutter.task.project.init.find.platform import ProjectInitFindPlatformTask


class BaseProjectInitFindFlavorIdentity(AflutterTaskIdentity, InitProjectTaskIdentity):
    @property
    def require_before(self) -> List[TaskIdentity]:
        return [ProjectInitFindPlatformTask.identity]


class BaseProjectInitFindFlavorTask(Task):
    @staticmethod
    def _append_flavor(
        project: Project,
        platform: Platform,
        flavor: Flavor,
        build_param: Optional[List[str]],
    ):
        if project.flavors is None:
            project.flavors = []
        if not flavor in project.flavors:
            project.flavors.append(flavor)

        if not build_param is None and len(build_param) > 0:
            project.obtain_platform_cofig(platform).obtain_config_by_flavor(flavor).append_build_param(build_param)
