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
        self.finished = False
        self.rest = False


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


def guardian(shared, run_time):
    """
    Guardian controls the loop in main module.
    It lets it run for a certain time, then interrupts it.

    Args:
        shared(Shared): shared object containing sync mechanisms.
        run_time(float): time for which to run a program.
    """
    sleep(run_time)
    shared.finished = True


def main():
    shared = Shared()
    run_time = 3
    threads = [Thread(guardian, shared, run_time)]

    while not shared.finished:
        sleep(randint(0, 2)/1000)
        element_type = randint(0, 2)
        if not element_type:
            threads.append(Thread(oxygen, shared))
        else:
            threads.append(Thread(hydrogen, shared))

    sleep(1)
    # taking care of stuck/unbonded threads.
    if shared.hydrogen > 0 or shared.oxygen > 0:
        print(f"---- not boned elements ----\n" +
              f"hydrogen: {shared.hydrogen}, oxygen: {shared.oxygen}")
        shared.rest = True
        shared.hydroQueue.signal(shared.hydrogen)
        shared.oxyQueue.signal(shared.oxygen)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
