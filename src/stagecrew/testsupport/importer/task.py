import abc
import six


__copyright__ = 'Copyright (C) 2020, Nokia'


@six.add_metaclass(abc.ABCMeta)
class Task(object):
    _importer = None

    def __init__(self, package, arg):
        self._package = package
        self._arg = arg

    @abc.abstractmethod
    def run(self):
        """Run task
        """


@six.add_metaclass(abc.ABCMeta)
class TaskCreator(object):
    def __init__(self, importer, function):
        self._importer = importer
        self._function = function
        self._package = self._create_package()

    @property
    def function(self):
        return self._function.function

    def create(self):
        return self._task_cls(self._package, self.function.arg)

    @abc.abstractmethod
    def _create_package(self):
        """Create package from function using importer.
        """

    @property
    @abc.abstractmethod
    def _task_cls(self):
        """Return task class to be created"""


class RemoteEvalExecute(Task):
    def run(self):
        # pylint: disable=eval-used
        exstracted_package = eval(self._package)
        self._importer = exstracted_package.importer
        return exstracted_package.obj(self._arg)


class RemoteEvalExecuteCreator(TaskCreator):

    def _create_package(self):
        return self._importer.create_eval_package(self.function)

    @property
    def _task_cls(self):
        return RemoteEvalExecute


class RemoteExecute(Task):
    def run(self):
        obj = self._importer.extract_package(self._package)
        return obj(self._arg)


class RemoteExecuteCreator(TaskCreator):
    def _create_package(self):
        return self._importer.create_package(self.function)

    @property
    def _task_cls(self):
        return RemoteExecute
