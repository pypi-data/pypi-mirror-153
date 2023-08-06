from typing import List

from ....model.error import Err
from ....model.platform.merge_config import MergePlatformConfigFlavored
from ....model.platform.platform import Platform
from ....model.project.project import Project
from ....model.task.task import *  # pylint: disable=wildcard-import
from ....module.aflutter.task.project.read import ProjectRead
from ....module.firebase.identity import FirebaseTaskIdentity
from ....module.firebase.model._const import FIREBASE_PROJECT_APP_ID_KEY
from ....module.flutter.task.build.stub import FlutterBuildStub


class FirebaseBuildValidate(Task):
    identity = FirebaseTaskIdentity(
        "-firebase-build-validate",
        "Checking if project is able to upload to firebase",
        [],
        lambda: FirebaseBuildValidate(),  # pylint: disable=unnecessary-lambda
    )

    ARG_FIREBASE_GOOGLE_ID = "FIREBASE_CONFIG_GOOGLE_ID"

    def require(self) -> List[TaskId]:
        return [ProjectRead.identity.task_id]

    def execute(self, args: Args) -> TaskResult:
        flutter_args = args.with_group(FlutterBuildStub.identity.group)
        flavor = FlutterBuildStub.opt_flavor.get_or_none(flutter_args)
        build_type = FlutterBuildStub.opt_build_type.get(flutter_args)
        project = Project.current
        config = MergePlatformConfigFlavored(
            project.get_platform_config(Platform.DEFAULT),
            project.get_platform_config(build_type.platform),
        )
        app_id = config.get_config_by_flavor(flavor).get_extra(FIREBASE_PROJECT_APP_ID_KEY.value)
        if app_id is None or len(app_id) <= 0:
            return TaskResult(
                args,
                error=Err(ValueError("App id not found in aflutter.json")),
                success=False,
            )

        args.add(FirebaseBuildValidate.ARG_FIREBASE_GOOGLE_ID, app_id)
        return TaskResult(args)
