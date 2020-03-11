from .importerbase import ImporterBase

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['ImporterBase']


class IncrImporter(ImporterBase):

    def import_from_object(self, obj):
        self._create_dependency_graph(obj)
        self._create_and_import_modules_if_needed()

    def create_eval_package(self, obj):
        assert 0

    def create_package(self, obj, imports=None):
        assert 0

    def exstract_package(self, package):
        assert 0
