from __future__ import annotations

from typing import Dict, List, Optional

from ...core.json.codec import JsonDecode, JsonEncode
from ...core.json.serializable import Json, Serializable
from ...core.utils import _Ensure
from ...model.build.type import BuildType
from ...model.platform.run_type import RunType
from ...model.task.id import TaskId

__all__ = ["PlatformConfig", "RunType", "BuildType", "TaskIdList", "TaskId"]


class TaskIdList(List[TaskId], Serializable["TaskIdList"]):
    def to_json(self) -> Json:
        output: List[str] = []
        output.extend(self)
        return output

    @staticmethod
    def from_json(json: Json) -> Optional[TaskIdList]:
        if json is None:
            return None
        if not isinstance(json, List):
            return None
        output = TaskIdList()
        output.extend(json)
        return output


class PlatformConfig(Serializable["PlatformConfig"]):
    def __init__(
        self,
        build_param: Optional[List[str]] = None,
        run_before: Optional[Dict[RunType, TaskIdList]] = None,
        output: Optional[str] = None,
        outputs: Optional[Dict[BuildType, str]] = None,
        extras: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__()
        self._build_param: Optional[List[str]] = build_param
        self._run_before: Optional[Dict[RunType, TaskIdList]] = run_before
        self._output: Optional[str] = output
        self._outputs: Optional[Dict[BuildType, str]] = outputs
        self._extras: Optional[Dict[str, str]] = extras

    def get_build_param(self) -> List[str]:
        if self._build_param is None:
            return []
        return self._build_param

    def append_build_param(self, param: str):
        if self._build_param is None:
            self._build_param = []
        self._build_param.append(_Ensure.instance(param, str, "build-param"))

    def remove_build_param(self, param: str) -> bool:
        if self._build_param is None:
            return False
        if param not in self._build_param:
            return False
        self._build_param.remove(param)
        return True

    def get_output(self, build_type: Optional[BuildType]) -> Optional[str]:
        if build_type is None:
            return self._output
        if not self._outputs is None:
            if build_type in self._outputs:
                return self._outputs[build_type]
        return self._output

    def put_output(self, build_type: Optional[BuildType], value: str):
        if build_type is None:
            self._output = value
        else:
            if self._outputs is None:
                self._outputs = {}
            self._outputs[build_type] = value

    def remove_output(self, build_type: Optional[BuildType]):
        if build_type is None:
            self._output = None
        else:
            if not self._outputs is None and build_type in self._outputs:
                self._outputs.pop(build_type)
                if len(self._outputs) <= 0:
                    self._outputs = None

    def get_extra(self, key: str) -> Optional[str]:
        if self._extras is None:
            return None
        if key in self._extras:
            return self._extras[key]
        return None

    def add_extra(self, key: str, value: str):
        if self._extras is None:
            self._extras = {}
        self._extras[key] = value

    def remove_extra(self, key: str) -> bool:
        if self._extras is None:
            return False
        if not key in self._extras:
            return False
        self._extras.pop(key)
        if len(self._extras) <= 0:
            self._extras = None
        return True

    def get_run_before(self, run_type: RunType) -> Optional[List[TaskId]]:
        _Ensure.type(run_type, RunType, "type")
        if self._run_before is None or run_type not in self._run_before:
            return None
        return self._run_before[run_type]

    def to_json(self) -> Json:
        extras = self._extras
        output = {
            "build-param": JsonEncode.encode_optional(self._build_param),
            "run-before": JsonEncode.encode_optional(self._run_before),
            "output": JsonEncode.encode_optional(self._output),
            "outputs": None
            if self._outputs is None
            else JsonEncode.encode_dict(self._outputs, lambda x: x.output, lambda x: x),
        }
        if extras is None:
            return output
        return {**output, **extras}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(build_param={self._build_param}, run_before:{self._run_before}, "
            + f"output:{self._output}, outputs:{self._outputs}, extras:{self._extras})"
        )

    # pylint: disable=protected-access
    def _merge(self, other: PlatformConfig):
        # Platform build_param = merge
        if not other._build_param is None:
            if self._build_param is None:
                self._build_param = other._build_param
            else:
                self._build_param.extend(other._build_param)

        # Platform run_before = merge
        if not other._run_before is None:
            if self._run_before is None:
                self._run_before = {}
            for run_type, values in other._run_before.items():
                if run_type not in self._run_before:
                    self._run_before[run_type] = values
                else:
                    self._run_before[run_type].extend(values)

        # Platform output = override
        if not other._output is None and len(other._output) > 0:
            self._output = other._output

        # Platform outputs = merge-override
        if not other._outputs is None:
            if self._outputs is None:
                self._outputs = {}
            for build_type, output in other._outputs.items():
                self._outputs[build_type] = output

        # Platform extra = merge-override
        if not other._extras is None:
            if self._extras is None:
                self._extras = {}
            for key, extra in other._extras.items():
                self._extras[key] = extra

    @staticmethod
    def from_json(json: Json) -> Optional[PlatformConfig]:
        if not isinstance(json, Dict):
            return None
        build_param: Optional[List[str]] = None
        run_before: Optional[Dict[RunType, TaskIdList]] = None
        output: Optional[str] = None
        outputs: Optional[Dict[BuildType, str]] = None
        extras: Dict[str, str] = {}
        for key, value in json.items():
            if not isinstance(key, str):
                continue
            if key == "build-param" and isinstance(value, List):
                build_param = JsonDecode.decode_list(value, str)
            elif key == "run-before" and isinstance(value, Dict):
                run_before = JsonDecode.decode_optional_dict(value, RunType, TaskIdList)
            elif key == "output" and isinstance(value, str):
                output = value
            elif key == "outputs" and isinstance(value, Dict):
                outputs = JsonDecode.decode_optional_dict(value, BuildType, str, BuildType.from_output)
            elif isinstance(value, str):
                extras[key] = value
        return PlatformConfig(build_param, run_before, output, outputs, extras if len(extras) > 0 else None)
