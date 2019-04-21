class FiniteElement:
    __slots__ = (
        '_d',
        '_connectivity',
        '_id'
    )
    def __init__(self):
        self._d = 0
        self._connectivity = []
        self._id = 0
    
    def get_n_nodes(self): return len(self._connectivity)


class Line1(FiniteElement):
    __slots__ = ()
    
    def __init__(self, connectivity, phys_id):
        self._d = 1
        self._connectivity = connectivity - 1
        self._id = phys_id
    
    def enum(self): return 1
       
class Quad1(FiniteElement):
    __slots__ = ()
    
    def __init__(self, connectivity, phys_id):
        self._d = 2
        self._connectivity= connectivity - 1
        self._id = phys_id
    
    def enum(self): return 2
 
class Tri1(FiniteElement):
    __slots__ = ()
    def __init__(self, connectivity, phys_id):
        self._d = 2
        self._connectivity= connectivity - 1
        self._id = phys_id
        
    def enum(self): return 3

class Point(FiniteElement):
    __slots__ = ()
    def __init__(self, connectivity, phys_id):
        self._d = 0
        
    def enum(self): return 0
        
