"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module computes fibonacci sequence using various synchronization ADT.
"""


from time import *
from random import randint
from fei.ppds import *
import numpy as np
import matplotlib.pyplot as plt


class Shared:
    """
    Shared object. Oject represents a "warehouse" in a consumer-producer
    problem.
    """
        
    def __init__(self, size):
        """
        Initialize Shared object. The "finished" parameter indicates
        whether the activity is finished. The mutex parameter ensures
        the integrity of the access. Parameter "items" expresses the total
        number of slots and the parameter "free" expresses the number of
        free slots. Last parameter "produced" is to count all ever produced
        items.

        Args:
            size(int): size of Shared object. The parameter expresses
            how many items it can store.
        """
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(size)
        self.items = Semaphore(0)
        self.produced = 0


def producer(shared, produce_time):
    """
    The method models the producers process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        produce_time(int): production time in seconds
    """
    while True:
        sleep(produce_time)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        shared.produced += 1
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared, consume_time):
    """
    The method models the consumer process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        consume_time(int): time of consuming in seconds
    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 1000)
        shared.mutex.unlock()
        shared.free.signal()
        sleep(consume_time)


def surface_plot(x, y, z, x_label, y_label):
    """
    Make a 3d surface plot.

    Args:
        x(int[]): list of values representing observed parameter 1
        y(int[]): list of values representing observed parameter 2
        z(int[]): list of values representing number of products
            produced per second
        x_label(string): label for x value 
        y_label(string): label for y value 
    """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(x, y, z)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.zlabel('Počet výrobkov za sekundu')
    plt.show()


def main():
    production_time = 1
    processing_time = 1
    producers_count = 1
    consumers_count = 1
    storage_size = 1
    optimality = []

    optimality.clear()
    for i in range(10):
        start = time()
        shared = Shared(storage_size)
        producers = [Thread(producer,
                            shared,
                            production_time) for _ in range(producers_count)]
        consumers = [Thread(consumer,
                            shared,
                            processing_time) for _ in range(consumers_count)]

        sleep(2)
        shared.finished = True
        shared.items.signal(100)
        shared.free.signal(100)
        [t.join() for t in producers + consumers]
        end = time()
        elapsed = end - start
        optimality.append(shared.produced / elapsed)
    print(optimality)


if __name__ == "__main__":
    main()

