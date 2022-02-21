from fei.ppds import *
import matplotlib.pyplot as plt


class Shared():
    """
    Shared array.

    Keyword arguments:
    counter -- current array index
    threads_count -- number of threads
    end -- array size
    elms -- array itself
    """
    def __init__(self, end):
        self.counter = 0
        self.threads_count = 0
        self.end = end
        self.elms = [0] * end


def counter(shared, mutex):
    """Increment shared array with use of mutex"""
    while shared.counter < shared.end - 1:
        mutex.lock()
        shared.elms[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()

    shared.threads_count += 1
    while shared.threads_count < 2:
        continue

    mutex.lock()
    if shared.counter != shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
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

histogram(shared.elms)
