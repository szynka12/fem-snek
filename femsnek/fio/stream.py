from abc import ABC, abstractmethod


class WritableBase(ABC):
    @property
    @abstractmethod
    def __repr__(self):
        pass


class OStream(object):
    def __init__(self, output=None):
        if output is None:
            import sys
            output = sys.stdout
        self.output = output
        self.format = '%s'

    def __lshift__(self, stream_input):
        if isinstance(stream_input, IOManipulator):
            stream_input.do(self)
        elif isinstance(stream_input, WritableBase) or isinstance(stream_input, (int, float, str)):

            self.output.write(self.format % stream_input)
            self.format = '%s'
            return self
        else:
            raise TypeError('OStream() input must be derived from WritableBase or IOManipulator classes!\n '
                            'Encountered object: ' + str(type(stream_input)))


class IOManipulator(object):
    def __init__(self, function=None):
        self.function = function

    def do(self, ostream):
        self.function(ostream)


def do_endl(stream):
    stream.output.write('\n')
    stream.output.flush()


endl = IOManipulator(do_endl)
