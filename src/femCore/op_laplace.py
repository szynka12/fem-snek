###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

from src.femCore.assemblerBase import AssemblerBase
import scipy.sparse as sp
from src.femCore.quadratures import GaussTriangle2D
import numpy as np


class PoissonAssembler(AssemblerBase):

    def __init__(self):
        super().__init__()

        self.asmMap = {2: self.assembleTriangle2D}
        self.matrix = 0
        
    def assembleTriangle2D(self, nodes, connectivity):
        print("Triangle 2D assemblation")

        nNodes = nodes.shape[1]

        tags = connectivity._tags
        quadr = GaussTriangle2D(order=2)

        # tabulate shape functions in quadrature points
        shapeF
        shapeFKsi

        # allocate storage for COO format
        i = np.zeros(nNodes)
        j = np.zeros(nNodes)
        data = np.zeros(nNodes)

        # loop over elements
        for nEl in range(connectivity.n_elements()):
            localIds = tags[:, nEl]
            localCoords = nodes[:, localIds]

            # Tri1 is a linear triangle, therefore Jacobian is computed once for element
            # compute element
            Kel = zeros((3, 3))

            for qPoint in range(quadr.npoints):
                Kel += quadr.weights[qPoint]*(shapeFKsi[qPoint].T)@(shapeFKsi[qPoint])
            Kel *= Jac


        # Push into global matrix
        i[???] = np.tile(localIds, 3)
        j[???] = np.tile(localIds, (3, 1)).transpose().ravel()
        data[???] = Kel.ravel()
        
        self.matrix = sp.csr_matrix((data, (i, j)))


