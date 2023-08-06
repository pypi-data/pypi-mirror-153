from threading import Thread
from time import sleep


class ProcessTerminateWatcher:
    def __init__(self) -> None:
        self.__thread = Thread(target=ProcessTerminateWatcher.__run)
        self.__thread.start()

    def join(self):
        self.__thread.join()

    @staticmethod
    def __run():
        # pylint:disable=import-outside-toplevel,cyclic-import
        from ...core.process.process import Process

        count = 0
        while len(Process.active) > 0 and count < 100:
            sleep(0.01)
        for process in Process.active:
            process.kill()
