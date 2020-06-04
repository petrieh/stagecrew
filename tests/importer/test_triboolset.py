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


def and_method(a, b):
    return a.intersection(b)


def and_operator(a, b):
    return a & b


def and_method_update(a, b):
    a.intersection_update(b)
    return a


def and_operator_update(a, b):
    a &= b
    return a


@pytest.fixture(params=[and_method,
                        and_operator,
                        and_method_update,
                        and_operator_update])
def a_and_b(triboolset_a, triboolset_b, request):
    return request.param(triboolset_a, triboolset_b)


@pytest.fixture(params=['method', 'method_update'])
def set_determined_b_else_a(triboolset_a, triboolset_b, request):
    args = (triboolset_a, triboolset_b)
    return {'method': method_determined_b_else_a(*args),
            'method_update': method_update_determined_b_else_a(*args)}[request.param]


def method_determined_b_else_a(a, b):
    return a.operator(determined_b_else_a, b)


def method_update_determined_b_else_a(a, b):
    a.operator_update(determined_b_else_a, b)
    return a


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


def test_intersection_a_b(a_and_b):
    print(a_and_b)
    assert a_and_b.partially_contains('b')
    for o in ['a', 'c']:
        assert a_and_b.excludes(o)


def test_excludes_iter(triboolset_a):
    assert set(triboolset_a.excludes_iter({'a', 'b', 'c'})) == {'a'}


def test_partially_contains_iter(triboolset_a):
    assert set(triboolset_a.partially_contains_iter({'a', 'b', 'c'})) == {'b'}


def test_fully_contains_iter(triboolset_a):
    assert set(triboolset_a.fully_contains_iter({'a', 'b', 'c'})) == {'c'}


def determined_b_else_a(a, b):
    return a if b is Tribool() else b


def test_operator(triboolset_a, triboolset_b):
    expected = {'a': Tribool(False),
                'b': Tribool(True),
                'c': Tribool(False)}

    c = triboolset_a.operator(determined_b_else_a, triboolset_b)

    assert {o: c.contains_as_tribool(o) for o in ['a', 'b', 'c']} == expected


def test_triboolset_repr(set_determined_b_else_a):
    expected = ['determined_b_else_a']
    expected += ['contains_as_tribool_{}'.format(s) for s in ['a', 'b']]
    actual = repr(set_determined_b_else_a)
    for s in expected:
        assert s in actual
