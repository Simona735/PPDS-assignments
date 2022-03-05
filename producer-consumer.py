"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module computes fibonacci sequence using various synchronization ADT.
"""


from time import sleep
from random import randint
from fei.ppds import *


class Lightswitch:
    """
    Lightswitch object. Syncronization object that implements
    two methods - lock and unlock.
    """
        
    def __init__(self):
        """ Initialize Lightswitch. """
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        """
        The lock() function works on the principle that the first thread
        to "enter the room" calls wait() on the semaphore to signal
        that the room is occupied (i.e., locked).

        Args:
            semaphore(Semaphore): semaphore object
        """
        self.mutex.lock()
        if not self.counter:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()

    def unlock(self, semaphore):
        """
        The unlock() function works on the principle that the last thread
        to "leave the room" calls signal() on the semaphore to signal
        that the room is free (i.e., unlocked).

        Args:
            semaphore(Semaphore): semaphore object
        """
        self.mutex.lock()
        self.counter -= 1
        if not self.counter:
            semaphore.signal()
        self.mutex.unlock()


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
        free slots. 

        Args:
            size(int): size of Shared object. The parameter expresses
            how many items it can store.
        """
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(size)
        self.items = Semaphore(0)


def producer(shared, produce_time):
    """
    The method models the producers process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        produce_time(int): production time in milliseconds
    """
    while True:
        sleep(produce_time / 1000)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 1000)
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared, consume_time):
    """
    The method models the consumer process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        consume_time(int): time of consuming in milliseconds
    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 1000)
        shared.mutex.unlock()
        shared.free.signal()
        sleep(consume_time / 1000)


def main():
    production_time = 1
    processing_time = 1
    producers_count = 1
    consumers_count = 1
    storage_size = 1

    shared = Shared(storage_size)
    producers = [Thread(producer,
                        shared,
                        production_time) for i in range(producers_count)]
    consumers = [Thread(consumer,
                        shared,
                        processing_time) for i in range(consumers_count)]

    sleep(1)
    [t.join() for t in producers + consumers]
    


if __name__ == "__main__":
    main()

