###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

class Error(Exception):
    """Base class for other exceptions"""
    pass


class MeshFormatError(Error):
    """Rised when error in mesh file is found"""
    pass


class MeshError(Error):
    """Rised when error in mesh specification is found"""
    pass


class FieldOperationError(Error):
    """
   Raised when illegal field operation is performed

   Examples:
   <Scalar> + <Vector>
   div(<Scalar>)
   """
    pass


class CoreError(Error):
    """
    Raised when illegal operation while fem core operation is made, e.g. quadrature creation.
    """
    pass
