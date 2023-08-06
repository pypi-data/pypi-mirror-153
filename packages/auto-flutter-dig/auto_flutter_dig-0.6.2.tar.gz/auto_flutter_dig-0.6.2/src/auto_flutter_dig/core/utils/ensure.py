from abc import ABC
from types import FunctionType, MethodType
from typing import Any, Callable, NoReturn, Optional, Tuple, Type, TypeVar, Union


class _Ensure(ABC):
    T = TypeVar("T")

    @staticmethod
    def not_none(value: Optional[T], name: Optional[str] = None) -> T:
        if not value is None:
            return value
        if name is None:
            raise AssertionError("Field require valid value")
        raise AssertionError(f"Field `{name}` require valid value")

    @staticmethod
    def type(
        value: Optional[T],
        cls: Union[Type[T], Tuple[Type, ...]],
        name: Optional[str] = None,
    ) -> Optional[T]:
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        return _Ensure.raise_error_instance(name, cls, type(value))

    @staticmethod
    def type_returned(
        value: Optional[T],
        cls: Union[Type[T], Tuple[Type, ...]],
        name: Optional[str] = None,
    ) -> Optional[T]:
        if value is None:
            return None
        if isinstance(value, cls):
            return value
        return _Ensure.raise_error_value(name, cls, type(value))

    @staticmethod
    def instance(value: Any, cls: Type[T], name: Optional[str] = None) -> T:
        if not value is None and isinstance(value, cls):
            return value
        return _Ensure.raise_error_instance(name, cls, type(value))

    @staticmethod
    def raise_error_value(name: Optional[str], expected: Union[T, Type[T], Type], received: Type) -> NoReturn:
        if name is None:
            _Ensure._raise_error(
                "Value must be instance of `{cls}`, but `{input}` was returned",
                "",
                expected,
                received,
            )
        else:
            _Ensure._raise_error(
                "`{name}` must be instance of `{cls}`, but `{input}` was returned",
                name,
                expected,
                received,
            )

    @staticmethod
    def raise_error_instance(name: Optional[str], expected: Union[T, Type[T], Type], received: Type) -> NoReturn:
        if name is None:
            _Ensure._raise_error(
                "Field must be instance of `{cls}`, but `{input}` was used",
                "",
                expected,
                received,
            )
        else:
            _Ensure._raise_error(
                "Field `{name}` must be instance of `{cls}`, but `{input}` was used",
                name,
                expected,
                received,
            )

    @staticmethod
    def _raise_error(message: str, name: str, expected: Union[T, Type[T], Type], received: Type) -> NoReturn:
        raise TypeError(message.format(name=name, cls=_Ensure.name(expected), input=_Ensure.name(received)))

    @staticmethod
    def name(clazz: Union[T, Type[T], Type]) -> str:
        if hasattr(clazz, "__name__"):
            return clazz.__name__  # type: ignore
        return str(clazz)


class _EnsureCallable(ABC):
    T = TypeVar("T", bound=Callable)

    @staticmethod
    def type(
        value: Optional[T],
        name: Optional[str] = None,
    ) -> Optional[T]:
        if value is None:
            return None
        if isinstance(value, (FunctionType, MethodType)):
            return value  # type: ignore
        return _Ensure.raise_error_instance(name, Callable, type(value))

    @staticmethod
    def type_returned(
        value: Optional[T],
        name: Optional[str] = None,
    ) -> Optional[T]:
        if value is None:
            return None
        if isinstance(value, (FunctionType, MethodType)):
            return value  # type: ignore
        return _Ensure.raise_error_value(name, Callable, type(value))

    @staticmethod
    def instance(value: Optional[T], name: Optional[str] = None) -> T:
        if not value is None and isinstance(value, (FunctionType, MethodType)):
            return value  # type: ignore
        return _Ensure.raise_error_instance(name, Callable, type(value))
