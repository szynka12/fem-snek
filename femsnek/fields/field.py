"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: field
   :synopsis: Module providing basic concepts for all field classes
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

from abc import ABC, abstractmethod
from femsnek.fio.error import FieldOperationError
from femsnek.mesh import feMesh


class FieldBase(ABC):
    __slots__ = ('_name',
                 '_region',
                 '_order',
                 '_ref_feMesh')

    def __init__(self):
        self._name = None
        self._region = (None, None)
        self._order = None
        self._ref_feMesh = None

    @property
    @abstractmethod
    def components(self):
        """
        Decomposes field into scalar fields
        """
        pass

    def name(self) -> str:
        """
        Returns name of the field.

        :return: name of the field
        """
        return self._name

    def mesh(self) -> feMesh.Mesh:
        """
        Returns mesh on which field is defined.

        :return: mesh
        """
        return self._ref_feMesh[self._region]

    def region(self) -> (str, int):
        """
        Returns region tuple.

        :return: region tuple
        """
        return self._region

    def order(self) -> int:
        return self._order

    def region_check(self, field) -> None:
        """
        Raises FieldOperationError() when fields have different regions

        :param field: second operand field
        :type field: FieldBase
        """
        if field.region() != (None, None) and field.region() != self._region:
            raise FieldOperationError('Cant operate on ' + str(type(self)) + ' and ' + str(type(field)) + '!')

    def order_check(self, field) -> None:
        """
        Raises FieldOperationError() when fields have different orders

        :param field: second operand field
        :type field: FieldBase
        """
        if self._order != field.order():
            raise FieldOperationError('Cant operate on ' + str(type(self)) + ' and ' + str(type(field)) + '!')


class UniformField(FieldBase):
    @property
    @abstractmethod
    def expand(self, mesh: feMesh):
        """
        Expands uniform field onto the whole mesh
        """

