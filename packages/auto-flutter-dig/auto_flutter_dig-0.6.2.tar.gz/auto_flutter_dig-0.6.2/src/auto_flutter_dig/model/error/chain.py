from sys import _getframe as sys_getframe
from types import TracebackType
from typing import Optional, TypeVar

__all__ = ["Err"]

Error = TypeVar("Error", bound=BaseException)


# pylint: disable=invalid-name
def Err(error: Error, cause: Optional[BaseException] = None) -> Error:
    if not cause is None:
        error.__cause__ = cause
    if error.__traceback__ is None:
        frame = sys_getframe(1)
        error.__traceback__ = TracebackType(None, frame, frame.f_lasti, frame.f_lineno)
    return error
