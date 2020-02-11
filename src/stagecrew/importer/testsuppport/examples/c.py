from . import a
from .b import (
    b_func,
    BExample)


__copyright__ = 'Copyright (C) 2020, Nokia'
# __deps__ is importer metadata containing list of attribute objects or
# alternatively attribute names as strings of the module which this module
# depends on and which has to be imported and packaged by the importer.
__deps__ = [a, 'b_func', BExample]


class CExample(BExample):
    def __init__(self, a_arg, b, c):
        super(CExample, self).__init__(a_arg, b)
        self._c = c

    def __eq__(self, other):
        return super(CExample, self).__eq__(other) and self._c == other._c


def c_func(arg):
    return CExample(a.a_func(arg), b_func(arg), arg)
