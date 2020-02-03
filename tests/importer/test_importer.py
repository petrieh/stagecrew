# pylint: disable=redefined-outer-name
from multiprocessing import (
    Process,
    Queue)

import pytest
from stagecrew.importer import create_eval_archive
from .examples.c import c_func


__copyright__ = 'Copyright (C) 2020, Nokia'


class Worker(Process):
    def __init__(self):
        self._queue = Queue()

    @property
    def queue(self):
        return self._queue

    def run(self):
        while True:
            task = self._queue.get()
            if not task:
                break
            task.run()


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

class EvalArchiveImportTask:
    assert 0


def test_importer(worker):
    a = create_eval_archive(c_func)
    worker.run_eval_archive_
