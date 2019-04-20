from math import sqrt

class Vector:
    def __init__(self, x, y, z=0):
        self._x = x
        self._y = y
        self._z = z
    
    def norm(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)
    