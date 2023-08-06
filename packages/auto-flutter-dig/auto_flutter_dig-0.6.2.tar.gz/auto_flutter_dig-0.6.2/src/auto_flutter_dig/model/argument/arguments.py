from __future__ import annotations

from typing import Dict, Iterable, Optional, Union

from ...model.argument.options import LongOption, Option, OptionAll, PositionalOption, ShortOption

Value = Optional[str]
Argument = str
Group = str
Key = Union[Argument, Option]


class Args:
    GLOBAL = "--"

    # pylint: disable=dangerous-default-value
    def __init__(
        self,
        initial: Dict[Group, Dict[Argument, Value]] = {},
        group: Optional[str] = None,
    ) -> None:
        self.__content: Dict[Group, Dict[Argument, Value]] = initial
        self.__selected_group: Optional[str] = group
        self.__selected_content: Dict[Argument, Value] = {}
        if not group is None:
            self.select_group(group)

    def __repr__(self) -> str:
        return f"Args(group={self.__selected_group}, content={self.__content.__repr__()})"

    def select_group(self, group: Group) -> Args:
        self.__selected_group = group
        if not group in self.__content:
            self.__content[group] = {}
        self.__selected_content = self.__content[group]
        return self

    def with_group(self, group: Group) -> Args:
        return Args(self.__content, group)

    ###############
    ## Methods for a selected group

    def contains(self, key: Key) -> bool:
        key = self.__get_key(key)
        return key in self.__selected_content

    def get(self, key: Key) -> Value:
        key = self.__get_key(key)
        if key in self.__selected_content:
            return self.__selected_content[key]
        return None

    def add(self, key: Key, value: Value = None):
        key = self.__get_key(key)
        self.__selected_content[key] = value

    def remove(self, key: Key):
        key = self.__get_key(key)
        if key in self.__selected_content:
            self.__selected_content.pop(key)

    def get_all(self, key: OptionAll) -> Iterable[Argument]:
        if self.__selected_group is None:
            return []
        return self.group_get_all(self.__selected_group, key)

    ###############
    ## Methods for a specified group

    def group_contains(self, group: Group, key: Key) -> bool:
        if not group in self.__content:
            return False
        return self.__get_key(key) in self.__content[group]

    def group_get(self, group: Group, key: Key) -> Value:
        if not group in self.__content:
            return None
        key = self.__get_key(key)
        if key in self.__content[group]:
            return self.__content[group][key]
        return None

    def group_add(self, group: Group, key: Key, value: Value):
        key = self.__get_key(key)
        if not group in self.__content:
            self.__content[group] = {}
        self.__content[group][key] = value

    def group_remove(self, group: Group, key: Key):
        if not group in self.__content:
            return
        key = self.__get_key(key)
        if key in self.__content[group]:
            self.__content[group].pop(key)

    # pylint: disable=unused-argument
    def group_get_all(self, group: Group, option: OptionAll) -> Iterable[Argument]:
        group += "#all"
        if not group in self.__content:
            return []
        return map(lambda x: x[0], self.__content[group].items())

    # pylint: disable=unused-argument
    def group_add_all(self, group: Group, option: OptionAll, argument: Argument):
        group += "#all"
        if not group in self.__content:
            self.__content[group] = {}
        self.__content[group][argument] = None

    ###############
    ## Methods for the special group GLOBAL

    def global_contains(self, key: Key) -> bool:
        return self.group_contains(Args.GLOBAL, key)

    def global_get(self, key: Key) -> Value:
        return self.group_get(Args.GLOBAL, key)

    def global_add(self, key: Key, value: Value):
        return self.group_add(Args.GLOBAL, key, value)

    def global_remove(self, key: Key):
        return self.group_remove(Args.GLOBAL, key)

    ###############
    ## Internal help method

    @staticmethod
    def __get_key(option: Key) -> Argument:
        key: Optional[Argument] = None
        if isinstance(option, Argument):
            key = option
        elif isinstance(option, Option):
            if isinstance(option, LongOption):
                key = option.long
            elif isinstance(option, ShortOption):
                key = option.short
            elif isinstance(option, PositionalOption):
                key = str(option.position)
            else:
                raise TypeError(f"Can not get correct type of Option: {type(option).__name__}")
        if key is None:
            raise KeyError(f"Can not extract key from `{type(option)}`")
        return key.lower()
