import abc
import six


__copyright__ = 'Copyright (C) 2020, Nokia'


@six.add_metaclass(abc.ABCMeta)
class Task(object):
    def __init__(self):
        self._state = {}

    @abc.abstractmethod
    def run(self):
        """Run task.
        """

    def set_state(self, state):
        self._state = state


class RemoteEvalExecute(Task):
    import_and_call = 'import_and_call'

    def __init__(self, eval_dumps):
        super(RemoteEvalExecute, self).__init__()
        self._eval_dumps = eval_dumps

    def run(self):
        # pylint: disable=eval-used
        self._state[self.import_and_call] = eval(self._eval_dumps)


class RemoteExecute(Task):
    def __init__(self, dumps, *args):
        super(RemoteExecute, self).__init__()
        self._dumps = dumps
        self._args = args

    def run(self):
        import_and_call = self._state[RemoteEvalExecute.import_and_call]
        return import_and_call(self._dumps, *self._args)
