###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################
import femsnek.python.pattern as pat

class ScalarFieldEnumerator(pat.Singleton):
    __num = 0
    def inc(self):
        ScalarFieldEnumerator.__num += 1
        return ScalarFieldEnumerator.__num

ScalarFieldEnumerator()