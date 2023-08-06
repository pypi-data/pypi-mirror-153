from abc import ABC
from typing import Callable, Dict, List, Mapping, Optional, TypeVar


class _Dict(ABC):
    K = TypeVar("K")
    V = TypeVar("V")

    @staticmethod
    def get_or_none(mapping: Mapping[K, V], key: K) -> Optional[V]:
        return None if not key in mapping else mapping[key]

    @staticmethod
    def get_or_default(mapping: Mapping[K, V], key: K, fallback: Callable[[], V]) -> V:
        return fallback() if not key in mapping else mapping[key]

    @staticmethod
    def merge(left: Dict[K, V], right: Optional[Dict[K, V]]) -> Dict[K, V]:
        if right is None:
            return left
        merge = left.copy()
        for key, value in right.items():
            merge[key] = value
        return merge

    @staticmethod
    def merge_append(left: Dict[K, List[V]], right: Optional[Dict[K, List[V]]]) -> Dict[K, List[V]]:
        if right is None:
            return left
        merge = left.copy()
        for key, value in right.items():
            if key in merge:
                merge[key].extend(value)
            else:
                merge[key] = value
        return merge

    @staticmethod
    def flatten(mapping: Mapping[K, V]) -> List[V]:
        return list(map(lambda x: x[1], mapping.items()))
