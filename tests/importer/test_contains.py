from tribool import Tribool
from stagecrew.importer.contains import (
    AllFalseContains,
    AllIndeterminateContains,
    AllTrueContains)


__copyright__ = 'Copyright (C) 2020, Nokia'


def test_all_false_contains():
    c = AllFalseContains()
    assert c('any-value') is Tribool(False)
    assert repr(c) == 'AllFalseContains()'


def test_all_indeterminate_contains():
    c = AllIndeterminateContains()
    assert c('any-value') is Tribool()
    assert repr(c) == 'AllIndeterminateContains()'


def test_all_true_contains():
    c = AllTrueContains()
    assert c('any-value') is Tribool(True)
    assert repr(c) == 'AllTrueContains()'
