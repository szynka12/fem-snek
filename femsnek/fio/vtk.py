"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: vtk
   :synopsis: Module providing output to vtk file format
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

import pyevtk as evtk
from femsnek.mesh import feMesh
import numpy as np
import femsnek.fields as fields


# Data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Dictionary [<fem-snek element type>] -> <VTK Element type>
# fem-snek element type is obtainable from connectivityList object
vtkTypes = {
        1: evtk.vtk.VtkLine,
        3: evtk.vtk.VtkQuad,
        2: evtk.vtk.VtkTriangle,
        0: None
        }


def write(path: str, femesh: feMesh, field_list: list) -> None:
    """
    Exports mesh (and in the future) scalar/vector/tensor fields

    Mesh will be decomposed into internal regions and boundary regions based
    on their physical ids. Each region will be stored in different .vtu file
    (.vtk unstructured).

    Internal regions will be named :
        <path>.i.<region name>.vtu
    Boundary region:
        <path>.b.<region name>.vtu


       :param path: - path to file.
       :param femesh: - finite element mesh object
    """

    # export internal regions
    for mesh in femesh._internalMesh:

        # prepare tables for vtk (for description read help for: 
        # unstructuredGridToVTK)

        vtk_connectivity = np.empty(0, dtype=np.int32)
        vtk_offsets = np.empty(1, dtype=np.int32)
        vtk_offsets[0] = 0
        vtk_celltypes = np.empty(0, dtype=np.int8)

        for con_list in mesh._connectivityLists:
            n_el = con_list.n_elements()
            el_nodes = con_list.n_nodes()
            vtk_connectivity = np.append(vtk_connectivity,
                                         con_list._tags.flatten('f'), axis=0)
            vtk_offsets = np.append(vtk_offsets,
                                    [el_nodes * (i + 1) + vtk_offsets[-1]
                                     for i in range(n_el)],
                                    axis=0)
            vtk_celltypes = np.append(vtk_celltypes,
                                      vtkTypes[con_list.el_type()].tid *
                                      np.ones((n_el,), dtype=np.int8),
                                      axis=0)

        filename = path + '.i.' + str(mesh._id)

        evtk.hl.unstructuredGridToVTK(filename,
                                      femesh._nodes[0, :],
                                      femesh._nodes[1, :],
                                      femesh._nodes[2, :],
                                      vtk_connectivity,
                                      vtk_offsets[1:],
                                      vtk_celltypes)

    # export boundary regions    
    for mesh in femesh._boundaryMesh:

        vtk_connectivity = np.empty(0, dtype=np.int32)
        vtk_offsets = np.empty(1, dtype=np.int32)
        vtk_offsets[0] = 0
        vtk_celltypes = np.empty(0, dtype=np.int8)

        for con_list in mesh._connectivityLists:
            n_el = con_list.n_elements()
            el_nodes = con_list.n_nodes()
            vtk_connectivity = np.append(vtk_connectivity,
                                         con_list._tags.flatten('f'), axis=0)
            vtk_offsets = np.append(vtk_offsets,
                                    [el_nodes * (i + 1) + vtk_offsets[-1]
                                     for i in range(n_el)],
                                    axis=0)
            vtk_celltypes = np.append(vtk_celltypes,
                                      vtkTypes[con_list.el_type()].tid *
                                      np.ones((n_el,), dtype=np.int8),
                                      axis=0)

        filename = path + '.b.' + str(mesh._id)

        evtk.hl.unstructuredGridToVTK(filename,
                                      femesh._nodes[0, :],
                                      femesh._nodes[1, :],
                                      femesh._nodes[2, :],
                                      vtk_connectivity,
                                      vtk_offsets[1:],
                                      vtk_celltypes)


def convert_field_list(field_list: list, point_fields=None) -> dict:
    if point_fields is None:
        point_fields = dict()
    for field in field_list:
        if isinstance(field, fields.scalar.ScalarField):
            # convert to list of scalars and than export
            point_fields = convert_field_list(field.components(), point_fields)
    return point_fields
