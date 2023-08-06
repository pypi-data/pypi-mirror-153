from __future__ import annotations

from typing import Dict, Generic, Iterable, Optional, Type, TypeVar, Union

from .....core.config import Config
from .....model.argument.option.error import OptionInvalidFormat, OptionNotFound, OptionRequireValue
from .....model.argument.options import *  # pylint: disable=wildcard-import
from .....model.task.identity import TaskIdentity
from .....model.task.task import *  # pylint: disable=wildcard-import
from .....module.aflutter.config.const import AFLUTTER_CONFIG_ENABLE_STACK_STRACE
from .....module.aflutter.task.help import HelpTask

Argument = str
Group = str
GroupedOptions = Dict[Group, Option]
OptionsByArgument = Dict[Argument, GroupedOptions]


T = TypeVar("T", bound=Option)  # pylint:disable=invalid-name


class _Helper(Generic[T]):
    def __init__(self, option: T, group: Union[Group, TaskIdentity], cls: Type[T]) -> None:
        self.option: T = option
        self.group: Group = ""
        if isinstance(group, Group):
            self.group = group
        elif isinstance(group, TaskIdentity):
            self.group = group.group

        self.has_value: bool = isinstance(option, OptionWithValue)
        self.argument: Argument = ""
        if cls is LongOption:
            assert isinstance(option, LongOption)
            self.argument = option.long
        elif cls is ShortOption:
            assert isinstance(option, ShortOption)
            self.argument = option.short
        elif cls is PositionalOption:
            assert isinstance(option, PositionalOption)
            self.argument = str(option.position)

    def into(self, target: Dict[Argument, Dict[Group, _Helper[T]]]):
        if not self.argument in target:
            target[self.argument] = {}
        target[self.argument][self.group] = self


class _ShortOptionMaybeWithValue(ShortOptionWithValue):
    ...


class _LongOptionMaybeWithValue(LongOptionWithValue):
    ...


OptionsLong = Dict[Argument, Dict[Group, _Helper[LongOption]]]
OptionsShort = Dict[Argument, Dict[Group, _Helper[ShortOption]]]
OptionsPositional = Dict[Argument, Dict[Group, _Helper[PositionalOption]]]
OptionsAll = List[_Helper[OptionAll]]


class _State:
    def __init__(
        self,
        has_param: List[_Helper],
        maybe_has_param: Optional[_Helper[Union[LongOption, ShortOption]]],
        position_count=0,
        has_option_all=False,
    ) -> None:
        self.has_param: List[_Helper] = has_param
        self.maybe_has_param: Optional[_Helper[Union[LongOption, ShortOption]]] = maybe_has_param
        self.position_count: int = position_count
        self.has_option_all: bool = has_option_all


class ParseOptionsTask(Task):
    __option_help = LongShortOption("h", "help", "Show help of task")
    __option_stack_trace = LongOption("stack-trace", "Enable stack trace of errors")

    def __init__(self, identity: TaskIdentity, arguments: List[str]) -> None:
        super().__init__()
        self._task_identity: TaskIdentity = identity
        self._input = arguments

    def describe(self, args: Args) -> str:
        return "Parsing arguments"

    def execute(self, args: Args) -> TaskResult:

        long_options: Dict[Argument, Dict[Group, _Helper[LongOption]]] = {}
        short_options: Dict[Argument, Dict[Group, _Helper[ShortOption]]] = {}
        positional_options: Dict[Argument, Dict[Group, _Helper[PositionalOption]]] = {}
        option_all: List[_Helper[OptionAll]] = []

        # Separate and identify options by type
        for identity in Task.manager()._task_stack.copy():  # pylint: disable=protected-access
            for option in identity.options:
                if isinstance(option, OptionAll):
                    option_all.append(_Helper(option, identity, OptionAll))
                    continue
                if isinstance(option, LongOption):
                    _Helper(option, identity, LongOption).into(long_options)
                if isinstance(option, ShortOption):
                    _Helper(option, identity, ShortOption).into(short_options)
                if isinstance(option, PositionalOption):
                    _Helper(option, identity, PositionalOption).into(positional_options)

        _Helper(ParseOptionsTask.__option_help, "aflutter", ShortOption).into(short_options)
        _Helper(ParseOptionsTask.__option_help, "aflutter", LongOption).into(long_options)
        _Helper(ParseOptionsTask.__option_stack_trace, "aflutter", LongOption).into(long_options)

        state = _State([], None, 0, len(option_all) > 0)
        for argument in self._input:  # pylint: disable=too-many-nested-blocks
            # Last iteration require param
            if len(state.has_param) > 0:
                self.__consume_param(args, argument, state, option_all)
                continue

            size = len(argument)
            # Last iteration maybe require param
            if not state.maybe_has_param is None:
                if size > 1 and argument[0] == "-":
                    if isinstance(state.maybe_has_param.option, ShortOption):
                        self.__append_argument(
                            args,
                            _Helper(
                                ShortOption(state.maybe_has_param.option.short, ""),
                                state.maybe_has_param.group,
                                ShortOption,
                            ),
                            None,
                        )
                    elif isinstance(state.maybe_has_param.option, LongOption):
                        self.__append_argument(
                            args,
                            _Helper(
                                LongOption(state.maybe_has_param.option.long, ""),
                                state.maybe_has_param.group,
                                LongOption,
                            ),
                            None,
                        )
                    state.maybe_has_param = None
                else:
                    self.__append_argument_all(args, option_all, argument)  # OptionAll
                    self.__append_argument(args, state.maybe_has_param, argument)
                    state.maybe_has_param = None
                    continue

            # Handle short option argument
            if size == 2 and argument[0] == "-":
                self.__parse_short(args, argument, state, short_options, option_all)
                continue

            # Handle long/grouped argument
            if size >= 4 and argument[0] == "-" and argument[1] == "-":
                self.__parse_long_or_grouped(args, argument, state, short_options, long_options, option_all)
                continue

            # Positional argument
            self.__parse_positional(args, argument, state, positional_options, option_all)

        ## For loop finished

        if args.group_contains("aflutter", ParseOptionsTask.__option_help):
            Task.manager()._task_stack.clear()  # pylint: disable=protected-access
            self._append_task(HelpTask.Stub(self._task_identity))

        if args.group_contains("aflutter", ParseOptionsTask.__option_stack_trace):
            Config.put_bool(
                AFLUTTER_CONFIG_ENABLE_STACK_STRACE,
                True,
            )

        return TaskResult(args)

    def __consume_param(self, args: Args, argument: str, state: _State, option_all: OptionsAll):
        self.__append_argument_all(args, option_all, argument)  # OptionAll
        for helper_has_param in state.has_param:
            self.__append_argument(args, helper_has_param, argument)
        state.has_param = []

    def __parse_short(
        self,
        args: Args,
        argument: str,
        state: _State,
        short_options: OptionsShort,
        option_all: OptionsAll,
    ):
        self.__append_argument_all(args, option_all, argument)  # OptionAll
        sub = argument[1:].lower()
        if sub in short_options:
            for _, helper_short in short_options[sub].items():
                if helper_short.has_value:
                    state.has_param.append(helper_short)
                else:
                    self.__append_argument(args, helper_short, None)
            return
        if state.has_option_all:
            return
        raise OptionNotFound("Unrecognized command line option {argument}")

    def __parse_long_or_grouped(
        self,
        args: Args,
        argument: str,
        state: _State,
        short_options: OptionsShort,
        long_options: OptionsLong,
        option_all: OptionsAll,
    ):
        split = argument[2:].lower().split(":")
        split_len = len(split)
        if split_len == 1:
            sub = split[0]
            group = None
        elif split_len == 2:
            sub = split[1]
            group = split[0]
        elif state.has_option_all:
            self.__append_argument_all(args, option_all, argument)  # OptionAll
            return
        else:
            raise OptionInvalidFormat("Invalid argument group structure for command line option {argument}")

        ###########
        # OptionAll
        if not group is None:
            self.__append_argument_all(
                args,
                # pylint: disable=cell-var-from-loop
                filter(lambda x: x.group == group, option_all),
                "-" + sub if len(sub) == 1 else "--" + sub,
            )
        else:
            self.__append_argument_all(
                args,
                option_all,
                "-" + sub if len(sub) == 1 else "--" + sub,
            )
        # OptionAll
        ###########

        # Short argument with group
        if len(sub) == 1:
            if sub in short_options:
                for group, helper_short in short_options[sub].items():
                    if helper_short.has_value:
                        state.has_param.append(helper_short)
                    else:
                        self.__append_argument(args, helper_short, None)
                return
            if not group is None:
                state.maybe_has_param = _Helper(_ShortOptionMaybeWithValue(sub, ""), group, ShortOption)
                return
            if state.has_option_all:
                return
            raise OptionNotFound("Unrecognized command line option {argument}")

        # Long argument
        if sub in long_options:
            if group is None:
                for _, helper_long in long_options[sub].items():
                    if helper_long.has_value:
                        state.has_param.append(helper_long)
                    else:
                        self.__append_argument(args, helper_long, None)
                return
            if group in long_options[sub]:
                helper_long = long_options[sub][group]
                if helper_long.has_value:
                    state.has_param.append(helper_long)
                else:
                    self.__append_argument(args, helper_long, None)
                return
            # unregistered group
            state.maybe_has_param = _Helper(_LongOptionMaybeWithValue(sub, ""), group, LongOption)
            return
        if not group is None:
            # unregistered option with group
            state.maybe_has_param = _Helper(_LongOptionMaybeWithValue(sub, ""), group, LongOption)
            return
        if state.has_option_all:
            return
        raise OptionNotFound("Unrecognized command line option {argument}")

    def __parse_positional(
        self,
        args: Args,
        argument: str,
        state: _State,
        positional_options: OptionsPositional,
        option_all: OptionsAll,
    ):
        self.__append_argument_all(args, option_all, argument)  # OptionAll
        pos = str(state.position_count)
        state.position_count += 1
        if pos not in positional_options:
            if state.has_option_all:
                return
            raise OptionNotFound('Unrecognized positional command line "{argument}"')
        for _, helper_positional in positional_options[pos].items():
            self.__append_argument(args, helper_positional, argument)

    @staticmethod
    def __append_argument(args: Args, helper: _Helper, value: Optional[str]):
        option: Option = helper.option
        group: Group = helper.group
        if helper.has_value and value is None:
            raise OptionRequireValue(f'Command line "{helper.argument}" requires value, but nothing found')
        if isinstance(option, OptionAll):
            assert not value is None
            args.group_add_all(group, option, value)
            return
        args.group_add(group, option, value)

    def __append_argument_all(self, args: Args, helper: Iterable[_Helper], argument: Argument):
        for helper_all in helper:
            self.__append_argument(args, helper_all, argument)
