import simpleMesh

import vtkTools as vtk



mesh = simpleMesh.Mesh()
mesh.Import_gmsh('msh.gmsh/quadtri.msh')

vtk.export('./test', mesh)


