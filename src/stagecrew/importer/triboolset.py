import operator
from tribool import Tribool


__copyright__ = 'Copyright (C) 2020, Nokia'


class TriboolSet(object):
    """Tribool valued function defined fuzzy set where the membership function
    *m* can be expressed formally e.g. in the following manner::

       m(obj) = 0, if f(obj) is Tribool(False),
       m(obj) = 1/2, if f(obj) is Tribool() (Undeterminate),
       m(obj) = 1, if f(obj) is Tribool(True),

    where f = *contains_as_tribool* is a mapping from Python objects *obj* to
    Tribool objects.
    """

    def __init__(self, contains_as_tribool):
        self._contains_as_tribool = contains_as_tribool

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

    def operator(self, oper, other):
        return self._create(self._create_oper_contains(oper, other))

    def operator_update(self, oper, other):
        self._contains_as_tribool = self._create_oper_contains(oper, other)

    def _create_oper_contains(self, oper, other):
        self_copy = self.copy()
        other_copy = other.copy()

        def oper_contains(obj):
            return oper(self_copy.contains_as_tribool(obj),
                        other_copy.contains_as_tribool(obj))

        return oper_contains

    def copy(self):
        return self._create(self._contains_as_tribool)

    @classmethod
    def _create(cls, contains_as_tribool):
        return cls(contains_as_tribool)

    def __and__(self, other):
        return self.operator(operator.__and__, other)
