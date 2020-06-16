import re
import abc
import six
from tribool import Tribool
from stagecrew.datatypes.triboolset import (
    TriboolSet,
    DeterminedBElseAContains,
    ContainsBase)


__copyright__ = 'Copyright (C) 2020, Nokia'


def get_triboolset_from_rules(*rules):
    return TriboolSet.create_with_operator(DeterminedBElseAContains, *rules)


@six.add_metaclass(abc.ABCMeta)
class RuleBase(ContainsBase):
    def __init__(self, module):
        self._module = module

    def __call__(self, module):
        return self._tribool_in_match if self._match(module) else Tribool()

    @property
    @abc.abstractmethod
    def _tribool_in_match(self):
        """Tribool value in case of match.
        """

    @abc.abstractmethod
    def _match(self, module):
        """Return value which bool conversion is True if *module* matches the
        rule else False.
        """

    def __repr__(self):
        return '{cls}({module!r})'.format(
            cls=self.__class__.__name__,
            module=self._module)


@six.add_metaclass(abc.ABCMeta)
class IncludeRuleBase(RuleBase):
    @property
    def _tribool_in_match(self):
        return Tribool(True)


@six.add_metaclass(abc.ABCMeta)
class ExcludeRuleBase(RuleBase):
    @property
    def _tribool_in_match(self):
        return Tribool(False)


@six.add_metaclass(abc.ABCMeta)
class ExactRuleBase(RuleBase):
    def _match(self, module):
        return self._module == module


@six.add_metaclass(abc.ABCMeta)
class RecursiveRuleBase(RuleBase):
    def __init__(self, module):
        super(RecursiveRuleBase, self).__init__(module)
        self._re = re.compile(r'^{module}$|^{module}\.'.format(module=self._module))

    def _match(self, module):
        return re.match(self._re, module)


class IncludeRule(IncludeRuleBase, ExactRuleBase):
    pass


class ExcludeRule(ExcludeRuleBase, ExactRuleBase):
    pass


class RecursiveIncludeRule(IncludeRuleBase, RecursiveRuleBase):
    pass


class RecursiveExcludeRule(ExcludeRuleBase, RecursiveRuleBase):
    pass
