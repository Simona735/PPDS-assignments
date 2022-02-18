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


def fnc_test(shared):
    pass


shared = Shared(1_000_000)
t1 = Thread(fnc_test, shared)
t1.join()

