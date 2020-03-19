import sys
import types
import hashlib

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['six']


class EntryPoint(object):
    def __init__(self, entry_point):
        self._entry_point = entry_point
        self._uniq_entry_points = set()
        self._initialize_uniq_entry_points()

    def __hash__(self):
        return self.module_key

    @property
    def module_key(self):
        """New key of the module in *sys.modules*
        .. note:
            Keys depend on source sha256. If the source is repeatedly
            changed, this may cause memory leak. All keys
            for particular path can be removed by removing modules from
            *sys.modules* if path == key[:-65].
        """
        return '{module_source_path}_{source_hash}'.format(
            module_source_path=self.module_source_path,
            source_hash=self._source_hash)

    @property
    def _source_hash(self):
        return hashlib.sha256(self.source).hexdigest()

    @property
    def source(self):
        with open(self.module_source_path, 'rb') as f:
            return f.read()

    @property
    def module_source_path(self):
        return (self._module_path
                if self._module_path.endswith('.py') else
                self._module_path[:-1])

    @property
    def _module_path(self):
        return self.module.__file__

    @property
    def uniq_entry_points(self):
        return self._uniq_entry_points

    def _initialize_uniq_entry_points(self):
        self._uniq_entry_points.add(self)
        for c in set(self._child_entry_points):
            self._uniq_entry_points += c.uniq_entry_points

    @property
    def _module_deps(self):
        return self.module.__deps__

    @property
    def module(self):
        return (self._entry_point
                if isinstance(self._entry_point, types.ModuleType) else
                sys.modules[self._entry_point.__module__])



