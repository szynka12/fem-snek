"""
.. module:: elements
   :synopsis: All functions and element operations are defined here
.. moduleauthor:: Wojciech Sadowski <github.com/szynka12>
"""

###################################################################
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

from numpy import zeros, int64, ndarray


class ConnectivityList:
    """
    Base class for defining connectivity list of certain element type.
    """
    __slots__ = (
                '_tags'
                )

    _dimension = 1  # element dimension
    _nNodes = 1     # number of nodes per element
    _type = 0       # element type

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
        Get node tags of nodes creating chosen element in the list.

        :param idx: element index (from 0 to number of elements - 1)
        :return: Array with node tags
        """
        return self._tags[:, idx]

    def __setitem__(self, idx: int, connectivity: ndarray) -> None:
        """
        Set node tags of nodes creating chosen element in the list.

        :param idx: element index (from 0 to number of elements - 1)
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


class ListLine1(ConnectivityList):
    """
    Class defining connectivity for first order line element.

    Private properties:


    * dimension = 1
    * nNodes = 2
    * type = 1

    Derived from :class:`femsnek.core.elements.ConnectivityList`
    """
    __slots__ = ()

    _dimension = 1
    _nNodes = 2
    _type = 1


class ListTri1(ConnectivityList):
    """
    Class defining connectivity for first order triangular element.

    Private properties:

    * dimension = 2
    * nNodes = 3
    * type = 2

    Derived from :class:`femsnek.core.elements.ConnectivityList`
    """
    __slots__ = ()

    _dimension = 2
    _nNodes = 3
    _type = 2


class ListQuad1(ConnectivityList):
    """
    Class defining connectivity for first order quadrilateral element.

    Private properties:

    * dimension = 2
    * nNodes = 4
    * type = 3

    Derived from :class:`femsnek.core.elements.ConnectivityList`
    """
    __slots__ = ()

    _dimension = 2
    _nNodes = 4
    _type = 3
