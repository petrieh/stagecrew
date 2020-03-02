import abc
import six


__copyright__ = 'Copyright (C) 2020, Nokia'


@six.add_metaclass(abc.ABCMeta)
class Task(object):
    @abc.abstractmethod
    def run(self):
        """Run task.
        """


class RemoteEvalExecute(Task):
    def __init__(self, eval_dumps):
        self._eval_dumps = eval_dumps
        self._import_and_call = None

    def run(self):
        # pylint: disable=eval-used
        self._import_and_call = eval(self._eval_dumps)


class RemoteExecuteTask(Task):
    def __init__(self, func, *args):
        self._func = func
        self._args = args

    def run(self):
        assert 0
