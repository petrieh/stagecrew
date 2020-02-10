import abc


class Task(metaclass=abc.ABCMeta):
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
