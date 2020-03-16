import types
import importlib
import six
from .metapathsingleton import MetaPathSingleton
from .metapathimporterbase import MetaPathImporterBase

__copyright__ = 'Copyright (C) 2019, Nokia'

__deps__ = ['six', 'MetaPathSingleton', 'MetaPathImporterBase']


class LocalModule(types.ModuleType):
    def __init__(self, importdata, *args, **kwargs):
        super(LocalModule, self).__init__(*args, **kwargs)
        self.__importdata__ = importdata


@six.add_metaclass(MetaPathSingleton)
class LocalMetaPathImporter(MetaPathImporterBase):
    def __init__(self):
        super(LocalMetaPathImporter, self).__init__()
        self._current_module = None
        self._import_data = None
        self._entry_point = None

    def import_from_entry_point(self, entry_point):
        with self._import_context():
            self._entry_point = entry_point
            importlib.import_module(entry_point.module_source_path)

    def find_module(self, fullname, path=None):
        assert 0, (fullname, path)

    def load_module(self, fullname):
        assert 0
