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


def bond(element_type=None):
    """
    Simulate H2O molecule bonding by printout.

    Args:
        element_type(str): element type. H - hydrogen, O - oxygen.
    """
    print(element_type, end='')


def oxygen(shared):
    """
    Simulate oxygen element, and it's bonding with 2 hydrogen elements to a H2O molecule.

    Args:
        shared(Shared): shared object containing sync mechanisms.
    """
    shared.mutex.lock()
    shared.oxygen += 1

    if shared.hydrogen < 2:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal()
        shared.hydroQueue.signal(2)

    shared.oxyQueue.wait()
    if shared.rest:
        print("O")
        return
    bond("O")
    shared.barrier.wait()
    shared.mutex.unlock()


def hydrogen(shared):
    """
    Simulate hydrogen element, and it's bonding with oxygen to a H2O molecule.

    Args:
        shared(Shared): shared object containing sync mechanisms.
    """
    shared.mutex.lock()
    shared.hydrogen += 1

    if shared.hydrogen < 2 or shared.oxygen < 1:
        shared.mutex.unlock()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal()
        shared.hydroQueue.signal(2)

    shared.hydroQueue.wait()
    if shared.rest:
        print("H")
        return
    bond("H")
    shared.barrier.wait()


def main():
    pass


if __name__ == "__main__":
    main()
