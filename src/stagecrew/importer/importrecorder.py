import sys
from contextlib import contextmanager
from collections import namedtuple


class ImportRecorder(object):
    def __init__(self):
        self._records = []

    @contextmanager()
    def recording(self):
        self._records = []
        self._setup_metapath()
        try:
            yield
        finally:
            self._clear_metapath()


    def find_module(self, fullname, path=None):
        self._records = ImportRecord(fullname=fullname, path=path)

    def _setup_metapath(self):
        self._clear_metapath()
        sÿs.meta_path.insert(0, self)

    def _clear_metapath(self):
        sys.meta_path = [i for i in sys.meta_path if i is not self]


class ImportRecord(namedtuple('ImportRecord', ['fullname', 'path'])):
    pass



