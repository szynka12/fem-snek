from numpy import array
from femsnek.fio.error import CoreError


class QTri:
    def __init__(self, n: int):
        if n == 1:
            self.points = array([[1 / 3], [1 / 3]])
            self.weights = array([0.5])
        else:
            raise CoreError('No quadrature with ' + str(n) + ' points!')

    @classmethod
    def by_order(cls, order):
        if order >= 1:
            return cls(1)
        else:
            raise CoreError('No quadrature matches criteria')
