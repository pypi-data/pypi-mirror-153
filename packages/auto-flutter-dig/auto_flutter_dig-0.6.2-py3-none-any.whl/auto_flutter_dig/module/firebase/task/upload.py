from pathlib import Path, PurePosixPath

from ....core.config import Config
from ....core.os.path_converter import PathConverter
from ....core.utils import _Dict, _If
from ....core.utils.task.process.process import BaseProcessTask, Process, ProcessOrResult
from ....model.argument.options import LongOptionWithValue
from ....model.error import Err
from ....model.task.task import *  # pylint: disable=wildcard-import
from ....module.firebase.identity import FirebaseTaskIdentity
from ....module.firebase.model._const import FIREBASE_CONFIG_KEY_PATH, FIREBASE_DISABLE_INTERACTIVE_MODE, FIREBASE_ENV
from ....module.firebase.task.setup.check import FirebaseCheck
from ....module.firebase.task.validate import FirebaseBuildValidate
from ....module.flutter.task.build.stub import FlutterBuildStub


class FirebaseBuildUpload(BaseProcessTask):
    __options = {
        "notes": LongOptionWithValue("notes", "Release notes to include"),
        "testers": LongOptionWithValue("testers", "A comma separated list of tester emails to distribute to"),
        "groups": LongOptionWithValue("groups", "A comma separated list of group aliases to distribute to"),
    }
    identity = FirebaseTaskIdentity(
        "firebase",
        "Upload build to firebase",
        _Dict.flatten(__options),
        lambda: FirebaseBuildUpload(),  # pylint: disable=unnecessary-lambda
    )

    def require(self) -> List[TaskId]:
        return [
            FirebaseBuildValidate.identity.task_id,
            FirebaseCheck.identity.task_id,
            FlutterBuildStub.identity.task_id,
        ]

    def _create_process(self, args: Args) -> ProcessOrResult:
        filename = args.global_get("output")
        if filename is None or len(filename) <= 0:
            return TaskResult(args, Err(AssertionError("Previous task does not have output")))

        file: Path = Path(PathConverter.from_posix(PurePosixPath(filename)).to_machine())
        if not file.exists():
            return TaskResult(
                args,
                Err(FileNotFoundError(f"Output not found: {file}")),
            )

        file = file.absolute()
        google_id = args.get(FirebaseBuildValidate.ARG_FIREBASE_GOOGLE_ID)
        if google_id is None or len(google_id) <= 0:
            return TaskResult(args, Err(AssertionError("Google app id not found")))

        arguments: List[str] = [
            FIREBASE_DISABLE_INTERACTIVE_MODE.value,
            "appdistribution:distribute",
            str(file),
            "--app",
            google_id,
        ]

        _If.not_none(
            args.get(self.__options["notes"]),
            lambda notes: arguments.extend(("--release-notes", notes)),
            lambda: None,
        )

        _If.not_none(
            args.get(self.__options["testers"]),
            lambda testers: arguments.extend(("--testers", testers)),
            lambda: None,
        )

        _If.not_none(
            args.get(self.__options["groups"]),
            lambda groups: arguments.extend(("--groups", groups)),
            lambda: None,
        )

        return Process.create(
            Config.get_path(FIREBASE_CONFIG_KEY_PATH),
            arguments=arguments,
            environment=FIREBASE_ENV.value,
            writer=self._print_content,
        )
