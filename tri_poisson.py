###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################



import src.femIO.vtk as vtk
import src.femIO.gmsh as gmsh
import src.femCore.op_laplace as lapl

femesh = gmsh.read('msh.gmsh/named.msh')

oper = lapl.PoissonAssembler()
oper.assemble(femesh)


vtk.write('finaltest/test', femesh)


