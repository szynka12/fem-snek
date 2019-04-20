import simpleMesh

mesh = simpleMesh.Mesh()

# mesh.Import_gmsh('msh.gmsh/square.msh')
mesh.Import_gmsh('msh.gmsh/quadun.msh')
mesh.Show()