from tribool import Tribool
from .basictriboolset import BasicTriboolSet

__copyright__ = 'Copyright (C) 2020, Nokia'


class TriboolSet(BasicTriboolSet):
    def __init__(self, contains_as_tribool, base_set):
        super(TriboolSet, self).__init__(contains_as_tribool)
        self._base_set = base_set

    @property
    def base_set(self):
        return self._base_set

    def contains_as_tribool(self, obj):
        return self._contains_as_tribool(obj) if obj in self.base_set else Tribool(False)

    def intersection(self, other):
        base_set_intersection = self.base_set.intersection(other.base_set)
        super_inst = super(TriboolSet, self).intersection(other)
        return TriboolSet(super_inst.contains_as_tribool, base_set_intersection)

    def partially_contains_gen(self):
        for o in self.base_set:
            if self.partially_contains(o):
                yield o

    def fully_contains_gen(self):
        for o in self.base_set:
            if self.fully_contains(o):
                yield o
