###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################


import femsnek.fio.vtk as vtk
import femsnek.fio.gmsh as gmsh


femesh = gmsh.read('msh.gmsh/named.msh')

# import elements
# nodes = array([[0, 1, 1, 0, 0.5], [0, 0, 1, 1, 2], [0, 0, 0, 0, 0]])
# ver = 'syntetic'
# tri = elements.ListTri1(1)
# quad = elements.ListQuad1(1)

# tri[0] = [3, 2, 4]
# quad[0] = [0, 1, 2, 3]

# e_list = [quad, tri]
# id_list = [1, 1]

# femesh =  FeMesh(ver,
#                   nodes,
#                   e_list,
#                   id_list)       


vtk.write('final/test', femesh)
