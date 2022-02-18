from fei.ppds import *


class Shared():
    """
    Shared array.

    Keyword arguments:
    index -- current array index
    size -- array size 
    array -- array itself
    """ 
    def __init__(self, size):
        self.index = 0
        self.size = size
        self.array = [0] * size


def counter(shared):
    pass


shared = Shared(1_000_000)
t1 = Thread(counter, shared)
t1.join()

