import six
import abc


class Rules(object):
    def __init__(self):
        self._rules = []

    def add(self, rule):
        self._rules.append(rule)

    def is_included(self, module):
        is_included = NotApplicable
        for is_included in self._is_includes(module):
            pass

        return is_included

    def _is_includes(self, module):
        for r in self._rules:
            is_included = r.is_included(module)
            if is_included is not NotApplicable:
                yield is_included


@six.add_metaclass(abc.ABCMeta)
class RuleBase(object):
    def __init__(self, module):
        self._module = module

    @abc.abstractmethod
    def is_included(self, module):
        """Return:

          - True, if module is included according to this rule.
          - False, if module is not included according to this rule.
          - NotApplicable, if this rule is not applicable for the module.
        """


class RecursiveExclude(object):
    pass


class RecursiveInclude(object):
    pass


class Include(object):
    pass


class Exclude(object):
    pass


class NotApplicable(object):
    pass
