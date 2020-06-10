from tribool import Tribool
import six
from .contains import (
    OperatorContains,
    OperandsContainsBase,
    LazyLeftAndContains)

__copyright__ = 'Copyright (C) 2020, Nokia'


class TriboolSet(object):
    """Tribool valued function defined fuzzy set where the membership function
    *m* can be expressed formally e.g. in the following manner::

       m(obj) = 0, if f(obj) is Tribool(False),
       m(obj) = 1/2, if f(obj) is Tribool() (Undeterminate),
       m(obj) = 1, if f(obj) is Tribool(True),

    where f = *contains_as_tribool* is a callable with Python objects *obj* argument
    returning Tribool object. For convenience, also TriboolSet object can be
    given as *contains_as_tribool* function.
    """

    def __init__(self, contains_as_tribool):
        self._contains_as_tribool = (
            contains_as_tribool._contains_as_tribool
            if isinstance(contains_as_tribool, TriboolSet) else
            contains_as_tribool)

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
        self._contains_as_tribool = self._create_contains(LazyLeftAndContains, other)

    def _create_contains(self, contains_factory, other):
        return contains_factory(a=self.copy(), b=other.copy())

    def __and__(self, other):
        return self.operator(LazyLeftAndContains, other)

    def operator(self, oper, other):
        contains_factory = self._get_contains_factory(oper)
        return self._create(self._create_contains(contains_factory, other))

    def operator_update(self, oper, other):
        contains_factory = self._get_contains_factory(oper)
        self._contains_as_tribool = self._create_contains(contains_factory, other)

    def copy(self):
        return self._create(self._contains_as_tribool)

    @classmethod
    def _create(cls, contains_as_tribool):
        return cls(contains_as_tribool)

    @staticmethod
    def _get_contains_factory(oper):
        is_operands_contains = (
            isinstance(oper, six.class_types) and issubclass(oper, OperandsContainsBase))
        return oper if is_operands_contains else OperatorContains.create_factory(oper)
