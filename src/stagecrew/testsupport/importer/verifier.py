import abc
from collections import namedtuple
import six


__copyright__ = 'Copyright (C) 2020, Nokia'


class Function(namedtuple('Function', ['module', 'function'])):
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


class EndToEndVerifier(ImporterVerifierBase):
    def verify(self, importer):
        import_and_call = self._get_object_for_module_attr('manager', 'import_and_call')
        incr_importer = importer.eval_dumps(import_and_call)
        self._remote_eval_execute(incr_importer)
        for f in self._functions():
            incr_importer.dumps(f.function)
            importer.import_from_object(f.function)
            arg = 'arg'
            assert self._remote_execute(incr_importer, arg) == f.function(arg)

    def _functions(self):
        for m in ['a', 'b', 'c']:
            yield Function(module=m,
                           function=self._get_function(m))

    def _get_function(self, module):
        return self._get_object_for_module_attr(
            module=module,
            attr='{module}_func'.format(module=module))

    def _remote_eval_execute(self, incr_importer):
        assert 0

    def _remote_execute(self, incr_importer, arg):
        assert 0
