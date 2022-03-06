"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements the solution for Producer-Conusmer problem and
executes experiments to find out optimal settings for given variables.
"""


from time import *
from random import randint
from fei.ppds import *
import numpy as np
import plotly.graph_objects as go


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
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y,
                                     contours={
                                         "x": {"show": True, "size": 1},
                                         "y": {"show": True, "size": 1},
                                         "z": {"show": True, "size": 1},
                                     },)])
    fig.update_layout(width=500, height=500,
                      margin=dict(l=0, r=0, b=0, t=0),
                      scene=dict(
                          xaxis=dict(title=x_label),
                          yaxis=dict(title=y_label),
                          zaxis=dict(title="Products per second")))
    fig.show()


def average(list_values):
    """
    Copmute an average value of 1D list.

    Args:
        list_values([]): list of values, possible values are int,
            double or float
    """
    return sum(list_values) / len(list_values)


def producer_consumer(produce, process, producers, consumers, size):
    """
    Model the problem of Producers-consumers.

    Args:
        produce(double): production time in seconds
        process(double): processing time in seconds
        producers(int): number of producers
        consumers(int): number of consumers 
        size(int): storage size
        
    Returns:
        shared.produced(int) - all products ever added to the storage
    """
    shared = Shared(size)
    producers = [Thread(producer,
                        shared,
                        produce) for _ in range(producers)]
    consumers = [Thread(consumer,
                        shared,
                        process) for _ in range(consumers)]

    sleep(0.2)
    shared.finished = True
    shared.items.signal(100)
    shared.free.signal(100)
    [t.join() for t in producers + consumers]
    return shared.produced


def main():
    production_time = 0.02
    processing_time = 0.01
    producers_count = 10
    consumers_count = 5
    storage_size = 5

    param1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    param2 = [10, 12, 15, 17, 20, 22, 25, 27, 30, 32]
    param1_label = "Producers count"
    param2_label = "Storage size"
    optimality = np.empty([len(param1), len(param2)], dtype=int)

    for m in range(len(param1)):
        average_optimality = []
        for n in range(len(param2)):
            print("\n", m, n,"\t", end=" ")
            optimality_values = []
            for i in range(10):
                print(".", end=" ")
                start = time()
                produced = producer_consumer(production_time,
                                  processing_time,
                                  param1[m],
                                  consumers_count,
                                  param2[n])
                optimality_values.append(produced /(time() - start))
            optimality[n][m] = average(optimality_values)
        print()
    print("\n", optimality)
    surface_plot(param1, param2, optimality, param1_label, param2_label)


if __name__ == "__main__":
    main()
