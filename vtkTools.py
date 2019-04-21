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

    pyevtk.hl.unstructuredGridToVTK(path,
                                    mesh._nodes[0,:],
                                    mesh._nodes[1,:],
                                    mesh._nodes[2,:], 
                                    vtk_connectivity,
                                    vtk_offsets[1:],
                                    vtk_celltypes)
    """
        Export unstructured grid and associated data.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: 1D arrays with coordinates of the vertices of cells. It is assumed that each element
                     has diffent number of vertices.
            connectivity: 1D array that defines the vertices associated to each element. 
                          Together with offset define the connectivity or topology of the grid. 
                          It is assumed that vertices in an element are listed consecutively.
            offsets: 1D array with the index of the last vertex of each element in the connectivity array.
                     It should have length nelem, where nelem is the number of cells or elements in the grid.
            cell_types: 1D array with an integer that defines the cell type of each element in the grid.
                        It should have size nelem. This should be assigned from evtk.vtk.VtkXXXX.tid, where XXXX represent
                        the type of cell. Please check the VTK file format specification for allowed cell types.                       
            cellData: Dictionary with variables associated to each line.
                      Keys should be the names of the variable stored in each array.
                      All arrays must have the same number of elements.        
            pointData: Dictionary with variables associated to each vertex.
                       Keys should be the names of the variable stored in each array.
                       All arrays must have the same number of elements.

        RETURNS:
            Full path to saved file.

    """