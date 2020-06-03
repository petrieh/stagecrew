import operator
from collections import namedtuple
from tribool import Tribool


__copyright__ = 'Copyright (C) 2020, Nokia'


class TriboolSet(object):
    """Tribool valued function defined fuzzy set where the membership function
    *m* can be expressed formally e.g. in the following manner::

       m(obj) = 0, if f(obj) is Tribool(False),
       m(obj) = 1/2, if f(obj) is Tribool() (Undeterminate),
       m(obj) = 1, if f(obj) is Tribool(True),

    where f = *contains_as_tribool* is a callable with Python objects *obj* argument
    returning Tribool object.
    """

    def __init__(self, contains_as_tribool):
        self._contains_as_tribool = contains_as_tribool

    def __repr__(self):
        return '{cls}({contains_as_tribool})'.format(
            cls=self.__class__.__name__,
            contains_as_tribool=self._contains_as_tribool)

    def contains_as_tribool(self, obj):
        return self._contains_as_tribool(obj)

    def excludes(self, obj):
        return self.contains_as_tribool(obj) is Tribool(False)

    def excludes_iter(self, iterable):
        return filter(self.excludes, iterable)

    def partially_contains(self, obj):
        return self.contains_as_tribool(obj) is Tribool()

    def partially_contains_iter(self, iterable):
        return filter(self.partially_contains, iterable)

    def fully_contains(self, obj):
        return self.contains_as_tribool(obj) is Tribool(True)

    def fully_contains_iter(self, iterable):
        return filter(self.fully_contains, iterable)

    def intersection(self, other):
        return self & other

    def intersection_update(self, other):
        self.operator_update(operator.__and__, other)

    def __and__(self, other):
        return self.operator(operator.__and__, other)

    def operator(self, oper, other):
        return self._create(self._create_set_operation(oper, other))

    def operator_update(self, oper, other):
        self._contains_as_tribool = self._create_set_operation(oper, other)

    def _create_set_operation(self, oper, other):
        return SetOperation(oper=oper, a=self.copy(), b=other.copy())

    def copy(self):
        return self._create(self._contains_as_tribool)

    @classmethod
    def _create(cls, contains_as_tribool):
        return cls(contains_as_tribool)


class SetOperation(namedtuple('SetOperation', ['oper', 'a', 'b'])):
    """Functor implementing contains_as_tribool for combined TriboolSet defined
    by operator *oper* and TriboolSet operands *a* and *b*.

    Arguments follow PN (Polish notation) order.

    Args:
        oper(callable): Set operation operator
        a(TriboolSet): left operand
        b(TriboolSet): right operand
    """
    def __call__(self, obj):
        return self.oper(self.a.contains_as_tribool(obj),
                         self.b.contains_as_tribool(obj))
