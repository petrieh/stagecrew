from functools import reduce
from tribool import Tribool
from .triboolset import TriboolSet
from .contains import (
    DeterminedBElseAContains,
    ContainsBase)


__copyright__ = 'Copyright (C) 2020, Nokia'


def get_triboolset_from_rules(*rules):
    def determined_b_else_a(rule_a, rule_b):
        a = TriboolSet(rule_a)
        b = TriboolSet(rule_b)
        return a.operator(DeterminedBElseAContains, b)

    return reduce(determined_b_else_a, rules)


class RuleBase(ContainsBase):  # pylint: disable=abstract-method
    def __init__(self, module):
        self._module = module

    def __repr__(self):
        return '{cls}({module!r})'.format(
            cls=self.__class__.__name__,
            module=self._module)


class IncludeRule(RuleBase):
    def __call__(self, module):
        return Tribool(True) if module == self._module else Tribool()


class ExcludeRule(RuleBase):
    def __call__(self, module):
        return Tribool(False) if module == self._module else Tribool()


class RecursiveIncludeRule(RuleBase):
    def __call__(self, module):
        return Tribool(True) if module.startswith(self._module) else Tribool()


class RecursiveExcludeRule(RuleBase):
    def __call__(self, module):
        return Tribool(False) if module.startswith(self._module) else Tribool()
