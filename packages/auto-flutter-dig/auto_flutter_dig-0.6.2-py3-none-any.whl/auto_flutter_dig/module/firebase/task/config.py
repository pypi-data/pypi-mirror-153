from typing import Optional

from ....model.argument.option.common.flavor import FlavorOption
from ....model.argument.option.common.platform import PlatformOption
from ....model.argument.options import LongOption, LongOptionWithValue
from ....model.error import Err
from ....model.platform.platform import Platform
from ....model.task.task import *  # pylint: disable=wildcard-import
from ....module.aflutter.task.config.base import BaseConfigTask, Project
from ....module.firebase.identity import FirebaseTaskIdentity
from ....module.firebase.model._const import FIREBASE_PROJECT_APP_ID_KEY


class FirebaseConfigTask(BaseConfigTask):
    __opt_add = LongOptionWithValue("set-app-id", "Set app id for platform and/or flavor")
    __opt_rem = LongOption("remove-app-id", "Remove app id from platform and/or flavor")
    __opt_platform = PlatformOption("Select platform to apply change")
    __opt_flavor = FlavorOption("Select flavor to apply change")

    identity = FirebaseTaskIdentity(
        "firebase",
        "Update project firebase config",
        [__opt_add, __opt_rem, __opt_platform, __opt_flavor],
        lambda: FirebaseConfigTask(),  # pylint: disable=unnecessary-lambda
    )

    def execute(self, args: Args) -> TaskResult:
        project = Project.current

        platform: Platform = self.__opt_platform.get_or_default(args, lambda: Platform.DEFAULT)
        if platform != Platform.DEFAULT and platform not in project.platforms:
            raise ValueError(f"Project does not support platform {platform}")

        flavor = self.__opt_flavor.get_or_none(args)
        if not flavor is None:
            if project.flavors is None or not flavor in project.flavors:
                raise ValueError(f"Project does not contains flavor {flavor}")

        add_app_id = args.get(self.__opt_add)
        remove_app_id = args.contains(self.__opt_rem)
        if not add_app_id is None and remove_app_id:
            raise ValueError("Can not set and remove app id at same time")
        if add_app_id is None and not remove_app_id:
            raise ValueError("At least one operation is required")

        has_warning: Optional[BaseException] = None

        ## Remove app id section
        if remove_app_id:
            platform_config = project.get_platform_config(platform)
            if platform_config is None:
                raise KeyError(f"Project does not have config for platform {platform}")
            config = platform_config.get_config_by_flavor(flavor)
            if config is None:
                raise KeyError(f"Project does not have config for platform {platform} and flavor {flavor}")
            if not config.remove_extra(FIREBASE_PROJECT_APP_ID_KEY.value):
                has_warning = Err(Warning("Selected platform and flavor does not have app id"))

        ## Set app id section
        if not add_app_id is None:
            project.obtain_platform_cofig(platform).obtain_config_by_flavor(flavor).add_extra(
                FIREBASE_PROJECT_APP_ID_KEY.value, add_app_id
            )

        self._add_save_project()
        return TaskResult(args, error=has_warning, success=True)
