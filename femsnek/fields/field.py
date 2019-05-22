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


class FieldBase(ABC):
    __slots__ = ('_name',
                 '_region',
                 '_order')

    def __init__(self):
        self._name = None
        self._region = (None, None)
        self._order = None

    @property
    @abstractmethod
    def components(self):
        pass

    def name(self) -> str:
        return self._name

    def region(self) -> (str, int):
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


from femsnek.mesh.feMesh import FeMesh
from numpy import ndarray
from femsnek.fio.stream import WritableBase


class ScalarField(FieldBase, WritableBase):
    __slots__ = '_value'
    _order = 1

    def __init__(self, name: str, value: ndarray, region: (str, int)):
        """
        Create instance of ScalarField class

        :param name: name of the scalar field
        :param value: numpy array with nodal values
        :param region: tuple describing region of the mesh
        """

        # fast field creation (no checks)
        self._region = region

        self._value = value
        self._name = name

    @classmethod
    def from_mesh(cls, name: str, value: ndarray, mesh: FeMesh, region_name: str):
        """
        Create instance of ScalarField class

        :param name: name of the scalar field
        :param value: numpy array with nodal values
        :param mesh: finite element mesh
        :param region_name: name of the chosen mesh region
        """
        if mesh is None:
            raise FieldOperationError('Mesh must be provided for safe type of field creation.')
        if region_name is None:
            region = ('i', 1)
        else:
            region = mesh.name2region(region_name)

        return cls(name, value, region)

    def components(self):
        return self

    def nodal(self) -> ndarray:
        """
        Returns nodal values of the field.

        :return: numpy array with nodal values of the field.
        """
        return self._value

    def __repr__(self) -> str:
        return 'ScalarField(\n \'' + self._name + '\',\n' + repr(self._value) + ',\n' + str(self._region) + '\n)'

    def __add__(self, rhs):
        self.region_check(rhs)
        self.order_check(rhs)
        return ScalarField(self._name + '+' + rhs.name(), self._value + rhs.nodal(), self._region)


class Scalar(ScalarField, WritableBase):
    __slots__ = '_value'
    _region = (None, None)
    
    def __init__(self, value: float, name: str = None):
        """
        Creates instance of Scalar object

        :param value: value held by scalar object
        :param name: (optional) name of the scalar
        """
        self._value = value
        if name is not None:
            self._name = name
        else:
            self._name = str(self._value)

    def __repr__(self) -> str:
        return 'Scalar(' + repr(self._value) + ' \'' + self._name + '\')'

    def __add__(self, rhs):
        self.order_check(rhs)
        if isinstance(rhs, Scalar):
            return Scalar(self._value + rhs.nodal(), self._name + '+' + rhs.name())
        elif isinstance(rhs, ScalarField):
            return ScalarField(self._name + '+' + rhs.name(), self._value + rhs.nodal(), self._region)


# Scalar shortcuts:
zero = Scalar(0.0, 'zero')
one = Scalar(1.0, 'one')
pi = Scalar(3.1415926535, 'pi')
e = Scalar(2.71828182845, 'e')

from numpy import array


a = array([1, 2, 3, 4])
S = ScalarField('dupa', a, ('a', 3))
print(S.nodal() == eval(repr(S)).nodal())

S2 = Scalar(1, 'eee')

print((S2 + S).nodal())
