###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

from numpy import array

class QuadratureBase(object):
    __slots__ = ("points","weights")

    def __init__(self):
        pass


class GaussTriangle2D(QuadratureBase):

    __slots__ = ("points", "weights", "npoints")

    def __init__(self, order=2):
        
        if order == 1:
            self.points = array([[1.0/3.0, 1.0/3.0, 1.0/3.0]])
            self.weights = array([1.0])
            self.npoints = 1

        elif order == 2:
            self.points = array([[0.5, 0.5, 0.0],
                                [0.5, 0.0, 0.5],
                                [0.0, 0.5, 0.5]])
            self.weights = array([1.0/3.0, 1.0/3.0, 1.0/3.0])
            self.npoints = 3

        elif order == 3:
            self.points = array([[1.0/3.0, 1.0/3.0, 1.0/3.0],
                                [0.6, 0.2, 0.2],
                                [0.2, 0.6, 0.2],
                                [0.2, 0.2, 0.6]])
            self.weights = array([-27.0/48.0, 25.0/48.0, 25.0/48.0, 25.0/48.0])
            self.npoints = 4
