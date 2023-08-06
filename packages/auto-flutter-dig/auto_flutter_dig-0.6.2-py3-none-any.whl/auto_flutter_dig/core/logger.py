from logging import DEBUG, INFO, FileHandler, Formatter, Logger, getLogger
from pathlib import Path

from appdirs import user_log_dir  # type: ignore[import]

__all__ = ["log", "log_task"]


def __log_path() -> Path:
    return Path(user_log_dir("auto-flutter", "DIG"))


def __log_creator() -> Logger:
    _log = getLogger(__name__)
    filepath = __log_path().joinpath("aflutter.log")
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
    handler = FileHandler(filepath, "wt", "utf-8")
    handler.setFormatter(Formatter("%(asctime)s %(filename)10s@%(lineno)03d %(levelname)8s: %(message)s"))
    _log.addHandler(handler)
    _log.setLevel(INFO)
    return _log


def __log_task_creator() -> Logger:
    _log = log.getChild("task")
    _log.propagate = False
    _log.handlers = []
    try:
        handler = FileHandler("aflutter.log", "wt", "utf-8")
    except BaseException as error:
        log.warning("Can not open aflutter.log for task", exc_info=error)
        filepath = __log_path().joinpath("aflutter-task.log")
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)
        handler = FileHandler(filepath, "wt", "utf-8")
    handler.setFormatter(Formatter("%(asctime)s %(levelname)8s %(tag)12s: %(message)s"))
    _log.addHandler(handler)
    _log.setLevel(DEBUG)
    return _log


log: Logger = __log_creator()
log_task: Logger = __log_task_creator()
