import abc
import six


@six.add_metaclass(abc.ABCMeta)
class ImporterVerifierBase(object):

    def __init__(self, package, runner):
        self._package = package
        self._runner = runner

    @abc.abstractmethod
    def verify(self, importer):
        """Verify importer
        """

    def _get_object_for_module_and_attr(self, module_name, attr_name):
        with self._package.tmpdir.as_cwd():
            p = __import__('.'.join([self._package, module_name]))
            m = getattr(p, module_name)
            return getattr(m, attr_name)


class EndToEndVerifier(ImporterVerifierBase):
    def verify(self, importer):
        assert 0
