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
   :synopsis: Provides elements descriptions.
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""
import femsnek.core.quadratures as quadrature
from numpy import ndarray, array, tile


class Element:
    """
    Base class for defining elements.

    Attributes:

        -`_order: int` - order of element
        -`_q: femsnek.core.quadratures.QuadratureBase` - quadrature static class
    """
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



