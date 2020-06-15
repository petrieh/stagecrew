# pylint: disable=redefined-outer-name

import operator
import itertools
from functools import reduce
import pytest
from tribool import Tribool
from stagecrew.datatypes.triboolset import (
    TriboolSet,
    DeterminedBElseAContains)


__copyright__ = 'Copyright (C) 2020, Nokia'


TRIBOOL_VALUES = [Tribool(False), Tribool(), Tribool(True)]

TRIBOOL_SQUARE = list(itertools.product(TRIBOOL_VALUES, TRIBOOL_VALUES))


@pytest.fixture
def a_and_b(and_operator, triboolset_a, triboolset_b):
    return and_operator(triboolset_a, triboolset_b)


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


@pytest.fixture
def triboolset_a():
    return TriboolSet(contains_as_tribool_a)


@pytest.fixture
def triboolset_b():
    return TriboolSet(contains_as_tribool_b)


def contains_as_tribool_a(obj):
    f = contains_as_tribool_factory(0)
    return f(obj)


def contains_as_tribool_b(obj):
    f = contains_as_tribool_factory(1)
    return f(obj)


def contains_as_tribool_c(obj):
    f = contains_as_tribool_factory(0)
    g = contains_as_tribool_factory(1)

    if f(obj) is Tribool():
        return Tribool(True)
    return Tribool(False) if g(obj) is Tribool() else Tribool()


def contains_as_tribool_factory(i):
    def contains_as_tribool(obj):
        return obj[i]

    return contains_as_tribool


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


def test_contains_as_tribool(triboolset_a):
    for o in TRIBOOL_SQUARE:
        assert triboolset_a.contains_as_tribool(o) is contains_as_tribool_a(o)


def test_excludes(triboolset_a):
    for o in TRIBOOL_SQUARE:
        assert triboolset_a.excludes(o) == (contains_as_tribool_a(o) is Tribool(False))


def test_partially_contains(triboolset_a):
    for o in TRIBOOL_SQUARE:
        expected = contains_as_tribool_a(o) is Tribool()
        assert triboolset_a.partially_contains(o) == expected


def test_fully_contains(triboolset_a):
    for o in TRIBOOL_SQUARE:
        expected = contains_as_tribool_a(o) is Tribool(True)
        assert triboolset_a.fully_contains(o) == expected


def test_intersection_a_a(triboolset_a):
    i = triboolset_a.intersection(triboolset_a)
    for o in TRIBOOL_SQUARE:
        assert i.contains_as_tribool(o) is triboolset_a.contains_as_tribool(o)


def test_intersection_a_b(a_and_b):
    for o in TRIBOOL_SQUARE:
        expected = contains_as_tribool_a(o) & contains_as_tribool_b(o)
        assert a_and_b.contains_as_tribool(o) is expected


def test_excludes_iter(triboolset_a):
    expected = [o for o in TRIBOOL_SQUARE if contains_as_tribool_a(o) is Tribool(False)]
    assert list(triboolset_a.excludes_iter(TRIBOOL_SQUARE)) == expected


def test_partially_contains_iter(triboolset_a):
    expected = [o for o in TRIBOOL_SQUARE if contains_as_tribool_a(o) is Tribool()]
    assert list(triboolset_a.partially_contains_iter(TRIBOOL_SQUARE)) == expected


def test_fully_contains_iter(triboolset_a):
    expected = [o for o in TRIBOOL_SQUARE if contains_as_tribool_a(o) is Tribool(True)]
    assert list(triboolset_a.fully_contains_iter(TRIBOOL_SQUARE)) == expected


def determined_b_else_a(a, b):
    return a if b is Tribool() else b


def test_operator(triboolset_a, triboolset_b):
    c = triboolset_a.operator(determined_b_else_a, triboolset_b)
    for o in TRIBOOL_SQUARE:
        expected = determined_b_else_a(triboolset_a.contains_as_tribool(o),
                                       triboolset_b.contains_as_tribool(o))
        assert c.contains_as_tribool(o) is expected


def test_triboolset_repr(set_determined_b_else_a):
    expected = ['Tribool', 'determined_b_else_a']
    expected += ['contains_as_tribool_{}'.format(s) for s in ['a', 'b']]
    actual = repr(set_determined_b_else_a)
    for s in expected:
        assert s in actual


def test_functor_determined_b_else_a(functor_set_determined_b_else_a):
    for o in TRIBOOL_SQUARE:
        actual = functor_set_determined_b_else_a.contains_as_tribool(o)
        expected = determined_b_else_a(contains_as_tribool_a(o),
                                       contains_as_tribool_b(o))
        assert actual is expected


def test_triboolset_as_triboolset_arg(triboolset_a):
    t = TriboolSet(triboolset_a)
    for o in TRIBOOL_SQUARE:
        expected = triboolset_a.contains_as_tribool(o)
        assert t.contains_as_tribool(o) is expected


@pytest.fixture(params=range(9))
def sets_for_create(triboolset_a, triboolset_b, request):
    sets = [[triboolset_a, triboolset_b, contains_as_tribool_c][:i] for i in range(1, 4)]
    return [s for t in sets for s in itertools.permutations(t)][request.param]


@pytest.mark.parametrize('operator', [determined_b_else_a, DeterminedBElseAContains])
def test_triboolset_create_with_operator(operator, sets_for_create):
    t = TriboolSet.create_with_operator(operator, *sets_for_create)
    expected_contains_as_tribool = create_expected_contains_as_tribool(sets_for_create)
    for o in TRIBOOL_SQUARE:
        assert t.contains_as_tribool(o) is expected_contains_as_tribool(o), o


def create_expected_contains_as_tribool(sets):
    def get_contains_as_tribool(s):
        return s.contains_as_tribool if isinstance(s, TriboolSet) else s

    expected_funcs = list(map(get_contains_as_tribool, sets))

    def contains_as_tribool(obj):
        expected_tribools = [f(obj) for f in expected_funcs]
        # pylint: disable=arguments-out-of-order
        return reduce(lambda a, b: determined_b_else_a(b, a),
                      reversed(expected_tribools))

    return contains_as_tribool
