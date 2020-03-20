import types
import importlib
import sys
from contextlib import contextmanager
import six
from .metapathsingleton import MetaPathSingleton
from .metapathimporterbase import MetaPathImporterBase

__copyright__ = 'Copyright (C) 2019, Nokia'

__deps__ = ['six', 'MetaPathSingleton', 'MetaPathImporterBase']

# TODO: LocalModule and RemoteModule and their importers LocalImporter can be
# just importer which rewrites attributes and places them into flat (meaning no
# package.subpackage.module keys in sys.modules but just module key as a
# string). If the entry_point is an attribute defined in the package
# __init__.py, then this is handled in local case very same fashion than normal
# module (apart that __path__ is set in that case (to e.g. original __path__).
# However, for remote modules we have to package also __init__.py files for
# each ancestor package of the module.  The special attribute __deps__ is not
# required in the implicit ancestor case as they are formed from __deps__ of
# descendants which matches attribute modules of the package __init__.  All
# other descendant attributes imported are replaced by dummy module, which
# __getattr__ raises NotImplemented error with a proper description that this
# module should be placed into the package __deps__ (or implicit descendant
# __deps__).  In remote case, we have to replace packages from sys.modules
# which according to this procedure, but, as we do not need these packages
# after the import, we should restore the original sys.modules (apart from flat
# locations). This means that the implicit packages are stored during the
# import process into two locations: to the original location and to flat. This
# flat package could be updated (not re-imported) so that those dummy modules
# which are possibly added to implicit __deps__ are replaced by real modules.
# This is optimization as we could of course re-compile packages every time and
# remove also flat package keys after the import process.


class LocalModule(object):
    def __init__(self, entry_point):
        self._entry_point = entry_point
        self._flat = self._create_flat_module()

    @property
    def orig(self):
        return self._entry_point.module

    @property
    def flat(self):
        return self._flat

    def _create_flat_module(self):
        m = types.ModuleType(self._entry_point.module_key)
        c = compile(self._entry_point.source,
                    filename=self._entry_point.module_source_path,
                    mode='exec')
        exec(c, m.__dict__)  # pylint: disable=exec-used
        return m


@six.add_metaclass(MetaPathSingleton)
class LocalMetaPathImporter(MetaPathImporterBase):
    def __init__(self):
        super(LocalMetaPathImporter, self).__init__()
        self._current_module = None
        self._import_data = None
        self._entry_point = None

    def import_from_entry_point(self, entry_point):
        # TODO: Add threading lock as sys.modules for *entry_point* induced
        # original modules are temporarily removed from sys.modules and they
        # may not be added back during the import process.
        with self._import_context():
            with self._moved_orig_modules():
                importlib.import_module(entry_point.module_key)

    @contextmanager
    def _moved_orig_modules(self):
        # TODO: _orig_modules should contain also packages which should be
        # replaced with packages containing only attributes which are found
        # from depended modules. Basically, if key == 'a.b.c' is found from
        # dependencies. Then also packages 'a' and 'a.b' has to be searched and
        # if there are any attribute attr which lives in the module 'a.b.c',
        # then e.g. fullpath=='a.attr' has to be found via
        # find_module('fullpath') the package 'a' must contain only
        # dependencies as attributes More testing is needed here as currently
        # there are no attributes in unit testing packages.  It would be better
        # in the local case to replace depend attributes after the import.
        try:
            for m in self._orig_modules():
                sys.modules.pop(m.__module__, None)
            yield
        finally:
            for m in self._orig_modules():
                sys.modules[m.__module__] = m

    def _orig_modules(self):
        for m in self._local_modules():
            yield m.orig

    def _flat_modules(self):
        for m in self._local_modules():
            yield m.flat

    def _local_modules(self):
        assert 0
