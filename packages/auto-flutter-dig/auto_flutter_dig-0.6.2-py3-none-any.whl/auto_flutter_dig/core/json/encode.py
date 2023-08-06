from abc import ABC
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union

from ...core.json.serializable import Json, Serializable


class JsonEncode(ABC):
    Input = TypeVar("Input", bound=Union[Serializable, Enum, Json])
    kInput = TypeVar("kInput", bound=Union[Enum, str])
    Encoder = Callable[[Input], Json]
    kEncoder = Callable[[kInput], Json]

    @staticmethod
    def encode_optional(value: Optional[Input], encoder: Optional[Encoder] = None) -> Optional[Json]:
        if value is None:
            return None
        return JsonEncode.encode(value, encoder)

    @staticmethod
    def encode(value: Input, encoder: Optional[Encoder] = None) -> Json:
        if encoder is None:
            if isinstance(value, str):
                return value
            if isinstance(value, Serializable):
                return value.to_json()
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, List):
                return JsonEncode.encode_list(value, JsonEncode.encode)
            if isinstance(value, Dict):
                return JsonEncode.encode_dict(
                    value,
                    JsonEncode.encode,
                    JsonEncode.encode,
                )
            raise TypeError(f"Unknown encoder for {type(value).__name__}")
        if isinstance(value, List):
            return JsonEncode.encode_list(value, encoder)
        if isinstance(value, Dict):
            raise TypeError("Can not encode Dict with only one encoder. Use encode_dict")

        return encoder(value)

    @staticmethod
    def encode_list(value: List[Input], encoder: Optional[Encoder] = None) -> List[Json]:
        return list(map(lambda x: JsonEncode.encode(x, encoder), value))

    @staticmethod
    def encode_dict(
        value: Dict[kInput, Input],
        encoder_key: kEncoder,
        enoder_value: Encoder,
    ) -> Dict[str, Json]:
        return dict(
            map(
                lambda x: JsonEncode.__encode_dict_tuple(x, encoder_key, enoder_value),
                value.items(),
            )
        )

    @staticmethod
    def __encode_dict_tuple(
        value: Tuple[kInput, Input],
        encoder_key: kEncoder,
        enoder_value: Encoder,
    ) -> Tuple[str, Json]:
        return (
            JsonEncode.__encode_dict_key(value[0], encoder_key),
            JsonEncode.encode(value[1], enoder_value),
        )

    @staticmethod
    def __encode_dict_key(key: kInput, encoder: kEncoder) -> str:
        output = encoder(key)
        if isinstance(output, str):
            return output
        raise ValueError(f'Can not accept "{type(output).__name__}" as dictionary key')

    @staticmethod
    def clear_nones(json: Json) -> Json:
        if isinstance(json, List):
            return [JsonEncode.clear_nones(x) for x in json if x is not None]
        if isinstance(json, Dict):
            return {key: JsonEncode.clear_nones(val) for key, val in json.items() if val is not None}
        return json
