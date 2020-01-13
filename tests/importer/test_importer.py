from multiprocessing import (
    Process,
    Queue)

import pytest

from stagecrew.importer import import_object


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


def test_importer():
    c = import_object(c)
