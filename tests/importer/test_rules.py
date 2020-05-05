from stagecrew.importer import (
    Rules,
    RecursiveExclude,
    RecursiveInclude,
    Include,
    Exclude,
    NotApplicable)


def test_rules():
    r = Rules()
    r.add(RecursiveExclude('a'))
    r.add(RecursiveInclude('a.b'))
    r.add(Exclude('a.b.c'))
    r.add(Include('b.c'))

    assert not r.is_included('a')
    assert r.is_included('a.b')
    assert r.is_included('a.b.d')
    assert not r.is_included('a.b.c')
    assert r.is_included('a.b.c.d')
    assert not r.is_included('a.b.d')
    assert r.is_included('b.c')
    assert not r.is_included('b.c.d')
    assert r.is_included('c') is NotApplicable
