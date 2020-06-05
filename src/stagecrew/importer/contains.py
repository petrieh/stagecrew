import abc
from collections import namedtuple
import six
from tribool import Tribool

__copyright__ = 'Copyright (C) 2020, Nokia'


@six.add_metaclass(abc.ABCMeta)
class ContainsBase(object):
    """Base functor for TriboolSet contains_as_tribool implementation.
    """
    @abc.abstractmethod
    def __call__(self, obj):
        """Return Tribool object for *obj*.
        """


class OperatorContains(namedtuple('OperatorContains', ['oper', 'a', 'b']), ContainsBase):
    """Functor implementing contains_as_tribool for combined TriboolSet defined
    by operator *oper* and TriboolSet operands *a* and *b*.

    Arguments follow PN (Polish notation) order.

    Args:
        oper(callable): Set operation operator
        a(TriboolSet): left operand
        b(TriboolSet): right operand
    """
    def __call__(self, obj):
        return self.oper(self.a.contains_as_tribool(obj),
                         self.b.contains_as_tribool(obj))

    @classmethod
    def create_factory(cls, oper):
        def factory(a, b):
            return cls(oper=oper, a=a, b=b)

        return factory


@six.add_metaclass(abc.ABCMeta)
class OperandsContainsBase(namedtuple('OperandsContainsBase', ['a', 'b']),
                           ContainsBase):
    """TriboolSet contains functor base for TriboolSet operands *a* and *b*.
    """


class LazyLeftAndContains(OperandsContainsBase):
    """Lazy intersection (and) contains. Right operand is evaluated only if needed.
    """
    def __call__(self, obj):
        a = self.a.contains_as_tribool(obj)
        return a if a is Tribool(False) else a & self.b.contains_as_tribool(obj)


class DeterminedBElseAContains(OperandsContainsBase):
    def __call__(self, obj):
        b = self.b.contains_as_tribool(obj)
        return self.a.contains_as_tribool(obj) if b is Tribool() else b
