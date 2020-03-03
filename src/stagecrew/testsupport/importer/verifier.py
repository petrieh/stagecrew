import abc
from collections import namedtuple
import six

from .task import (
    RemoteEvalExecute,
    RemoteExecute)


__copyright__ = 'Copyright (C) 2020, Nokia'


class Function(namedtuple('Function', ['function', 'arg'])):
    pass


@six.add_metaclass(abc.ABCMeta)
class ImporterVerifierBase(object):

    def __init__(self, package, runner):
        self._package = package
        self._runner = runner

    @abc.abstractmethod
    def verify(self, importer):
        """Verify importer
        """

    def _get_object_for_module_attr(self, module, attr):
        with self._package.tmpdir.as_cwd():
            p = __import__('.'.join([self._package, module]))
            m = getattr(p, module)
            return getattr(m, attr)

    def _run_remote_task(self, task):
        self._runner.task_queue.put(task)
        return self._runner.response_queue.get()


class EndToEndVerifier(ImporterVerifierBase):
    def verify(self, importer):
        arg = 'arg'
        for task in self._tasks(importer, arg):
            importer.import_from_object(task.function)
            assert self._run_remote_task(task) == task.function(arg)

    def _tasks(self, importer, arg):
        yield RemoteEvalExecute(importer=importer,
                                function=Function(function=self._get_function('a'),
                                                  arg=arg))

        for m in ['b', 'c']:
            yield RemoteExecute(importer=importer,
                                function=Function(function=self._get_function(m),
                                                  arg=arg))

    def _get_function(self, module):
        return self._get_object_for_module_attr(
            module=module,
            attr='{module}_func'.format(module=module))
