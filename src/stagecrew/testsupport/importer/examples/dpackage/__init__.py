__copyright__ = 'Copyright (C) 2020, Nokia'


class DExample(object):
    def __init__(self, d):
        self._d = d

    def __eq__(self, other):
        return self._d == other._d


def d_func(arg):
    return DExample(arg)
