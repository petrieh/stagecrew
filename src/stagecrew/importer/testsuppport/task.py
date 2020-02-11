import abc
import six


__copyright__ = 'Copyright (C) 2020, Nokia'


@six.add_metaclass(abc.ABCMeta)
class Task(object):
    @abc.abstractmethod
    def run(self):
        """Run task.
        """


class EvalLoadsTask(Task):
    def run(self):
        assert 0


class ExecuteTask(Task):
    def __init__(self, func, *args):
        self._func = func
        self._args = args

    def run(self):
        assert 0
