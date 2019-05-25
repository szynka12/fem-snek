"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: explicit
   :synopsis: Explicit operations in fem framework
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

import femsnek.fields.field as f


def integral(field: f.FieldBase):
    int_output = 0

    # extract mesh from field
    mesh = field.mesh()
    for i in range(mesh.n_lists()):

        # get fem calculator, it will give us quadratures, element Jacobian etc.
        c = mesh.lists()[i].fem_calculator()
        q, w = c.quadrature()   # quadrature and weights
        n = c.N(q)              # shape functions at q-points
        for el in range(mesh.lists()[i].n_elements()):
            element_coordinates = field._ref_feMesh._nodes[:, mesh.lists()[i][el]]
            # extract nodal values in the element
            nodal_values = field.nodal()[mesh.lists()[i][el]]

            # accumulate integral
            int_output += c.detJ(element_coordinates)*nodal_values @ n*w

    return int_output


