import femsnek.fields.scalar as sf
import numpy as np


internal0 = ('i', 0)
internal1 = ('i', 1)
boundary0 = ('b', 0)
boundary1 = ('b', 1)

val1 = np.array([1., 2., 3., 4., 5.])
val2 = np.array([6., 7., 8., 9., 10.])

s_const = sf.Scalar(1.)
s_field_0 = sf.ScalarField(val1, internal0)
s_field_1 = sf.ScalarField(val1, internal1)

assert np.all((s_field_1 + s_const)._value == val1 + 1.)
s_field_0 + s_field_1
