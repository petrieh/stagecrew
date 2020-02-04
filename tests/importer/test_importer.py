# pylint: disable=redefined-outer-name
from multiprocessing import (
    Process,
    Queue)

import pytest
from stagecrew import Importer

__copyright__ = 'Copyright (C) 2020, Nokia'


class Worker(Process):
    def __init__(self):
        self._task_queue = Queue()
        self._response_queue = Queue()

    @property
    def task_queue(self):
        return self._task_queue

    @property
    def response_queue(self):
        return self._response_queue

    def run(self):
        while True:
            task = self._task_queue.get()
            if not task:
                break
            self.response_queue.put(task.run())


@pytest.fixture(scope='module')
def worker():
    try:
        p = Worker()
        p.start()
        yield p
    finally:
        p.queue('')
        try:
            p.close()
        except ValueError:
            p.kill()


class Task(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        """Run task.
        """

class EvalLoadsTask:
    assert 0


def test_importer(worker):
    from .examples.a import A
    i = Importer()
    e = EvalLoadsTask(i.eval_dumps(A))
    worker.task_queue.put(e)
    response = worker.response_queue.get()
    assert




