from traceback import TracebackException

from ...core.config import Config
from ...module.aflutter.config.const import AFLUTTER_CONFIG_ENABLE_STACK_STRACE


def format_exception(error: BaseException) -> str:
    if Config.get_bool(AFLUTTER_CONFIG_ENABLE_STACK_STRACE):
        return "".join(TracebackException.from_exception(error).format()).rstrip("\n")
    return str(error)
