import a
from .b import b


IMPORTS = [a, b]


def c(arg):
    return 'A({arg})={a}, b({arg})={b}'.format(
        arg=arg,
        a=a.A(arg),
        b=b(arg))
