from fei.ppds import *
import matplotlib.pyplot as plt


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


def counter(shared, mutex):
    """Increment shared array with use of mutex"""
    while shared.index < shared.size - 1:
        mutex.lock()
        shared.array[shared.index] += 1
        shared.index += 1
        mutex.unlock()


def histogram(data):
    """Print histogram."""
    plt.hist(data)
    plt.show()


shared = Shared(1_000_000)
mutex = Mutex()
t1 = Thread(counter, shared, mutex)
t2 = Thread(counter, shared, mutex)
t1.join()
t2.join()

histogram(shared.array)
