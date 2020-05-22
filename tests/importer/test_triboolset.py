# pylint: disable=redefined-outer-name
import pytest
from tribool import Tribool
from stagecrew.importer import TriboolSet

__copyright__ = 'Copyright (C) 2020, Nokia'


def contains_as_tribool_a(s):
    return {'a': Tribool(False),
            'b': Tribool(),
            'c': Tribool(True)}[s]


def contains_as_tribool_b(s):
    return {'a': Tribool(),
            'b': Tribool(True),
            'c': Tribool(False)}[s]


@pytest.fixture
def triboolset_a():
    return TriboolSet(contains_as_tribool_a)


@pytest.fixture
def triboolset_b():
    return TriboolSet(contains_as_tribool_b)


def test_contains_as_tribool(triboolset_a):
    for o in ['a', 'b', 'c']:
        assert triboolset_a.contains_as_tribool(o) is contains_as_tribool_a(o)


def test_excludes(triboolset_a):
    assert triboolset_a.excludes('a')
    for o in ['b', 'c']:
        assert not triboolset_a.excludes(o)


def test_partially_contains(triboolset_a):
    assert triboolset_a.partially_contains('b')
    for o in ['a', 'c']:
        assert not triboolset_a.partially_contains(o)


def test_fully_contains(triboolset_a):
    assert triboolset_a.fully_contains('c')
    for o in ['a', 'b']:
        assert not triboolset_a.fully_contains(o)


def test_intersection_a_a(triboolset_a):
    i = triboolset_a.intersection(triboolset_a)
    for o in ['a', 'b', 'c']:
        assert i.contains_as_tribool(o) is triboolset_a.contains_as_tribool(o)


def test_intersection_a_b(triboolset_a, triboolset_b):
    i = triboolset_a.intersection(triboolset_b)
    assert i.partially_contains('b')
    for o in ['a', 'c']:
        assert i.excludes(o)


def test_excludes_iter(triboolset_a):
    assert set(triboolset_a.excludes_iter({'a', 'b', 'c'})) == {'a'}


def test_partially_contains_iter(triboolset_a):
    assert set(triboolset_a.partially_contains_iter({'a', 'b', 'c'})) == {'b'}


def test_fully_contains_iter(triboolset_a):
    assert set(triboolset_a.fully_contains_iter({'a', 'b', 'c'})) == {'c'}
