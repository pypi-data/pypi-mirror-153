from abc import ABC
from enum import Enum
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union

from ...core.json.serializable import Json, Serializable
from ...core.utils import _Ensure, _Enum, _Iterable


class JsonDecode(ABC):
    T = TypeVar("T", bound=Union[str, Serializable, Enum, bool])
    K = TypeVar("K", bound=Union[str, Enum])
    Decoder = Callable[[Json], Optional[T]]
    KDecoder = Callable[[str], Optional[K]]

    @staticmethod
    def decode(
        json: Json,
        cls: Type[T],
        decoder: Optional[Decoder] = None,
    ) -> Optional[T]:
        if not decoder is None:
            return decoder(json)
        if cls is str:
            if isinstance(json, cls):
                return json
            return None
        if issubclass(cls, Serializable):
            result = cls.from_json(json)
            if not result is None and not isinstance(result, cls):
                return _Ensure.raise_error_value(None, cls, type(result))
            return result  # type: ignore
        if issubclass(cls, Enum):
            return _Enum.parse_value(cls, json)  # type:ignore
        raise ValueError(f"Unknown type to handle `{type(json).__name__}`")

    @staticmethod
    def decode_optional(json: Optional[Json], cls: Type[T], decoder: Optional[Decoder] = None) -> Optional[T]:
        if json is None:
            return None
        return JsonDecode.decode(json, cls, decoder)

    @staticmethod
    def __decode_list(
        json: Union[Json, List[Json]], cls: Type[T], decoder: Optional[Decoder] = None
    ) -> Iterable[Optional[T]]:
        if not isinstance(json, List):
            return _Ensure.raise_error_instance("json", List, type(json))
        return map(lambda x: JsonDecode.decode(x, cls, decoder), json)

    @staticmethod
    def decode_list(json: Union[Json, List[Json]], cls: Type[T], decoder: Optional[Decoder] = None) -> List[T]:
        return list(_Iterable.FilterOptional(JsonDecode.__decode_list(json, cls, decoder)))

    @staticmethod
    def decode_list_optional(
        json: Union[Json, List[Json]], cls: Type[T], decoder: Optional[Decoder] = None
    ) -> List[Optional[T]]:
        return list(JsonDecode.__decode_list(json, cls, decoder))

    @staticmethod
    def decode_optional_list(
        json: Optional[Union[Json, List[Json]]],
        cls: Type[T],
        decoder: Optional[Decoder] = None,
    ) -> Optional[List[T]]:
        if json is None:
            return None
        return JsonDecode.decode_list(json, cls, decoder)

    @staticmethod
    def decode_optional_list_optional(
        json: Optional[Union[Json, List[Json]]],
        cls: Type[T],
        decoder: Optional[Decoder] = None,
    ) -> Optional[List[Optional[T]]]:
        if json is None:
            return None
        return JsonDecode.decode_list_optional(json, cls, decoder)

    @staticmethod
    def decode_dict(
        json: Union[Json, Dict[str, Json]],
        k_cls: Type[K],
        t_cls: Type[T],
        k_decoder: Optional[KDecoder] = None,
        t_decoder: Optional[Decoder] = None,
    ) -> Dict[K, T]:
        mapped = JsonDecode.__decode_dict_to_map(json, k_cls, t_cls, k_decoder, t_decoder)
        filtered = _Iterable.FilterTupleOptional(mapped)
        return dict(filtered)

    @staticmethod
    def decode_dict_optional(
        json: Union[Json, Dict[str, Json]],
        k_cls: Type[K],
        t_cls: Type[T],
        k_decoder: Optional[KDecoder] = None,
        t_decoder: Optional[Decoder] = None,
    ) -> Dict[K, Optional[T]]:
        return dict(JsonDecode.__decode_dict_to_map(json, k_cls, t_cls, k_decoder, t_decoder))

    @staticmethod
    def decode_optional_dict(
        json: Optional[Union[Json, Dict[str, Json]]],
        k_cls: Type[K],
        t_cls: Type[T],
        k_decoder: Optional[KDecoder] = None,
        t_decoder: Optional[Decoder] = None,
    ) -> Optional[Dict[K, T]]:
        if json is None:
            return None
        return JsonDecode.decode_dict(json, k_cls, t_cls, k_decoder, t_decoder)

    @staticmethod
    def decode_optional_dict_optional(
        json: Optional[Union[Json, Dict[str, Json]]],
        k_cls: Type[K],
        t_cls: Type[T],
        k_decoder: Optional[KDecoder] = None,
        t_decoder: Optional[Decoder] = None,
    ) -> Optional[Dict[K, Optional[T]]]:
        if json is None:
            return None
        return JsonDecode.decode_dict_optional(json, k_cls, t_cls, k_decoder, t_decoder)

    @staticmethod
    def __decode_dict_to_map(
        json: Union[Json, Dict[str, Json]],
        k_cls: Type[K],
        t_cls: Type[T],
        k_decoder: Optional[KDecoder] = None,
        t_decoder: Optional[Decoder] = None,
    ) -> Iterable[Tuple[K, Optional[T]]]:
        if not isinstance(json, Dict):
            return _Ensure.raise_error_instance("json", Dict, type(json))
        return map(
            lambda x: JsonDecode.__decode_dict_tuple(x, k_cls, t_cls, k_decoder, t_decoder),
            json.items(),
        )

    @staticmethod
    def __decode_dict_tuple(
        value: Tuple[str, Json],
        k_cls: Type[K],
        t_cls: Type[T],
        k_decoder: Optional[KDecoder] = None,
        t_decoder: Optional[Decoder] = None,
    ) -> Tuple[K, Optional[T]]:
        return (
            JsonDecode.__decode_dict_key(value[0], k_cls, k_decoder),
            JsonDecode.decode(value[1], t_cls, t_decoder),
        )

    @staticmethod
    def __decode_dict_key(key: str, k_cls: Type[K], k_decoder: Optional[KDecoder] = None) -> K:
        if k_decoder is None:
            decoded = JsonDecode.decode(key, k_cls, None)
        else:
            decoded = k_decoder(key)
        if decoded is None:
            raise ValueError(f'Unexpected dict key decode "{key}" to `{k_cls.__name__}`')
        if isinstance(decoded, k_cls):
            return decoded
        raise ValueError(f'Invalid decoded key "{key}" as `{type(key).__format__}`')
