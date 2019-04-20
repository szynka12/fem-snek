import simpleMesh

mesh = simpleMesh.Mesh()

# mesh.Import_gmsh('square.msh')
mesh.Import_gmsh('quadun.msh')
mesh.Show()