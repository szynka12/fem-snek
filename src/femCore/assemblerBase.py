###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################


class AssemblerBase(object):
    __slots__ = ("asmMap", "matrix")

    def __init__(self):
        pass

    def assemble(self, mesh):
        for imesh in mesh._internalMesh:
            for el in imesh._connectivityLists:
                self.asmMap[el.el_type()](mesh._nodes,el)

