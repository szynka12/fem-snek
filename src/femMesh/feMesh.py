###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################


#TODO Refactor of some import elements (same code in both places)
#TODO Documentation
#TODO Move gmsh import fun
#TODO IO package

## Imports ---------------------------------------------------------------------
from numpy import array

## Class definition ------------------------------------------------------------

# main mesh class
class FeMesh:
    __slots__ = (
        '_info',
        '_nodes',
        '_internalMesh',
        '_boundaryMesh'
    )
    
    def __init__(self,info, nodes, element_lists, physical_ids):
        self._info = info
        self._nodes = nodes
        self._internalMesh = []
        self._boundaryMesh = []
        
        maxDim = max([i.dim() for i in element_lists])
        
        internalIndex = \
            [i for (i, list) in enumerate(element_lists) 
             if list.dim() == maxDim]
        
        boundaryIndex = \
            [i for (i, list) in enumerate(element_lists)
             if list.dim() < maxDim]
        
        # extract boudary data    
        b_ids = [ physical_ids[i] for i in boundaryIndex]
        b_lists = [ element_lists[i] for i in boundaryIndex]
        
        # sort boundary data
        while b_ids:
            same_ids = [i for (i, id) in enumerate(b_ids) if id == b_ids[0]]
            
            self._boundaryMesh.append(
                                Mesh(self._nodes.view(),
                                [b_lists[i] for i in same_ids],
                                b_ids[0]   
                                )
                                )
            
            b_lists = [b_lists[i] for i in range(len(b_lists)) 
                       if i not in same_ids]
            
            b_ids = list(filter(lambda a: a != b_ids[0], b_ids))
        
        # extract internal data
        i_ids = [ physical_ids[i] for i in internalIndex]
        i_lists = [ element_lists[i] for i in internalIndex]
        
        # sort internal data
        while i_ids:
            same_ids = [i for (i, id) in enumerate(i_ids) if id == i_ids[0]]
            self._internalMesh.append(
                                Mesh(self._nodes.view(),
                                [i_lists[i] for i in same_ids],
                                i_ids[0]   
                                )
                                )
            
            
            i_ids = list(filter(lambda a: a != i_ids[0], i_ids))
        
        self._internalMesh = tuple(self._internalMesh)
        self._boundaryMesh = tuple(self._boundaryMesh)
        
    def n_nodes(self): return self._nodes.shape[0]
     
        
class Mesh:
    __slots__: (
        '_connectivityLists',
        '_id',
        '_ref_nodes'
    )
    
    def __init__(self, ref_nodes,lists, id):
        self._ref_nodes = ref_nodes
        self._connectivityLists = tuple(lists)
        self._id = id    
    
        
    

           
## Helper functions ------------------------------------------------------------




