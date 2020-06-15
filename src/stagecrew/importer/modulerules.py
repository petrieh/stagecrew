from tribool import Tribool
from stagecrew.datatypes.triboolset import (
    TriboolSet,
    DeterminedBElseAContains,
    ContainsBase)


__copyright__ = 'Copyright (C) 2020, Nokia'


def get_triboolset_from_rules(*rules):
    return TriboolSet.create_with_operator(DeterminedBElseAContains, *rules)


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
