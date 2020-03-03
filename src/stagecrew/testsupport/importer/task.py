import abc
import six


__copyright__ = 'Copyright (C) 2020, Nokia'


@six.add_metaclass(abc.ABCMeta)
class Task(object):
    def __init__(self, importer, function):
        self._importer = importer
        self._function = function
        self._package = self._create_package()

    @property
    def function(self):
        return self._function.function

    @abc.abstractmethod
    def run(self):
        """Run task.
        """

    @abc.abstractmethod
    def _create_package(self):
        """Create package from function using importer.
        """


class RemoteEvalExecute(Task):

    def run(self):
        # pylint: disable=eval-used
        exstracted_package = eval(self._package)
        self._importer = exstracted_package.importer
        return exstracted_package.obj(self._function.arg)

    def _create_package(self):
        return self._importer.create_eval_package(self.function)


class RemoteExecute(Task):
    def run(self):
        obj = self._importer.extract_package(self._package)
        return obj(self._function.arg)

    def _create_package(self):
        return self._importer.create_package(self.function)
