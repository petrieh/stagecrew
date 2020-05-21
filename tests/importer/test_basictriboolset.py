# pylint: disable=redefined-outer-name
import pytest
from tribool import Tribool
from stagecrew.importer import BasicTriboolSet

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
def basictriboolset_a():
    return BasicTriboolSet(contains_as_tribool_a)


@pytest.fixture
def basictriboolset_b():
    return BasicTriboolSet(contains_as_tribool_b)


def test_contains_as_tribool(basictriboolset_a):
    for o in ['a', 'b', 'c']:
        assert basictriboolset_a.contains_as_tribool(o) is contains_as_tribool_a(o)


def test_excludes(basictriboolset_a):
    assert basictriboolset_a.excludes('a')
    for o in ['b', 'c']:
        assert not basictriboolset_a.excludes(o)


def test_partially_contains(basictriboolset_a):
    assert basictriboolset_a.partially_contains('b')
    for o in ['a', 'c']:
        assert not basictriboolset_a.partially_contains(o)


def test_fully_contains(basictriboolset_a):
    assert basictriboolset_a.fully_contains('c')
    for o in ['a', 'b']:
        assert not basictriboolset_a.fully_contains(o)


def test_intersection_a_a(basictriboolset_a):
    i = basictriboolset_a.intersection(basictriboolset_a)
    for o in ['a', 'b', 'c']:
        assert i.contains_as_tribool(o) is basictriboolset_a.contains_as_tribool(o)


def test_intersection_a_b(basictriboolset_a, basictriboolset_b):
    i = basictriboolset_a.intersection(basictriboolset_b)
    assert i.partially_contains('b')
    for o in ['a', 'c']:
        assert i.excludes(o)
