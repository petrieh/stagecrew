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
    print(t)
    assert t.contains_as_tribool('a') is Tribool(False)
    assert t.contains_as_tribool('a.b') is Tribool(True)
    assert t.contains_as_tribool('a.b.d') is Tribool(True)
    assert t.contains_as_tribool('a.b.c') is Tribool(False)
    assert t.contains_as_tribool('a.b.c.d') is Tribool(True)
    assert t.contains_as_tribool('b.c') is Tribool(True)
    assert t.contains_as_tribool('b.c.d') is Tribool()
    assert t.contains_as_tribool('c') is Tribool()
