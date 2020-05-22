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
        def intersection_contains(obj):
            return self.contains_as_tribool(obj) & other.contains_as_tribool(obj)

        return TriboolSet(intersection_contains)
