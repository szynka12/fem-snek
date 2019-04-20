class FiniteElement:
    def __init__(self):
        self._connectivity = []


class Line1:
    def __init__(self, connectivity, phys_id):
        self._d = 1
        self._connectivity= [i - 1 for i in connectivity]
        self._id = phys_id
        
class Quad1:
    def __init__(self, connectivity, phys_id):
        self._d = 2
        self._connectivity= [i - 1 for i in connectivity]
        self._id = phys_id
        
class Tri1:
    def __init__(self, connectivity, phys_id):
        self._d = 2
        self._connectivity= [i - 1 for i in connectivity]
        self._id = phys_id

class Point:
    def __init__(self, connectivity, phys_id):
        self._d = 0
        
