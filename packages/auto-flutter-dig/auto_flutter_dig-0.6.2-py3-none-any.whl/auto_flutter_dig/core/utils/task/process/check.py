from .....core.process.process import Process
from .....core.string import SB
from .....core.utils.task.process.timeout import BaseProcessTimeoutTask, ProcessOrResult

__all__ = ["BaseProcessCheckTask", "ProcessOrResult", "Process"]


class BaseProcessCheckTask(BaseProcessTimeoutTask):
    def _on_interval(self, process: Process, elapsed: float, count: int) -> None:
        if count == 1:
            self._print("  Skill wating...")
        elif count == 3:
            self._print(SB().append("  It is taking some time...", SB.Color.YELLOW).str())
        return super()._on_interval(process, elapsed, count)

    def _on_process_stop(self, process: Process, elapsed: float, count: int) -> None:
        self._print(SB().append("  Stop process...", SB.Color.RED).str())
        return super()._on_process_stop(process, elapsed, count)

    def _on_process_kill(self, process: Process, elapsed: float, count: int) -> None:
        self._print(SB().append("  Kill process...", SB.Color.RED, True).str())
        return super()._on_process_kill(process, elapsed, count)
