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
from femsnek.fio.error import FieldOperationError


class OperatorBase(ABC):
    __slots__ = '_value'

    def __init__(self):
        pass

    def region(self):
        return self._region

    def __add__(self, operator):
        self.check_operator(operator)
        self._value += operator._value
        return self

    def __sub__(self, operator):
        self.check_operator(operator)
        self._value -= operator._value
        return self

    def __call__(self):
        return self._value

    @abstractmethod
    def check_operator(self, operator):
        pass


class LHSBase(OperatorBase):
    __slots__ = ()

    def __init__(self):
        pass

    def check_operator(self, operator):
        if self._region != operator.region():
            raise FieldOperationError('Cant add or subtract operators from different regions.')
        if not isinstance(LHSBase, operator):
            raise FieldOperationError('Cant add or subtract operators and ' + str(type(operator)))


class RHSBase(OperatorBase):
    __slots__ = ()

    def check_operator(self, operator):
        if self._region != operator.region():
            raise FieldOperationError('Cant add or subtract operators from different regions.')
        if not isinstance(RHSBase, operator):
            raise FieldOperationError('Cant add or subtract operators and ' + str(type(operator)))

