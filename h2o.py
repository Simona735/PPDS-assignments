"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements The Building H2O Problem and it's solution.
"""


from time import *
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print


class SimpleBarrier(object):
    """
    SimpleBarrier object.

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
        self.count = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self):
        """
        The wait() function shall synchronize participating threads
        at the barrier until all threads have reached wait() specifying
        the barrier. After that all threads are released to continue.
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.threads_num:
            print("")
            self.count = 0
            self.barrier.signal(self.threads_num)
        self.mutex.unlock()
        self.barrier.wait()


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
