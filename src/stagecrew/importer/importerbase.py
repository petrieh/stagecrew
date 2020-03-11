import abc
import six

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['six']


@six.add_metaclass(abc.ABCMeta)
class ImporterBase(object):
    """Importer imports modules and creates and extract packages. All
    operations are done for the single *entry_point* which can be a *function*,
    *class* or *module*.
    """

    @abc.abstractmethod
    def import_from_entry_point(self, entry_point):
        """Import modules associated with the *entry_point* and return
        created new *entry_point* from these imported modules.
        """

    @abc.abstractmethod
    def create_eval_package(self, entry_point):
        """Create package from modules associated with *entry_point*. The
        package can be extracted by *eval(package)*.
        The *eval* operation must import modules with propiatary way
        and return an object with attributes:

        - entry_point: *entry_point* from imported modules

        - importer: importer which can be used for extracting packages
          created using :meth:`.create_package`. The importer implementation
          must inherit from this *ImporterBase*.
        """

    @abc.abstractmethod
    def create_package(self, entry_point, imports=None):
        """Create package from moudles associated with *entry_point*. The *imports*
        can contain information about already imported package. The implementation
        may use this information *imports*  and create incremental package instead
        of the package containing all associated modules.
        """

    @abc.abstractmethod
    def exstract_package(self, package):
        """Extract package created by :meth:`.create_package`. Return
        the *entry_point* passed to :meth:`.create_package`.
        """
