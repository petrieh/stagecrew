import abc
from collections import namedtuple
import six
from tribool import Tribool

__copyright__ = 'Copyright (C) 2020, Nokia'


class DefaultSetOperation(namedtuple('DefaultSetOperation', ['oper', 'a', 'b'])):
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
    def get_factory(cls, oper):
        def factory(a, b):
            return cls(oper=oper, a=a, b=b)
        return factory


@six.add_metaclass(abc.ABCMeta)
class SetOperationBase(namedtuple('SetOperationBase', ['a', 'b'])):
    """TriboolSet operation functor base class.  The implementation must define
    new combined TriboolSet membership function *contains_as_tribool* as
    __call__ implementation.
    """
    @abc.abstractmethod
    def __call__(self, obj):
        """Implement TriboolSet *contains_as_tribool* using TriboolSet operands
        *_a* and *_b*.
        """


class AndOperation(SetOperationBase):
    def __call__(self, obj):
        b = self.b.contains_as_tribool(obj)
        return b if b is Tribool(False) else self.a.contains_as_tribool(obj) & b


class DeterminedBElseA(SetOperationBase):
    def __call__(self, obj):
        b = self.b.contains_as_tribool(obj)
        return self.a.contains_as_tribool(obj) if b is Tribool() else b


def get_set_operation_factory(oper):
    return (
        oper
        if isinstance(oper, six.class_types) and issubclass(oper, SetOperationBase) else
        DefaultSetOperation.get_factory(oper))
