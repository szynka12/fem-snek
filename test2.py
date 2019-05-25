import femsnek.fio.stream as info

from femsnek.fields.scalar import Scalar, ScalarField, InternalScalarField

import numpy




info.OStream() << Scalar(1) << info.endl

a = ScalarField(numpy.array([1, 2, 3, 4]), ('i', 1), 'aaa')

b = a + ScalarField(numpy.array([1, 2, 3, 4]), ('b', 1), 'aaa')

