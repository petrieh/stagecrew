# pylint: disable=redefined-outer-name

import operator
from collections import namedtuple
import pytest
from tribool import Tribool
from stagecrew.importer import TriboolSet
from stagecrew.importer.contains import DeterminedBElseAContains


__copyright__ = 'Copyright (C) 2020, Nokia'


def contains_as_tribool_a(s):
    return {'a': Tribool(False),
            'b': Tribool(),
            'c': Tribool(True),
            'd': Tribool(),
            'e': Tribool(True),
            'f': Tribool(False),
            'g': Tribool(False),
            'h': Tribool(),
            'i': Tribool(True)}[s]


def contains_as_tribool_b(s):
    return {'a': Tribool(),
            'b': Tribool(True),
            'c': Tribool(False),
            'd': Tribool(False),
            'e': Tribool(),
            'f': Tribool(True),
            'g': Tribool(False),
            'h': Tribool(),
            'i': Tribool(True)}[s]


@pytest.fixture
def triboolset_a():
    return TriboolSet(contains_as_tribool_a)


@pytest.fixture
def triboolset_b():
    return TriboolSet(contains_as_tribool_b)


def and_method(a, b):
    return a.intersection(b)


def and_method_update(a, b):
    a.intersection_update(b)
    return a


def and_operator_update(a, b):
    a &= b
    return a


def multi_and_method_update(a, b):
    a.intersection_update(b)
    b.intersection_update(a)
    a.intersection_update(b)
    return a


@pytest.fixture(params=[operator.__and__,
                        and_method,
                        and_method_update,
                        and_operator_update,
                        multi_and_method_update])
def and_operator(request):
    return request.param


@pytest.fixture(params=[iter, reversed])
def and_operargiter(request, and_operator):
    return OperArgiter(oper=and_operator, argiter=request.param)


class OperArgiter(namedtuple('OperRever', ['oper', 'argiter'])):
    def __call__(self, a, b):
        return self.oper(*self.argiter((a, b)))


@pytest.fixture
def a_and_b(and_operargiter, triboolset_a, triboolset_b):
    return and_operargiter(triboolset_a, triboolset_b)


def functor_determined_b_else_a(a, b):
    return a.operator(DeterminedBElseAContains, b)


def functor_update_determined_b_else_a(a, b):
    a.operator_update(DeterminedBElseAContains, b)
    return a

@pytest.fixture(params=[functor_determined_b_else_a,
                        functor_update_determined_b_else_a])
def functor_set_determined_b_else_a(request, triboolset_a, triboolset_b):
    return request.param(triboolset_a, triboolset_b)


def method_determined_b_else_a(a, b):
    return a.operator(determined_b_else_a, b)


def method_update_determined_b_else_a(a, b):
    a.operator_update(determined_b_else_a, b)
    return a


@pytest.fixture(params=[method_determined_b_else_a,
                        method_update_determined_b_else_a])
def set_determined_b_else_a(triboolset_a, triboolset_b, request):
    return request.param(triboolset_a, triboolset_b)


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


def test_functor_determined_b_else_a(functor_set_determined_b_else_a):
    for o in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
        actual = functor_set_determined_b_else_a.contains_as_tribool(o)
        expected = determined_b_else_a(contains_as_tribool_a(o),
                                       contains_as_tribool_b(o))
        assert actual is expected
