import pytest
from tribool import Tribool
from stagecrew.importer import (
    IncludeRule,
    ExcludeRule,
    RecursiveIncludeRule,
    RecursiveExcludeRule)
from stagecrew.importer.modulerules import get_triboolset_from_rules


def test_get_triboolset_from_rules():
    t = get_triboolset_from_rules(RecursiveExcludeRule('a'),
                                  RecursiveIncludeRule('a.b'),
                                  ExcludeRule('a.b.c'),
                                  IncludeRule('b.c'),
                                  IncludeRule('ab.c'))
    assert t.contains_as_tribool('a') is Tribool(False)
    assert t.contains_as_tribool('ab') is Tribool()
    assert t.contains_as_tribool('a.b') is Tribool(True)
    assert t.contains_as_tribool('a.bd') is Tribool(False)
    assert t.contains_as_tribool('a.b.d') is Tribool(True)
    assert t.contains_as_tribool('a.b.c') is Tribool(False)
    assert t.contains_as_tribool('a.b.c.d') is Tribool(True)
    assert t.contains_as_tribool('b.c') is Tribool(True)
    assert t.contains_as_tribool('b.cd') is Tribool()
    assert t.contains_as_tribool('b.c.d') is Tribool()
    assert t.contains_as_tribool('c') is Tribool()
    assert t.contains_as_tribool('c.a.d') is Tribool()


@pytest.mark.parametrize('rule_cls', [IncludeRule,
                                      ExcludeRule,
                                      RecursiveIncludeRule,
                                      RecursiveExcludeRule])
def test_rule_repr(rule_cls):
    assert repr(rule_cls('module')) == "{cls}('module')".format(cls=rule_cls.__name__)
