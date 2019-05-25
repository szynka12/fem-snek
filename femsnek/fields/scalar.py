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


from femsnek.fields.field import FieldBase, UniformField
from femsnek.mesh.feMesh import FeMesh
from numpy import ndarray
from femsnek.fio.stream import WritableBase
from femsnek.fio.error import FieldOperationError


class ScalarField(FieldBase, WritableBase):
    __slots__ = '_value'
    _order = 1

    def __init__(self, name: str, value: ndarray, mesh: FeMesh, region: (str, int) = (None, None)):
        """
        Create instance of ScalarField class

        :param name: name of the scalar field
        :param value: numpy array with nodal values
        :param mesh: finite element mesh
        :param region: tuple describing region of the mesh
        """

        if region == (None, None):
            region = ('i', 0)

        self._region = region
        self._ref_feMesh = mesh
        if value.shape[0] != mesh[region].n_nodes():
            raise FieldOperationError('Number of field values and mesh nodes not equal for specified mesh '
                                      'region!')
        else:
            self._value = value

        self._name = name

    @classmethod
    def by_region_name(cls, name: str, value: ndarray, mesh: FeMesh, region_name: str):
        """
        Create instance of ScalarField class (region by its physical name)

        :param name: name of the scalar field
        :param value: numpy array with nodal values
        :param mesh: finite element mesh
        :param region_name: name of the chosen mesh region
        """

        return cls(name, value, mesh, mesh(region_name))

    @classmethod
    def by_fun(cls, name: str, v_by_lambda, mesh: FeMesh, region: (str, int) = (None, None)):
        """
        Create instance of ScalarField class (values by lambda function)

        :param name: name of the scalar field
        :param v_by_lambda: lambda function with signature foo(x, y, z)
        :param mesh: finite element mesh
        :param region: tuple describing region of the mesh
        """

        if region == (None, None):
            region = ('i', 0)

        return cls(name,
                   v_by_lambda(mesh._nodes[0, mesh[region]._node_tags],
                               mesh._nodes[1, mesh[region]._node_tags],
                               mesh._nodes[2, mesh[region]._node_tags]),
                   mesh,
                   region)

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


class Scalar(UniformField, WritableBase):
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

    def expand(self, mesh: FeMesh, region):
        NotImplemented

    def components(self):
        return self

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
