# pylint: disable=redefined-outer-name
import pytest
from tribool import Tribool
from stagecrew.importer import TriboolFuzzySet


def contains_as_tribool_a(s):
    return {'a': Tribool(False),
            'b': Tribool(),
            'c': Tribool(True)}[s]


def contains_as_tribool_b(s):
    return {'a': Tribool(),
            'b': Tribool(True),
            'c': Tribool(False)}[s]


@pytest.fixture
def triboolfuzzyset_a():
    return TriboolFuzzySet(contains_as_tribool_a)


@pytest.fixture
def triboolfuzzyset_b():
    return TriboolFuzzySet(contains_as_tribool_b)


def test_contains_as_tribool(triboolfuzzyset_a):
    for s in ['a', 'b', 'c']:
        assert triboolfuzzyset_a.contains_as_tribool(s) is contains_as_tribool_a(s)


def test_excludes(triboolfuzzyset_a):
    assert triboolfuzzyset_a.excludes('a')
    for s in ['b', 'c']:
        assert not triboolfuzzyset_a.excludes(s)


def test_partially_contains(triboolfuzzyset_a):
    assert triboolfuzzyset_a.partially_contains('b')
    for s in ['a', 'c']:
        assert not triboolfuzzyset_a.partially_contains(s)


def test_fully_contains(triboolfuzzyset_a):
    assert triboolfuzzyset_a.fully_contains('c')
    for s in ['a', 'b']:
        assert not triboolfuzzyset_a.fully_contains(s)


def test_intersection_a_a(triboolfuzzyset_a):
    i = triboolfuzzyset_a.intersection(triboolfuzzyset_a)
    for s in ['a', 'b', 'c']:
        assert i.contains_as_tribool(s) is triboolfuzzyset_a.contains_as_tribool(s)


def test_intersection_a_b(triboolfuzzyset_a, triboolfuzzyset_b):
    i = triboolfuzzyset_a.intersection(triboolfuzzyset_b)
    assert i.partially_contains('b')
    for s in ['a', 'c']:
        assert i.excludes(s)
