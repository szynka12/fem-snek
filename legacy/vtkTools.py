from pyevtk.vtk import *
from pyevtk.hl import *
from pyevtk.hl import _addDataToFile
from pyevtk.hl import _appendDataToFile
from pyevtk.evtk import *
from pyevtk.xml import *

import pyevtk



import numpy as np
from numpy import int32

pyevtk.vtk.VtkLine

vtkTypes = {
    1: pyevtk.vtk.VtkLine,
    2: pyevtk.vtk.VtkQuad,
    3: pyevtk.vtk.VtkTriangle,
    0: None
}

def export(path,mesh):
    n = mesh.get_n_elements()
    vtk_connectivity = np.empty(0, dtype=int32)
    vtk_offsets = np.empty(n+1, dtype=int32)
    vtk_offsets[0] = 0
    vtk_celltypes = np.empty(n, dtype=int32)
    for i in range(n):
        el = mesh._domainElements[i]
        vtk_connectivity = np.append(vtk_connectivity, el._connectivity, axis = 0)
        vtk_offsets[i+1] = el.get_n_nodes() + vtk_offsets[i]
        vtk_celltypes[i] = vtkTypes[el.enum()].tid

    unstructuredGridToVTK(path,
                                    mesh._nodes[0,:],
                                    mesh._nodes[1,:],
                                    mesh._nodes[2,:], 
                                    vtk_connectivity,
                                    vtk_offsets[1:],
                                    vtk_celltypes)


