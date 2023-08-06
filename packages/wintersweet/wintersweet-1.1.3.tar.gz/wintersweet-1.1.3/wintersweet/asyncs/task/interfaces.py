

class TaskInterface:

    def __init__(self):
        self._running = False

    @property
    def running(self):
        return self._running

    def start(self):
        raise InterruptedError()

    def stop(self):
        raise InterruptedError()

