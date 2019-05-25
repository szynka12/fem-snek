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
from femsnek.mesh.feMesh import FeMesh, Mesh
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


def write(path: str, femesh: FeMesh, fields_list = None) -> None:
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
       :param fields_list: list of fields 
       :param femesh: - finite element mesh object
    """
    if fields_list is not None:
        point_fields = convert_field_list(fields_list)
    else:
        point_fields = dict()

    # export internal regions
    for i in range(len(femesh._internalMesh)):
        export_region(path, ('i', i), point_fields.get(('i', i)), femesh)

    for i in range(len(femesh._boundaryMesh)):
        export_region(path, ('b', i), point_fields.get(('b', i)), femesh)


def export_region(path: str, region: (str, int), fields: dict, femesh: FeMesh):
    vtk_connectivity = np.empty(0, dtype=np.int32)
    vtk_offsets = np.empty(1, dtype=np.int32)
    vtk_offsets[0] = 0
    vtk_cell_types = np.empty(0, dtype=np.int8)
    for con_list in femesh[region]._connectivityLists:
        n_el = con_list.n_elements()
        el_nodes = con_list.n_nodes()
        vtk_connectivity = np.append(vtk_connectivity, con_list._tags.flatten('f'), axis=0)
        vtk_offsets = np.append(vtk_offsets,
                                [el_nodes * (i + 1) + vtk_offsets[-1] for i in range(n_el)],
                                axis=0)
        vtk_cell_types = np.append(vtk_cell_types,
                                   vtkTypes[con_list.el_type()].tid *
                                   np.ones((n_el,), dtype=np.int8),
                                   axis=0)

        filename = path + '.' + region[0] + '.' + str(femesh[region].id())

        evtk.hl.unstructuredGridToVTK(filename,
                                      femesh._nodes[0, femesh[region]._node_tags],
                                      femesh._nodes[1, femesh[region]._node_tags],
                                      femesh._nodes[2, femesh[region]._node_tags],
                                      vtk_connectivity,
                                      vtk_offsets[1:],
                                      vtk_cell_types,
                                      pointData=fields)


def convert_field_list(field_list: list, point_fields=None) -> dict:
    if point_fields is None:
        point_fields = dict()
    for field in field_list:
        if not isinstance(field, fields.scalar.ScalarField):
            # convert to list of scalars and than export
            point_fields = convert_field_list(field.components(), point_fields)
        else:
            if field.region() not in point_fields:
                point_fields[field.region()] = dict()
            point_fields[field.region()][field.name()] = field.nodal()

    return point_fields
