import a
from .b import b


__copyright__ = 'Copyright (C) 2020, Nokia'
IMPORTS = [a, b]


def c_func(arg):
    return 'A({arg})={a}, b({arg})={b}'.format(
        arg=arg,
        a=a.A(arg),
        b=b(arg))
