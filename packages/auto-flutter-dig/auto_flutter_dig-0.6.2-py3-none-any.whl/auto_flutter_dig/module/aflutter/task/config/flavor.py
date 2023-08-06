from .....core.string import SB
from .....model.argument.options import LongOptionWithValue, LongShortOption
from .....model.error import Err
from .....model.result import Result
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.task.config.base import BaseConfigTask, Project
from .....module.aflutter.task.config.project import ProjectConfigTaskIdentity


class AflutterFlavorConfigTask(BaseConfigTask):
    option_add = LongOptionWithValue("add", "Add flavor to project")
    option_remove = LongOptionWithValue("remove", "Remove flavor from project")
    option_rename = LongOptionWithValue("rename", "Rename flavor from project. Use with --to-name")
    option_toname = LongOptionWithValue("to-name", "New flavor name from --rename")
    option_list = LongShortOption("l", "list", "List all flavors from project")
    identity = ProjectConfigTaskIdentity(
        "flavor",
        "Handle project flavors in general",
        [option_add, option_remove, option_rename, option_toname, option_list],
        lambda: AflutterFlavorConfigTask(),  # pylint: disable=unnecessary-lambda
    )

    def describe(self, args: Args) -> str:
        return "Updating project flavor"

    def execute(self, args: Args) -> TaskResult:
        project = Project.current
        if project.flavors is None:
            project.flavors = []

        has_change: bool = False

        has_change = self._add_flavor(args, project) or has_change
        has_change = self._remove_flavor(args, project) or has_change
        has_change = self._rename_flavor(args, project) or has_change

        if args.contains(self.option_list):
            self._uptade_description("Listing flavors")
            result: TaskResult
            if project.flavors is None or len(project.flavors) <= 0:
                result = TaskResult(args, message=SB().append("  Project has no flavors", SB.Color.YELLOW).str())
            else:
                builder = SB().append(" Project flavors:")
                for flavor in project.flavors:
                    builder.append("\n  ").append(flavor, SB.Color.GREEN)
                result = TaskResult(args, message=builder.str())
            if not has_change:
                return result
            self._uptade_description(self.describe(args), result)

        if not has_change:
            return TaskResult(args, error=Err(Warning("No change was made")), success=True)

        self._uptade_description("")  # To not write check for "Updating project flavor"
        if len(project.flavors) <= 0:
            project.flavors = None

        self._add_save_project()
        return TaskResult(args)

    def _add_flavor(self, args: Args, project: Project) -> bool:
        add_flavor = args.get(self.option_add)
        if add_flavor is None or len(add_flavor) <= 0:
            return False

        self._uptade_description(f"Adding flavor {add_flavor}")
        if not project.flavors is None and add_flavor in project.flavors:
            self._uptade_description(
                self.describe(args),
                Result(error=Err(AssertionError(f"Flavor `{add_flavor}` already exist in project"))),
            )
            return False

        if project.flavors is None:
            project.flavors = []

        project.flavors.append(add_flavor)
        self._uptade_description(self.describe(args), Result(success=True))
        return True

    def _remove_flavor(self, args: Args, project: Project) -> bool:
        rem_flavor = args.get(self.option_remove)
        if rem_flavor is None or len(rem_flavor) <= 0:
            return False

        self._uptade_description(f"Removing flavor {rem_flavor}")
        if project.flavors is None or not rem_flavor in project.flavors:
            self._uptade_description(
                self.describe(args),
                Result(Err(AssertionError(f"Flavor `{rem_flavor}` do not exist in project"))),
            )
            return False

        project.flavors.remove(rem_flavor)
        if not project.platform_config is None:
            for _, config in project.platform_config.items():
                if not config.flavored is None and rem_flavor in config.flavored:
                    config.flavored.pop(rem_flavor)
        self._uptade_description(self.describe(args), Result(success=True))
        return True

    def _rename_flavor(self, args: Args, project: Project) -> bool:
        ren_flavor = args.get(self.option_rename)
        to_flavor = args.get(self.option_toname)
        has_ren = not ren_flavor is None and len(ren_flavor) > 0
        has_to = not to_flavor is None and len(to_flavor) > 0
        if not has_ren and not has_to:
            return False

        self._uptade_description("Renaming flavor")

        if has_ren != has_to:
            if has_ren:
                self._uptade_description(
                    self.describe(args), Result(Err(ValueError("Trying to rename without destination name")))
                )
                return False
            self._uptade_description(
                self.describe(args), Result(Err(ValueError("Trying to rename without origin name")))
            )
            return False

        assert not ren_flavor is None
        assert not to_flavor is None
        self._uptade_description(f"Renaming flavor {ren_flavor} to {to_flavor}")
        if ren_flavor == to_flavor:
            self._uptade_description(
                self.describe(args), Result(Err(ValueError("Trying to rename flavor to same name")))
            )
            return False
        if project.flavors is None or to_flavor in project.flavors:
            self._uptade_description(
                self.describe(args), Result(Err(AssertionError("Destination flavor name already exist")))
            )
            return False
        if not ren_flavor in project.flavors:
            self._uptade_description(
                self.describe(args), Result(Err(AssertionError("Origin flavor name does not exist")))
            )
            return False
        project.flavors.remove(ren_flavor)
        project.flavors.append(to_flavor)
        if not project.platform_config is None:
            for _, config in project.platform_config.items():
                if (not config.flavored is None) and ren_flavor in config.flavored:
                    config.flavored[to_flavor] = config.flavored.pop(ren_flavor)
        self._uptade_description(self.describe(args), Result(success=True))
        return True
