from __future__ import annotations

from typing import Dict, List, Optional

from ....core.json.codec import JsonDecode, JsonEncode
from ....core.json.serializable import Json, Serializable
from ....core.utils import _Ensure


class CustomTaskContent(Serializable["CustomTaskContent"]):
    def __init__(
        self,
        command: str,
        args: Optional[List[str]],
        output: Optional[bool] = None,  # Default is True
        skip_failure: Optional[bool] = None,  # Default is False
    ) -> None:
        self.command: str = _Ensure.instance(command, str, "command")
        self.args: Optional[List[str]] = args
        self.__output: Optional[bool] = _Ensure.type(output, bool, "output")
        self.__skip_failure: Optional[bool] = _Ensure.type(skip_failure, bool, "skip_failure")

    @property
    def output(self) -> bool:
        return True if self.__output is None else self.__output

    @output.setter
    def output(self, value: Optional[bool]):
        self.__output = _Ensure.type(value, bool, "value")

    @property
    def skip_failure(self) -> bool:
        return False if self.__skip_failure is None else self.__skip_failure

    @skip_failure.setter
    def skip_failure(self, value: Optional[bool]):
        self.__skip_failure = _Ensure.type(value, bool, "value")

    def to_json(self) -> Json:
        return {
            "command": self.command,
            "args": None if self.args is None else JsonEncode.encode_list(self.args, lambda x: x),
            "output": JsonEncode.encode_optional(self.__output),
            "skip_failure": JsonEncode.encode_optional(self.__skip_failure),
        }

    @staticmethod
    def from_json(json: Json) -> Optional[CustomTaskContent]:
        if not isinstance(json, Dict):
            return None
        command: Optional[str] = None
        args: Optional[List[str]] = None
        output: Optional[bool] = None
        skip_failure: Optional[bool] = None
        for key, value in json.items():
            if not isinstance(key, str):
                continue
            if key == "command":
                command = JsonDecode.decode(value, str)
            elif key == "args":
                args = JsonDecode.decode_list(value, str)
            elif key == "output":
                output = JsonDecode.decode(value, bool)
            elif key == "skip_failure":
                skip_failure = JsonDecode.decode(value, bool)
        return CustomTaskContent(command, args, output, skip_failure)  # type: ignore[arg-type]
