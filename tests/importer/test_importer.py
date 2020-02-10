# pylint: disable=redefined-outer-name
import abc
from multiprocessing import (
    Process,
    Queue)

import pytest
from stagecrew import Importer

__copyright__ = 'Copyright (C) 2020, Nokia'



def test_importer(worker):
    # pylint: disable=import-outside-toplevel
    from .examples.c import c_func
    i = Importer()
    e = EvalLoadsTask(i.eval_dumps(c_func))
    worker.task_queue.put(e)
    assert worker.response_queue.get()
    arg = 1
    e = ExecuteTask(c_func, arg)
    worker.task_queue.put(e)
    assert worker.response_queue.get() == c_func(arg)
