from . import a
from .b import b


__copyright__ = 'Copyright (C) 2020, Nokia'
# __deps__ is importer metadata containing list of attribute objects or
# alternatively attribute names as strings of the module which this module
# depends on and which has to be imported and packaged by the importer.
__deps__ = [a, b]


def c_func(arg):
    return 'A({arg})={a}, b({arg})={b}'.format(
        arg=arg,
        a=a.A(arg),
        b=b(arg))
