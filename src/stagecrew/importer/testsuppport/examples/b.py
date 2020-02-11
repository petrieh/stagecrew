from .a import (
    AExample,
    a_func)

__copyright__ = 'Copyright (C) 2020, Nokia'

__deps__ = ['AExample', a_func]


class BExample(AExample):
    def __init__(self, a, b):
        super(BExample, self).__init__(a)
        self._b = b

    def __eq__(self, other):
        return super(BExample, self).__eq__(other) and self._b == other._b


def b_func(arg):
    return BExample(arg, arg)
