from . import a
from .b import (
    b_func,
    BExample)


__copyright__ = 'Copyright (C) 2020, Nokia'


class CExample(BExample):
    def __init__(self, a_arg, b, c):
        super(CExample, self).__init__(a_arg, b)
        self._c = c

    def __eq__(self, other):
        return super(CExample, self).__eq__(other) and self._c == other._c


def c_func(arg):
    return CExample(a.a_func(arg), b_func(arg), arg)
