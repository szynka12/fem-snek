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


class PoissonAssembler(AssemblerBase):

    def __init__(self):
        super().__init__()

        self.asmMap = {2: self.assembleTriangle2D}
        self.matrix = 0
        
    def assembleTriangle2D(self, nodes, connectivity):
        print("Triangle 2D assemblation")

        tags = connectivity._tags

        # loop over elements
        for nEl in range(connectivity.n_elements()):
            localIds = tags[:, nEl]
            localCoords = nodes[:, localIds]

            # Tri1 is a linear triangle, therefore Jacobian is not necessary




