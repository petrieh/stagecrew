import sys

__copyright__ = 'Copyright (C) 2019, Nokia'


class MetaPathSingleton(type):
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
    instance = super(MetaPathSingleton, cls).__call__(*args, **kwargs)
    sys.meta_path.insert(0, instance)
    return instance
