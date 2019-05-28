"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: abstract
   :synopsis: Provides basic abstract classes for all differential operators
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

from abc import ABC, abstractmethod
from operator import add, sub
from femsnek.fio.error import FieldOperationError


class OperatorBase():
    __slots__ = ('_lhs_next',
                 '_rhs_next',
                 '_operation_next')

    def __init__(self):
        self._lhs_next = None
        self._rhs_next = None
        self._operation_next = None

    @abstractmethod
    def assemble(self):
        pass

    @abstractmethod
    def matrix(self):
        pass

    def propagate_lhs(self, operator, operation):
        if self._lhs_next is not None:
            self._lhs_next.propagate_lhs(operator, operation)
        else:
            self._lhs_next = operator
            self._operation_next = operation

    def propagate_rhs(self, operator, operation):
        if self._rhs_next is not None:
            self._rhs_next.propagate_rhs(operator, operation)
        else:
            self._rhs_next = operator
            self._operation_next = operation

    def check_operator(self, operator):
        if not isinstance(operator, self.__class__):
            raise FieldOperationError('Cant add or subtract ' + str(self.__class__) + ' and ' + str(type(operator)))


class LHSBase(OperatorBase):
    __slots__ = '_operation_next'

    def __init__(self):
        super().__init__()

    def __add__(self, other):
        self.check_operator(other)
        self.propagate_lhs(other, add)
        return self

    def __sub__(self, other):
        self.check_operator(other)
        self.propagate_lhs(other, sub)
        return self

    def __eq__(self, other):
        self._rhs_next = other
        return self

    def assemble(self):
        if self._lhs_next is not None and self._rhs_next is not None:
            return (self._operation_next(self.matrix(), self._lhs_next.assemble()),
                    self._rhs_next.assemble())
        elif self._lhs_next is not None and self._rhs_next is None:
            return self._operation_next(self.matrix(), self._lhs_next.assemble())
        else:
            return self.matrix()


class RHSBase(OperatorBase):
    __slots__ = ()

    def __init__(self):
        super().__init__()

    def __add__(self, other):
        self.check_operator(other)
        self.propagate_rhs(other, add)
        return self

    def __sub__(self, other):
        self.check_operator(other)
        self.propagate_rhs(other, sub)
        return self

    def assemble(self):
        if self._rhs_next is not None:
            return self._operation_next(self.matrix(), self._rhs_next.assemble())
        else:
            return self.matrix()


class DummyLHS(LHSBase):
    def matrix(self):
        return 1


class DummyRHS(RHSBase):
    def matrix(self):
        return 0.5


a = (DummyLHS() + DummyLHS() - DummyLHS() == DummyRHS() + DummyRHS())

b = a.assemble()

print(b)


