###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

#-------------------------------------------------------------------------------
## Imports 
#-------------------------------------------------------------------------------
import numpy as np
from src.fefields import ScalarFieldEnumerator
from src.io.error import FieldOperationError

class Scalar:
    __slots__ = (
        '_value',
        '_name'
    )
    def __init__(self, value):
        try:
            self._value = float(value)
        except TypeError: 
            print('Scalar input must be a single value')
        self._name = str(self._value)
            
    def __add__(self, scalar):
        if isinstance(scalar, Scalar):
            return Scalar(self._value + scalar._value)
        elif isinstance(scalar, ScalarField):
            return ScalarField(self._value + scalar._value, scalar._region)
        else:
            raise TypeError(('Can\'t add scalar and' +  str(type(scalar)) )) 
            
            
class ScalarField:
    __slots__ = (
        '_value',
        '_region',
        '_name'
    )
    def __init__(self, value, region, name=False):
        self._value = value
        self._region = region
        if name:
            try:
                self._name = str(name)
            except TypeError('Field name must be a string'):
                pass
        else:
            self._name = 'ScalarF' + str(
                ScalarFieldEnumerator.getInstance().inc())   
    
    def isCompatible(self, scalar_field):
        if (isinstance(scalar_field, ScalarField) and 
            self._region == scalar_field._region):
            raise FieldOperationError('Cant operate on ' + str(type(self)) + 
                                      ' and ' + str(type(scalar_field)) + '!')
        
    def __add__(self, scalar):
        if not isinstance(scalar, Scalar):
            self.isCompatible(scalar)
        return ScalarField(self._value + scalar._value, self._region)
    


class InternalScalarField(ScalarField):
    def __init__(self, femesh, value, index, name=False):
        if femesh._internalMesh[index]._node_tags.shape[0] != value.shape[0]:
            raise FieldOperationError('Invalid number of field values')
        super().__init__(value, ('i', index), name)
        
        
class BoundaryScalarField(ScalarField):
    def __init__(self, femesh, value, index, name=False):
        if femesh._boundaryMesh[index]._node_tags.shape[0] != value.shape[0]:
            raise FieldOperationError('Invalid number of field values')
        super().__init__(value, ('b', index), name)