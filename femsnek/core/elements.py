###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

from numpy import array, zeros, int64

class ConnectivityList:
    __slots__ = (
        '_tags'
    )
    
    _dimension = 1
    _nNodes = 1
    _type = 0
    
    def __init__(self, nElem):
        self._tags = zeros((self._nNodes,nElem), dtype=int64)

        
    def __getitem__(self, idx): 
        return self._tags[:,idx]
    
    def __setitem__(self, idx, connectivity): 
        self._tags[:,idx] = connectivity
    
    def dim(self): return self._dimension

    def n_elements(self): return self._tags.shape[1]
    def n_nodes(self): return self._nNodes
    def el_type(self): return self._type
    
class ListLine1(ConnectivityList):
    __slots__ = ()
    
    _dimension = 1
    _nNodes = 2
    _type = 1
     
        
class ListTri1(ConnectivityList):
    __slots__ = ()
    
    _dimension = 2
    _nNodes = 3
    _type = 2
    
class ListQuad1(ConnectivityList):
    __slots__ = ()
    
    _dimension = 2
    _nNodes = 4
    _type = 3
    

