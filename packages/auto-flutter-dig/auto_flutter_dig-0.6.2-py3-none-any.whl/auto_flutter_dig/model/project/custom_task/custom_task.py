from __future__ import annotations

from typing import List, Optional

from ....core.json.codec import JsonDecode, JsonEncode
from ....core.json.serializable import Json, Serializable
from ....core.utils import _Ensure
from ....model.project.custom_task.content import CustomTaskContent
from ....model.project.custom_task.type import CustomTaskType
from ....model.task.id import TaskId


class CustomTask(Serializable["CustomTask"]):
    def __init__(
        self,
        task_id: TaskId,
        name: str,
        custom_type: CustomTaskType,
        require: Optional[List[str]] = None,
        content: Optional[CustomTaskContent] = None,
    ) -> None:
        super().__init__()
        self.task_id: TaskId = _Ensure.instance(task_id, TaskId, "id")
        self.name: str = _Ensure.instance(name, str, "name")
        self.custom_type: CustomTaskType = _Ensure.instance(custom_type, CustomTaskType, "type")
        self.require: Optional[List[str]] = require
        self.content: Optional[CustomTaskContent] = content

    def to_json(self) -> Json:
        return {
            "id": self.task_id,
            "name": self.name,
            "type": JsonEncode.encode(self.custom_type),
            "require": JsonEncode.encode_optional(self.require),
            "content": JsonEncode.encode_optional(self.content),
        }

    @staticmethod
    def from_json(json: Json) -> Optional[CustomTask]:
        if not isinstance(json, dict):
            return None

        task_id: Optional[TaskId] = None
        name: Optional[str] = None
        custom_type: Optional[CustomTaskType] = None
        require: Optional[List[str]] = None
        content: Optional[CustomTaskContent] = None

        for key, value in json.items():
            if not isinstance(key, str):
                continue
            if key == "id" and isinstance(value, str):
                task_id = value
            elif key == "name" and isinstance(value, str):
                name = value
            elif key == "type":
                custom_type = JsonDecode.decode(value, CustomTaskType)
            elif key == "require":
                require = JsonDecode.decode_list(value, str)
            elif key == "content":
                content = JsonDecode.decode(value, CustomTaskContent)
        return CustomTask(task_id, name, custom_type, require, content)  # type: ignore[arg-type]
