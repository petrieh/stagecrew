import types
import sys
from .importerbase import ImporterBase

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['ImporterBase']


class IncrImporter(ImporterBase):

    def import_from_entry_point(self, entry_point):
        e = EntryPoint(entry_point)
        e.import_module()

    def create_eval_package(self, entry_point):
        assert 0

    def create_package(self, entry_point, imports=None):
        assert 0

    def exstract_package(self, package):
        assert 0


class EntryPoint(object):
    def __init__(self, entry_point):
        self._entry_point = entry_point

    def import_module(self):
        assert 0

    @property
    def _module_source_path(self):
        return (self._module_path
                if self._module_path.endswith('.py') else
                self._module_path[:-1])

    @property
    def _module_path(self):
        return self._module.__file__

    @property
    def _module(self):
        return (self._entry_point
                if isinstance(self._entry_point, types.ModuleType) else
                sys.modules[self._entry_point.__module__])
