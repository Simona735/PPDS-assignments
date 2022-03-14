"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements various synchronization mechanisms.
You can find the complete description in a README.md file - Task 2.
"""


from time import *
from random import randint, choice, shuffle
from fei.ppds import Thread, Semaphore, Mutex, Event, print


MONITORS = 8
SENSORS = 3


class Lightswitch:
    """
    Lightswitch object. Synchronization object that implements
    two methods - lock and unlock.
    """

    def __init__(self):
        """ Initialize Lightswitch. """
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        """
        The lock() function works on the principle that the first thread
        to use the resource calls wait() on the semaphore to signal
        that the resource is occupied (i.e., locked).
        
        Args:
            semaphore(Semaphore): semaphore object
            
        Returns:
            int: number of objects using resource
        """
        self.mutex.lock()
        counter = self.counter
        if not self.counter:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        """
        The unlock() function works on the principle that the last thread
        to leave the resource calls signal() on the semaphore to signal
        that the resource is free (i.e., unlocked).
        
        Args:
            semaphore(Semaphore): semaphore object
        """
        self.mutex.lock()
        self.counter -= 1
        if not self.counter:
            semaphore.signal()
        self.mutex.unlock()


def main():
    pass    

if __name__ == '__main__':
    main()

