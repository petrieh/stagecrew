import sys
from contextlib import contextmanager
from collections import namedtuple

__copyright__ = 'Copyright (C) 2020, Nokia'


class ImportRecorder(object):
    def __init__(self):
        self._records = []
        self._modulerules = None

    def set_modulerules(self, modulerules):
        self._modulerules = modulerules

    @contextmanager
    def recording(self):
        self._records = []
        self._clear_modules_cache()
        self._setup_metapath()
        try:
            yield
        finally:
            self._clear_metapath()

    @property
    def records(self):
        return self._records

    def find_module(self, fullname, path=None):
        self._records.append(ImportRecord(fullname=fullname, path=path))

    def _clear_modules_cache(self):
        for m in sys.modules.copy():
            assert 0

    def _clear_metapath(self):
        sys.meta_path = [i for i in sys.meta_path if i is not self]

    def _setup_metapath(self):
        self._clear_metapath()
        sys.meta_path.insert(0, self)


class ImportRecord(namedtuple('ImportRecord', ['fullname', 'path'])):
    pass
