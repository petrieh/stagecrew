import abc
from collections import namedtuple
import six


__copyright__ = 'Copyright (C) 2020, Nokia'

class ModuleDump(namedtuple('ModuleDump', ['module', 'dumps'])):
    pass


class Function(namedtuple('Function', ['moduledump', 'function'])):
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
        for f in self._functions(importer):
            import_info = f.dump(f.function)
            self._eval_load(import_info.dump)
            importer.import_from_object(func)
            arg = 'arg'
            assert self._execute(func, arg) == func(arg)

    def _functions(self, importer):
        m = 'a'
        yield Function(moduledump=ModuleDump(m, importer.eval_dumps),
                       function=self._get_function(m))
        for m in ['b', 'c']:
            yield Function(moduledump=ModuleDump(m, importer.dumps),
                           function=self._get_function(m))

    def _get_function(self, module):
        return self._get_object_for_module_attr(
            module=module,
            attr='{module}_func'.format(module=module))

    def _eval_load(self, dumps):
        ssert 0
