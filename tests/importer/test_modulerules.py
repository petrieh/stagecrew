from tribool import Tribool
from stagecrew.importer import (
    ModuleRules,
    IncludeRule,
    ExcludeRule,
    RecursiveIncludeRule,
    RecursiveExcludeRule)


def test_modulerules():
    r = ModuleRules()
    r.add(RecursiveExcludeRule('a'))
    r.add(RecursiveIncludeRule('a.b'))
    r.add(ExcludeRule('a.b.c'))
    r.add(IncludeRule('b.c'))

    assert r.contains_as_tribool('a') is Tribool(False)
    assert r.contains_as_tribool('a.b') is Tribool(True)
    assert r.contains_as_tribool('a.b.d') is Tribool(True)
    assert r.contains_as_tribool('a.b.c') is Tribool(False)
    assert r.contains_as_tribool('a.b.c.d') is Tribool(True)
    assert r.contains_as_tribool('b.c') is Tribool(True)
    assert r.contains_as_tribool('b.c.d') is Tribool()
    assert r.contains_as_tribool('c') is Tribool()
