from femsnek.core.connectivity import Tri1
from numpy import array

p = array([[0, 0], [1, 0], [0, 1]]).T
print(p[:, 0])
print(Tri1().N(p))
print(Tri1().gradN(p))
print(Tri1().J(p))
print(Tri1().detJ(p))


