"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements The Building H2O Problem and it's solution.
"""


from time import *
from random import randint, choice, shuffle
from fei.ppds import Thread, Mutex, Semaphore, print


class SimpleBarrier:
    """
    SimpleBarrier object. Event is used to implement the turnstile.
    Args:
        threads_num(int): number of threads
    """
        
    def __init__(self, threads_num):
        """
        Initialize SimpleBarrier.
        
        Args:
            threads_num(int): number of threads
        """
        self.threads_num = threads_num
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Event()
 
    def wait(self):
        """
        The wait() function shall synchronize participating threads
        at the barrier until all threads have reached wait() specifying
        the barrier. After that all threads are released to continue.
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads_num:
            self.counter = 0
            self.turnstile.signal()
        self.mutex.unlock()
        self.turnstile.wait()


class Shared(object):
    """
    Shared object containing all synchronization mechanisms.
    """

    def __init__(self):
        self.mutex = Mutex()
        self.barrier = SimpleBarrier(3)
        self.oxygen = 0
        self.hydrogen = 0
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)


def oxygen(shared):
    pass


def hydrogen(shared):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
