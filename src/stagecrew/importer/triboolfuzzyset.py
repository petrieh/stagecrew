from tribool import Tribool


class TriboolFuzzySet(object):
    """Tribool valued function defined fuzzy set where the membership function
    *m* can be expressed formally e.g. in the following manner::

       m(s) = 0, iff f(s) is Tribool(False),
       m(s) = 1/2, iff f(s) is Tribool() (Undeterminate),
       m(s) = 1, iff f(s) is Tribool(True),

    where f = *contains_as_tribool* mapping from strings to Tribool objects.
    """

    def __init__(self, contains_as_tribool):
        self._contains_as_tribool = contains_as_tribool

    def contains_as_tribool(self, s):
        return self._contains_as_tribool(s)

    def excludes(self, s):
        return self.contains_as_tribool(s) is Tribool(False)

    def partially_contains(self, s):
        return self.contains_as_tribool(s) is Tribool()

    def fully_contains(self, s):
        return self.contains_as_tribool(s) is Tribool(True)

    def intersection(self, other):
        def intersection_func(s):
            return self.contains_as_tribool(s) & other.contains_as_tribool(s)

        return self._create(intersection_func)

    @classmethod
    def _create(cls, contains_as_tribool):
        return cls(contains_as_tribool)
