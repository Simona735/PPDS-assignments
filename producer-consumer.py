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

