from contextlib import contextmanager

__copyright__ = 'Copyright (C) 2019, Nokia'


class MetaPathImporterBase(object):
    def __init__(self):
        self._in_import_context = False  # TODO: should be thread local

    @contextmanager
    def _import_context(self):
        self._in_import_context = True
        try:
            yield
        finally:
            self._in_import_context = False
