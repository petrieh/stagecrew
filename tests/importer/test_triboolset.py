from tribool import Tribool
from stagecrew.importer import TriboolSet


def contains_as_tribool_factory(s):
    def contains_as_tribool(obj):
        if obj.startswith('c'):
            return Tribool(False)
        return Tribool(True) if obj.startswith(s) else Tribool()

    return contains_as_tribool


BASE_SET_A = {'a', 'ab', 'b', 'c', 'e'}

BASE_SET_B = {'a', 'ab', 'c', 'd', 'e'}


def test_triboolset_intersection():
    a = TriboolSet(contains_as_tribool_factory('a'), BASE_SET_A)
    b = TriboolSet(contains_as_tribool_factory('ab'), BASE_SET_B)

    c = a.intersection(b)

    assert set(c.fully_contains_gen()) == {'ab'}
    assert set(c.partially_contains_gen()) == {'a', 'e'}
