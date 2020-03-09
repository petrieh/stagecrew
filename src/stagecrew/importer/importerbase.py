import abc
import six

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['six']


@six.add_metaclass(abc.ABCMeta)
class ImporterBase(object):

    @abc.abstractmethod
    def import_from_object(self, obj):
        """Import modules associated with the object *obj* and return *obj*
        from these imported modules.
        """

    @abc.abstractmethod
    def create_eval_package(self, obj):
        """Create package from modules associated with *obj*. The
        package can be extracted by *eval(package)*. The return
        value of *eval* must be object containing the following attributes

        - obj: the object *obj*

        - importer: importer which can be used for extracting packages
          created using :meth:`.create_package`. The importer implementation
          must inherit from this *ImporterBase*.
        """

    @abc.abstractmethod
    def create_package(self, obj, imports=None):
        """Create package from moudles associated with *obj*. The *imports*
        can contain information about already imported package. The implementation
        may use this information *imports*  and create incremental package instead
        of the package containing all associated modules.
        """

    @abc.abstractmethod
    def exstract_package(self, package):
        """Extract package created by :meth:`.create_package`. Return
        the *obj* passed to :meth:`.create_package`.
        """
