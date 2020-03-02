from multiprocessing import (
    Process,
    Queue)


__copyright__ = 'Copyright (C) 2020, Nokia'


class Runner(Process):
    def __init__(self):
        super(Runner, self).__init__()
        self._task_queue = Queue()
        self._response_queue = Queue()
        self._state = {}

    @property
    def task_queue(self):
        return self._task_queue

    @property
    def response_queue(self):
        return self._response_queue

    def run(self):
        while True:
            task = self._task_queue.get()
            task.set_state(self._state)
            if not task:
                break
            self.response_queue.put(task.run())
