"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: elements
   :synopsis: All functions and element operations are defined here
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

from numpy import zeros, int64, ndarray, array, tile
import femsnek.core.quadratures as quadrature

# Element signatures
T_Line1 = 1
T_Tri1 = 2
T_Quad1 = 3


class Element:
    __slots__ = ()

    order = None
    q = None

    def __init__(self):
        pass

    @classmethod
    def quadrature(cls):
        return cls.q.by_order(cls.order)


class Tri1(Element):
    order = 1
    q = quadrature.QTri

    @staticmethod
    def N(points: ndarray) -> ndarray:
        return array([1 - points[0, :] - points[1, :],
                      points[0, :],
                      points[1, :]])

    @staticmethod
    def gradN(points: ndarray) -> (ndarray, ndarray):

        n_d_ksi = array([[-1], [1], [0]])
        n_d_eta = array([[-1], [0], [1]])

        if len(points.shape) == 1:
            return n_d_ksi, n_d_eta
        else:
            return tile(n_d_ksi, (1, points.shape[1])), tile(n_d_eta, (1, points.shape[1]))

    @staticmethod
    def J(points: ndarray):
        return array(
                [[points[0, 1] - points[0, 0], points[1, 1] - points[1, 0]],
                 [points[0, 2] - points[0, 0], points[1, 2] - points[1, 0]]]
                )

    @staticmethod
    def detJ(points: ndarray):
        j = array(
                [[points[0, 1] - points[0, 0], points[1, 1] - points[1, 0]],
                 [points[0, 2] - points[0, 0], points[1, 2] - points[1, 0]]]
                )
        return j[0, 0] * j[1, 1] - j[0, 1] * j[1, 0]




class ConnectivityList:
    """
    Base class for defining connectivity list of certain element type.

    Attributes:

        -`_dimension: int` - dimension of element type
        -`_nNodes: int` - number of nodes per one element
        -`_type: int` - element type signature defined in `__init__.py of this package`
        -`_tags: nparray` - tags of nodes that span elements, has shape equal `(_nNodes, nElem)`
    """
    __slots__ = (
            '_tags'
    )

    _dimension = 1  # element dimension
    _nNodes = 1  # number of nodes per element
    _type = 0  # element type
    _calculator = None

    def __init__(self, n_elem: int):
        """
        Creates instance of ConncetivityList object.

        :param n_elem: number of elements
        :returns: ConnectivityList object
        :rtype: ConnectivityList
        """
        self._tags = zeros((self._nNodes, n_elem), dtype=int64)

    def __getitem__(self, idx: int) -> ndarray:
        """
        Get node tags of nodes spanning chosen element in the list.

        :param idx: element index (from 0 to number of elements)
        :return: Array with node tags
        """
        return self._tags[:, idx]

    def __setitem__(self, idx: int, connectivity: ndarray) -> None:
        """
        Set node tags of nodes creating chosen element in the list.

        :param idx: element index (from 0 to number of elements)
        :param connectivity: Array with node tags
        """

        self._tags[:, idx] = connectivity

    def dim(self) -> int:
        """
        Returns physical dimension of element type.

        :returns: element dimension.
        :rtype: int
        
        An example would be 3 for tetrahedral element or 2 for quad.
        """
        return self._dimension

    def n_elements(self) -> int:
        """
        Get number of elements in connectivity list.

        :return: number of elements in connectivity list
        """
        return self._tags.shape[1]

    def n_nodes(self) -> int:
        """
        Get number of nodes per element.

        :return: number of nodes per element
        """
        return self._nNodes

    def el_type(self) -> int:
        """
        Get number of element type stored in the list.

        :return: element type number
        """
        return self._type

    def fem_calculator(self):
        return self._calculator


class ListLine1(ConnectivityList):
    """
    Class defining connectivity for first order line element.

    Attributes:

    * dimension = 1
    * nNodes = 2
    * type = 1

    Derived from :class:`femsnek.core.elements.ConnectivityList`
    """
    __slots__ = ()

    _dimension = 1
    _nNodes = 2
    _type = T_Line1


class ListTri1(ConnectivityList):
    """
    Class defining connectivity for first order triangular element.

    Attributes:

    * dimension = 2
    * nNodes = 3
    * type = 2

    Derived from :class:`femsnek.core.elements.ConnectivityList`
    """
    __slots__ = ()

    _dimension = 2
    _nNodes = 3
    _type = T_Tri1
    _calculator = Tri1


class ListQuad1(ConnectivityList):
    """
    Class defining connectivity for first order quadrilateral element.

    Attributes:

    * dimension = 2
    * nNodes = 4
    * type = 3

    Derived from :class:`femsnek.core.elements.ConnectivityList`
    """
    __slots__ = ()

    _dimension = 2
    _nNodes = 4
    _type = T_Quad1
