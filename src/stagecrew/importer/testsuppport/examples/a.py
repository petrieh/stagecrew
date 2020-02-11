__copyright__ = 'Copyright (C) 2020, Nokia'


class AExample(object):
    def __init__(self, a):
        self._a = a

    def __eq__(self, other):
        return self._a == other._a


def a_func(arg):
    return AExample(arg)
