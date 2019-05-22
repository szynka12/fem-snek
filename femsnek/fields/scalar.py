"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: scalar
   :synopsis: Provides scalar field operation capabilities
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

from numpy import ndarray
from femsnek.fio.stream import WritableBase
from femsnek.fields import ScalarFieldEnumerator
from femsnek.fio.error import FieldOperationError
from femsnek.mesh.feMesh import FeMesh
from femsnek.fields.field import FieldBase


class Scalar(FieldBase, WritableBase):
    """
    Class describing a single scalar e.g. 2, pi.

    Attributes:

        - `_value: float` - value held by scalar object
        - `_name: str` - name of the scalar, generated automatically
    """
    __slots__ = (
            '_value',
            '_name'
            )

    def __init__(self, value: float):
        """
        Creates instance of Scalar object

        :param value: value held by scalar object
        """
        try:
            self._value = float(value)
        except TypeError:
            print('Scalar input must be a single value')
        self._name = str(self._value)

    # Helpers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    def get_name(self):
        return self._name

    def components(self):
        return self

    def __add__(self, rhs):
        """
        Addition of two Scalar objects or Scalar and ScalarField

        :param rhs: Scalar or ScalarField
        :return: Scalar or ScalarField
        """
        if isinstance(rhs, Scalar):
            return Scalar(self._value + rhs._value)
        elif isinstance(rhs, ScalarField):
            return ScalarField(self._value + rhs._value, rhs._region)
        else:
            raise TypeError('Can\'t add scalar and' + str(type(rhs)))

    def __sub__(self, rhs):
        """
        Subtraction of two Scalar objects or Scalar and ScalarField

        :param rhs: Scalar or ScalarField
        :return: Scalar or ScalarField
        """
        if isinstance(rhs, Scalar):
            return Scalar(self._value - rhs._value)
        elif isinstance(rhs, ScalarField):
            return ScalarField(self._value - rhs._value, rhs._region)
        else:
            raise TypeError('Can\'t subtract scalar and' + str(type(rhs)))

    def __mul__(self, rhs):
        """
        Multiplication of two Scalar objects or Scalar and ScalarField

        :param rhs: Scalar or ScalarField
        :return: Scalar or ScalarField
        """
        if isinstance(rhs, Scalar):
            return Scalar(self._value * rhs._value)
        elif isinstance(rhs, ScalarField):
            return ScalarField(self._value * rhs._value, rhs._region)
        else:
            raise TypeError('Can\'t multiply scalar and' + str(type(rhs)))

    def __truediv__(self, rhs):
        """
        Division of two Scalar objects or Scalar and ScalarField

        :param rhs: Scalar or ScalarField
        :return: Scalar or ScalarField
        """
        if isinstance(rhs, Scalar):
            return Scalar(self._value / rhs._value)
        elif isinstance(rhs, ScalarField):
            return ScalarField(self._value / rhs._value, rhs._region)
        else:
            raise TypeError('Can\'t divide scalar by' + str(type(rhs)))

    def __repr__(self):
        """
        Returns string representation of scalar object e.g: `'Scalar(2.0)'`

        :return: String representation of scalar object
        """
        return 'Scalar(' + str(self._value) + ')'


class ScalarField(FieldBase, WritableBase):
    __slots__ = (
            '_value',
            '_region',
            '_name'
            )

    def __init__(self, value: ndarray, region: tuple, name: str = False):
        """
        Creates instance of ScalarField class
        :rtype: ScalarField
        """
        self._value = value
        self._region = region
        if name:
            try:
                self._name = str(name)
            except TypeError('Field name must be a string'):
                pass
        else:
            self._name = 'ScalarF' + str(
                    ScalarFieldEnumerator.getInstance().inc())

    def get_name(self):
        return self._name

    def components(self):
        return self

    def region_check(self, scalar_field) -> None:
        """
        Raises FieldOperationError() when fields have different regions

        :type scalar_field: ScalarField
        """
        if isinstance(scalar_field, ScalarField) and self._region != scalar_field._region:
            raise FieldOperationError('Cant operate on ' + str(type(self)) +
                                      ' and ' + str(type(scalar_field)) + '!')

    def __add__(self, rhs):
        if isinstance(rhs, Scalar):
            return ScalarField(self._value + rhs._value, self._region)
        elif isinstance(rhs, ScalarField):
            self.region_check(rhs)
            return ScalarField(self._value + rhs._value, self._region)
        else:
            raise TypeError('Can\'t add ScalarField and' + str(type(rhs)))

    def __repr__(self):
        """
        Returns string representation of ScalarField object

        :return: String representation of ScalarField object
        """
        raise NotImplemented

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Scalar shortcuts:
zero = Scalar(0.0)
one = Scalar(1.0)
pi = Scalar(3.141592653589793238462643383279502884197169399375105820974944592)
e = Scalar(2.718281828459045235360287471352662497757247093699959574966967627)


# Helper classes ---------------------------------
class InternalScalarField(ScalarField):
    """
    Class defining scalar fields on internal parts of finite element mesh.
    """
    def __init__(self, mesh: FeMesh, value: ndarray, index: int, name: str = False):
        """
        Creates instance of InternalScalarField object.

        :param mesh: Finite element mesh
        :param value: Nodal values of the field
        :param index: Index of internal mesh region
        :param name: Name of the field
        :returns A scalar Field with nodal values specified by value:
        :rtype: ScalarField
        """
        if mesh._internalMesh[index]._node_tags.shape[0] != value.shape[0]:
            raise FieldOperationError('Invalid number of field values')
        super().__init__(value, ('i', index), name)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class BoundaryScalarField(ScalarField):
    """
    Class defining scalar fields on boundary parts of finite element mesh.
    """

    def __init__(self, mesh: FeMesh, value: ndarray, index: int, name: str = False):
        """
        Creates instance of BoundaryScalarField object.

        :param mesh: Finite element mesh
        :param value: Nodal values of the field
        :param index: Index of boundary mesh region
        :param name: Name of the field
        :returns A scalar Field with nodal values specified by value:
        :rtype: ScalarField
        """
        if mesh._boundaryMesh[index]._node_tags.shape[0] != value.shape[0]:
            raise FieldOperationError('Invalid number of field values')
        super().__init__(value, ('b', index), name)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
