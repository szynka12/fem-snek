import femsnek.mesh.feMesh as feMesh
import femsnek.fields.scalar as scalar
import femsnek.fio.stream as info
import femsnek.fio.vtk as vtk


mesh = feMesh.FeMesh.from_gmsh('../data/msh.gmsh/named.msh')
mesh.info()

print(mesh('dol'))
print(mesh[mesh('dol')].id())
print(mesh[mesh('dol')].n_nodes())

S = scalar.ScalarField.by_fun('test',
                              lambda x, y, z: x + y + z,
                              mesh)
S2 = scalar.ScalarField.by_fun('test_bound',
                               lambda x, y, z: x,
                               mesh,
                               mesh('dol'))

S3 = scalar.ScalarField.by_fun('test_bound',
                               lambda x, y, z: y,
                               mesh,
                               mesh('prawa'))


info.OStream() << S << info.endl
info.OStream() << S2 << info.endl


vtk.write('../../final/test', mesh, [S, S2, S3])
