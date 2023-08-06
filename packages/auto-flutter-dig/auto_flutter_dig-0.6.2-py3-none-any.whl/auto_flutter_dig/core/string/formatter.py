from os import environ
from re import Match as re_Match
from re import compile as re_compile
from typing import Dict, Optional, Tuple

from ...core.utils import _Dict
from ...model.argument.arguments import Args


class StringFormatter:
    REGEX = re_compile(r"\$\{(\w+):([\w\_\-]+\.)?([\w\_\-]+)(\|\w+)?}")
    EXTRAS = Dict[str, str]

    def format(self, string: str, args: Args, args_extra: Optional[EXTRAS] = None) -> str:
        if args_extra is None:
            args_extra = {}
        replaces: Dict[str, str] = {}
        for match in StringFormatter.REGEX.finditer(string):
            try:
                processed = self.__sub(match, args, args_extra)
                replaces[processed[0]] = processed[1]
            except ValueError as error:
                raise ValueError(f'Error formatting "{match.group(0)}"') from error

        output: str = string
        for key, value in replaces.items():
            output = output.replace(key, value)
        return output

    @staticmethod
    def __sub(match: re_Match, args: Args, args_extras: EXTRAS) -> Tuple[str, str]:
        parsed: Optional[str] = None

        source: str = match.group(1)
        group: Optional[str] = match.group(2)
        argument: str = match.group(3)
        operation: Optional[str] = match.group(4)

        source = source.lower()
        argument = argument.lower()
        if not group is None:
            group = group.lower()[:1]
        if not operation is None:
            operation = operation.lower()[1:]

        if source == "arg":
            parsed = _Dict.get_or_none(args_extras, argument)
            if parsed is None:
                if group is None:
                    parsed = args.get(argument)
                else:
                    parsed = args.group_get(group, argument)
        elif source == "env":
            if not group is None:
                raise ValueError("Substitution from environment does not accept group")
            for key, value in environ.items():
                if key.lower() == argument:
                    parsed = value
                    break
        else:
            raise ValueError(f'Unknown source "{source}"')

        if parsed is None:
            raise ValueError(f'Value not found for "{argument}"')

        if operation is None or len(operation) <= 0:
            pass
        elif operation in ("capitalize"):
            parsed = parsed.capitalize()
        elif operation in ("upper", "uppercase"):
            parsed = parsed.upper()
        elif operation in ("lower", "lowercase"):
            parsed = parsed.lower()
        else:
            raise ValueError(f'Unknown operation "{operation}"')

        return (match.group(0), parsed)


SF = StringFormatter()
