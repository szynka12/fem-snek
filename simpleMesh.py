import numpy as np

import gmshTools as gmsh
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class Mesh:
    def __init__(self):
        self._info = {}                 #information about mesh
        self._nodes = np.empty((3,0))   #node list (type vector)
        self._domainElements = []               #elements inside domain (type element)
        self._boundaryElements = []             #elements on boundary
        self._problemDim = 3            #dimension of the problem
        self._meshDim = 3               #dimension of mesh   
        
        
    def Import_gmsh(self, filename):
        '''
        Importer of ascii .msh meshes.
        
        Imports meshes generated in Gmsh software. 
        Supported version: MSH 4.1 
        Supported elements:
            - Line (2 node)
            - Triangle (3 node)
            - Quadrangle (4 node)
        '''
        #TODO implemenation that reads only known sections
        #TODO   and can omit any unwanted data 
        
        with open(filename) as file:
            
            # get mesh format
            file.readline()
            gmsh.read_MeshFormat(file, self._info)
            
            # get info about mesh entities
            file.readline()
            gmsh.read_Entities(file, self._info)
            
            # assert if mesh has volume (be aware mesh with dim = 2 can
            # be 3 dimensional e.g. boundary mesh or mesh for shell elements)
            if (self._info['#volumes'] == 0):
                self._meshDim = 2
            
            # read nodes
            file.readline()
            self._nodes, node_tags = gmsh.read_Nodes(file)
            
            # assert if problem is planar 
            if (max(self._nodes[2,:]) == min(self._nodes[2,:])):
                self._problemDim = 2
            
            # read elements
            file.readline()
            gmsh.read_Elements(file, self._domainElements, self._boundaryElements, self._meshDim)
            
            # repair mesh (gmsh is retarted and can omit a node tag, we fight
            # back)
            skipped_tags = []
            if (gmsh.check_for_renumeration(node_tags, skipped_tags)):
                gmsh.renumerate_elements(self._domainElements, skipped_tags)
                gmsh.renumerate_elements(self._boundaryElements, skipped_tags)
            
    def Show(self):
        ax = plt.subplots()[1]
        patches = []
        for el in self._domain:
            patches.append(
                Polygon(np.transpose(self._nodes[0:2, el._connectivity ]), True)
            )
        p = PatchCollection(patches)

        colors = 100*np.random.rand(len(patches))
        p.set_array(np.array(colors))

        ax.add_collection(p)

        plt.show()
    
    
        
        
    
        
            
    
        
    
    
    
    
        
        
        
        
    
        
