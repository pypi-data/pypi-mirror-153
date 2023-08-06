from pathlib import Path, PurePosixPath
from typing import Optional

from .....core.os.path_converter import PathConverter
from .....core.string import SB, SF
from .....model.build.mode import BuildMode
from .....model.build.type import BuildType
from .....model.error import Err, SilentWarning
from .....model.platform.flavored_config import PlatformConfigFlavored
from .....model.platform.platform import Platform
from .....model.platform.run_type import RunType
from .....model.project.flavor import Flavor
from .....model.project.project import Project
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.help import HelpTask
from .....module.flutter.identity import FlutterTaskIdentity
from .....module.flutter.task.command import FlutterCommandTask


class FlutterBuildTaskIdentity(FlutterTaskIdentity):
    def __init__(
        self,
        project: Project,
        build_type: BuildType,
        flavor: Optional[Flavor],
        config: PlatformConfigFlavored,
        build_mode: BuildMode = BuildMode.RELEASE,
        android_rebuild_fix_other: bool = False,
        android_rebuild_fix_desired: bool = False,
    ) -> None:
        super().__init__(
            "--flutter-build-task--",
            "",
            [],
            lambda: FlutterBuildTask(
                project=project,
                build_type=build_type,
                flavor=flavor,
                config=config,
                build_mode=build_mode,
                android_rebuild_fix_other=android_rebuild_fix_other,
                android_rebuild_fix_desired=android_rebuild_fix_desired,
            ),
        )


# pylint: disable=too-many-instance-attributes
class FlutterBuildTask(FlutterCommandTask):
    identity = FlutterTaskIdentity(
        "--flutter-build-task--",
        "",
        [],
        lambda: HelpTask(None, None),
        True,
    )

    def __init__(
        self,
        project: Project,
        build_type: BuildType,
        flavor: Optional[Flavor],
        config: PlatformConfigFlavored,
        build_mode: BuildMode = BuildMode.RELEASE,
        android_rebuild_fix_other: bool = False,
        android_rebuild_fix_desired: bool = False,
    ) -> None:
        super().__init__(
            command=[],
            ignore_failure=False,
            show_output_at_end=False,
            put_output_args=True,
        )
        self._project: Project = project
        self._build_type: BuildType = build_type
        self._flavor: Optional[Flavor] = flavor
        self._config: PlatformConfigFlavored = config
        self._build_mode: BuildMode = build_mode
        self._android_rebuild_fix_other: bool = android_rebuild_fix_other
        self._android_rebuild_fix_desired: bool = android_rebuild_fix_desired
        if (
            android_rebuild_fix_other or android_rebuild_fix_desired
        ) and android_rebuild_fix_other == android_rebuild_fix_desired:
            raise AssertionError("Trying rebuild android fix for other and desired at same time")

    def require(self) -> List[TaskId]:
        config = self._config.get_config_by_flavor(self._flavor)
        if config is None:
            return []
        run_before = config.get_run_before(RunType.BUILD)
        if run_before is None:
            return []
        return run_before

    def describe(self, args: Args) -> str:
        if self._android_rebuild_fix_desired:
            return f"Rebuild flutter {self._build_type.platform.value}, flavor {self._flavor}"
        if self._flavor is None:
            return f"Building flutter {self._build_type.platform.value}"
        return f"Building flutter {self._build_type.platform.value}, flavor {self._flavor}"

    def execute(self, args: Args) -> TaskResult:
        self._command = ["build", self._build_type.flutter]

        if not self._flavor is None:
            self._command.extend(("--flavor", self._flavor))

        self._command.append("--" + self._build_mode.value)

        self._command.extend(self._config.obtain_config_by_flavor(self._flavor).get_build_param())

        result = super().execute(args)

        if result.success:
            self._clear_output(args)
            return self._check_output_file(args)

        if self._build_type.platform == Platform.ANDROID:
            return self._handle_android_error(args, result)

        self._clear_output(args)
        return result

    def _check_output_file(self, args: Args) -> TaskResult:
        config = self._config.get_config_by_flavor(self._flavor)
        output_file: Optional[str] = None
        if not config is None:
            output_file = config.get_output(self._build_type)
        if output_file is None:
            return TaskResult(
                args,
                error=Err(Warning("Build success, but file output not defined")),
                success=True,
            )
        flavor = ""
        if not self._flavor is None:
            flavor = self._flavor
        output_file = SF.format(
            output_file,
            args,
            {
                "platform": self._build_type.platform.value,
                "flavor": flavor,
            },
        )

        if Path(PathConverter.from_posix(PurePosixPath(output_file)).to_machine()).exists():
            self._print_content(SB().append("Build output found successfully", SB.Color.GREEN).str())
        else:
            return TaskResult(
                args,
                Err(FileNotFoundError(f'Output "{output_file}" not found')),
                success=False,
            )

        args.global_add("output", output_file)
        return TaskResult(args, success=True)

    def _handle_android_error(self, args: Args, result: TaskResult) -> TaskResult:
        if self._android_rebuild_fix_other:
            # Skip, since it is a fix build
            self._clear_output(args)
            return TaskResult(
                args,
                error=Err(SilentWarning("Build failed. Maybe there is more flavors to build")),
                success=True,
            )

        if self._android_rebuild_fix_desired:
            # Failed our desired build
            self._clear_output(args)
            return result

        output = args.global_get("output")
        self._clear_output(args)
        if (
            output is None
            or output.find("This issue appears to be https://github.com/flutter/flutter/issues/58247") < 0
        ):
            # This error is not the issue we handle
            return result

        flavors = self._project.flavors
        if flavors is None or len(flavors) <= 1:
            # There is no other flavor to be the reason of this issue
            return result

        self._append_task(
            FlutterBuildTaskIdentity(
                self._project,
                self._build_type,
                self._flavor,
                self._config,
                self._build_mode,
                android_rebuild_fix_other=False,
                android_rebuild_fix_desired=True,
            )
        )
        for flavor in filter(lambda x: x != self._flavor, flavors):
            self._append_task(
                FlutterBuildTaskIdentity(
                    self._project,
                    self._build_type,
                    flavor,
                    self._config,
                    self._build_mode,
                    android_rebuild_fix_other=True,
                    android_rebuild_fix_desired=False,
                )
            )

        return TaskResult(
            args,
            error=Err(Warning("Flutter issue #58247 detected, building others flavors to fix...")),
            success=True,
        )

    @staticmethod
    def _clear_output(args: Args) -> None:
        args.global_remove("output")
