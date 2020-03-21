__copyright__ = 'Copyright (C) 2020, Nokia'


class EExample(object):
    def __init__(self, e):
        self._e = e

    def __eq__(self, other):
        return self._e == other._e


def e_func(arg):
    return EExample(arg)
