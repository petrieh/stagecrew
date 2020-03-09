import abc
import sys
import importlib
from collections import namedtuple
from contextlib import contextmanager
import six

from .task import (
    RemoteEvalExecuteCreator,
    RemoteExecuteCreator)


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
        with self._tmpdir_in_sys_path():
            full_module_path = '.'.join([self._package.name, module])
            m = importlib.import_module(full_module_path)
            return getattr(m, attr)

    @contextmanager
    def _tmpdir_in_sys_path(self):
        try:
            sys.path.insert(0, str(self._package.tmpdir))
            yield
        finally:
            sys.path = [p for p in sys.path if p != str(self._package.tmpdir)]

    def _run_remote_task(self, task):
        self._runner.task_queue.put(task)
        return self._runner.response_queue.get()


class EndToEndVerifier(ImporterVerifierBase):
    def verify(self, importer):
        arg = 'arg'
        imports = None
        for taskcreator in self._taskcreators(importer, arg):
            f = importer.import_from_object(taskcreator.function)
            task = self._create_task(taskcreator, imports)
            imports = taskcreator.current_package.imports
            assert self._run_remote_task(task) == f(arg)
            assert f(arg) == taskcreator.function(arg)

    @staticmethod
    def _create_task(taskcreator, imports):
        if imports:
            taskcreator.set_imports(imports)
        return taskcreator.create()

    def _taskcreators(self, importer, arg):
        yield RemoteEvalExecuteCreator(
            importer=importer,
            function=Function(function=self._get_function('a'),
                              arg=arg))
        for m in ['b', 'c']:
            yield RemoteExecuteCreator(
                importer=importer,
                function=Function(function=self._get_function(m),
                                  arg=arg))

    def _get_function(self, module):
        return self._get_object_for_module_attr(
            module=module,
            attr='{module}_func'.format(module=module))
