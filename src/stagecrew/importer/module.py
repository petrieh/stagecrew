import sys
import types
import six

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['six']


class SysMetaPathSingleton(type):
    def __call__(cls, *args, **kwargs):
        for instance in _instances_for_cls(cls):
            return instance

        return _create_instance(cls, *args, **kwargs)


def _instances_for_cls(cls):
    for instance in sys.meta_path:
        try:
            if isinstance(instance, cls) and cls is instance.__class__:
                yield instance

        except AttributeError:
            continue


def _create_instance(cls, *args, **kwargs):
    instance = super(SysMetaPathSingleton, cls).__call__(*args, **kwargs)
    sys.meta_path.insert(instance, 0)
    return instance


class LocalModule(types.ModuleType):
    def __init__(self, importdata, *args, **kwargs):
        super(LocalModule, self).__init__(*args, **kwargs)
        self.__importdata__ = importdata


@six.add_metaclass(SysMetaPathSingleton)
class LocalFinder(object):
    def __init__(self):
        assert 0
