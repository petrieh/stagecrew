from .a import (
    A,
    a)

__copyright__ = 'Copyright (C) 2020, Nokia'

IMPORTS = [A, a]


class B(A):
    def __init__(self, a, b):
        super(B, self).__init__(a)
        self.b = b


def b(arg):
    return 'b: {}'.format(a(arg))
