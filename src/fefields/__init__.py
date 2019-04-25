import src.python.pattern as pat

class ScalarFieldEnumerator(pat.Singleton):
    __num = 0
    def inc(self):
        ScalarFieldEnumerator.__num += 1
        return ScalarFieldEnumerator.__num

ScalarFieldEnumerator()