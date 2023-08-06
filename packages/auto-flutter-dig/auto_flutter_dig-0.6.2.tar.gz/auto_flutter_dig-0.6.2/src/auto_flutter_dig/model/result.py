from typing import Optional

from ..core.utils import _Ensure


class Result:
    def __init__(self, error: Optional[BaseException] = None, success: Optional[bool] = None) -> None:
        self.error: Optional[BaseException] = _Ensure.type(error, BaseException, "error")
        _Ensure.type(success, bool, "success")
        self.success: bool = success if not success is None else error is None

    @property
    def is_error(self) -> bool:
        return not self.success

    @property
    def is_warning(self) -> bool:
        return not self.error is None and self.success

    @property
    def is_success(self) -> bool:
        return self.success and self.error is None

    def __repr__(self) -> str:
        return f"{type(self).__name__}(error={self.error}, success={self.success})"
