from .importerbase import ImporterBase
from .localmetapathimporter import LocalMetaPathImporter
from .entrypoint import EntryPoint


__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['ImporterBase', 'LocalMetaPathImporter']


class IncrImporter(ImporterBase):

    def import_from_entry_point(self, entry_point):
        limporter = LocalMetaPathImporter()
        limporter.import_from_entry_point(EntryPoint(entry_point))

    def create_eval_package(self, entry_point):
        assert 0

    def create_package(self, entry_point, imports=None):
        assert 0

    def exstract_package(self, package):
        assert 0
