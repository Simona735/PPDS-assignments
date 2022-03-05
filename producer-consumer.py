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


def producer(shared, produce_time, store_time):
    """
    The method models the producers process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        produce_time(int): production time in milliseconds 
        store_time(int): storing time in milliseconds 
    """
    sleep(produce_time / 1000)
    shared.free.wait()
    shared.mutex.lock()
    sleep(store_time / 1000)
    shared.mutex.unlock()
    shared.items.signal()
