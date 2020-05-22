import abc
import six
from tribool import Tribool


__copyright__ = 'Copyright (C) 2020, Nokia'


class ModuleRules(object):
    def __init__(self):
        self._rules = []

    def add(self, rule):
        self._rules.append(rule)

    @property
    def triboolset(self):
        assert 0

    def contains_as_tribool(self, module):
        """This is the same as applying rules using the expression
        a & ?b | b & ~?b.
        """
        contains = Tribool()
        for contains in self._boolean_contains_gen(module):
            pass

        return contains

    def _boolean_contains_gen(self, module):
        for r in self._rules:
            contains = r.contains_as_tribool(module)
            if contains is not Tribool():
                yield contains


@six.add_metaclass(abc.ABCMeta)
class RuleBase(object):
    def __init__(self, module):
        self._module = module

    @abc.abstractmethod
    def contains_as_tribool(self, module):
        """Return:

          - Tribool(True), if module is included according to this rule.
          - Tribool(False), if module is not included according to this rule.
          - Tribool() (== Tribool('Unknown')), if the inclusion cannot be
            determined by this rule.  """


class IncludeRule(RuleBase):
    def contains_as_tribool(self, module):
        return Tribool(True) if module == self._module else Tribool()


class ExcludeRule(RuleBase):
    def contains_as_tribool(self, module):
        return Tribool(False) if module == self._module else Tribool()


class RecursiveIncludeRule(RuleBase):
    def contains_as_tribool(self, module):
        return Tribool(True) if module.startswith(self._module) else Tribool()


class RecursiveExcludeRule(RuleBase):
    def contains_as_tribool(self, module):
        return Tribool(False) if module.startswith(self._module) else Tribool()
