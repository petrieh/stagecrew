from .a import (
    A,
    a)


IMPORTS = [A, a]


class B(A):
    def __init__(self, a, b):
        super(B, self).__init__(a)
        self.b = b


def b(arg):
    return 'b: {}'.format(a(arg))
