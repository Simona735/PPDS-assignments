"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements the dining savages problem and it's solution.
"""


from time import *
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, Event, print


"""
SERVINGS, SAVAGES and COOKS are model parameters.
    SERVINGS: the number of stewed missionary servings
        that will fit in the pot.
    SAVAGES: the number of savages in the tribe.
    COOKS: the number of cooks in the tribe.
"""
SERVINGS = 8
SAVAGES = 3
COOKS = 5


class SimpleBarrier(object):
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
        self.count = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None):
        """
        The wait() function shall synchronize participating threads
        at the barrier until all threads have reached wait() specifying
        the barrier. After that all threads are released to continue.

        Args:
            each(str): string to be printed by each thread
            last(str): string to be printed by the last thread
        Returns:
            bool: returns true if the thread was last, false otherwise
        """
        self.mutex.lock()
        if each:
            print(each)
        self.count += 1
        is_last = False
        if self.count == self.threads_num:
            if last:
                print(last)
            self.count = 0
            is_last = True
            self.barrier.signal(self.threads_num)
        self.mutex.unlock()
        self.barrier.wait()
        return is_last


class Shared(object):
    """
    Shared object containing all synchronization mechanisms, and it also
    represents the pot for servings. Param servings server for that.
    empty_pot and full_pot semaphores are to signal related events.
    Barriers are to ensure a proper synchronization in savages and
    cooks processes.
    """

    def __init__(self):
        self.servings = 0
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

        self.barrier1 = SimpleBarrier(SAVAGES)
        self.barrier2 = SimpleBarrier(SAVAGES)

        self.barrier3 = SimpleBarrier(COOKS)


def eat(i):
    """
    Simulate eating by sleep.

    Args:
        i(int): id of savage that eats
    """
    print(f"savage {i}: feasting")
    sleep(randint(20, 50) / 100)


def get_serving_from_pot(shared, i):
    """
    Simulate taking a portion from pot by decrementing the serving's
    counter and printout.

    Args:
        shared(Shared): shared object with sync mechanisms.
        i(int): id of savage that takes a portion form pot
    """
    shared.servings -= 1
    print(f"savage {i}: takes from pot, portions left: {shared.servings}")


def put_servings_in_pot(shared, i):
    """
    Simulate putting portions to pot by adding the count to the serving's
    counter and printout.

    Args:
        shared(Shared): shared object with sync mechanisms.
        i(int): id of cook that adds portions to pot
    """
    print(f"cook {i}: all cooked, servings to pot")
    shared.servings += SERVINGS


def cook(shared, i):
    """
    Simulate the process of a cook, which includes waiting for pot
    to be empty, then cooking all portions, and adding mentioned portions
    to the pot. After that, the last cook signals that the pot is full.

    Args:
        shared(Shared): shared object with sync mechanisms.
        i(int): id of cook
    """
    while True:
        shared.empty_pot.wait()

        print(f"cook {i}: cooking")
        sleep(randint(50, 80) / 100)

        is_last = shared.barrier3.wait()
        if is_last:
            put_servings_in_pot(shared, i)
            shared.full_pot.signal()


def savage(shared, i):
    """
    Simulate the process of a savages, which includes trying to get
    a portion from a pot. If the pot is empty, the savage wakes all
    the cooks and waits for a pot to be refilled. If the pot is full,
    savage takes a portion for himself and eats it.

    Args:
        shared(Shared): shared object with sync mechanisms.
        i(int): id of savage
    """
    sleep(randint(0, 100) / 100)

    while True:
        shared.barrier2.wait(last=f"savage {i}: all of us are here, let's have dinner")
        shared.mutex.lock()
        print(f"savage {i}: num of servings in pot is {shared.servings}")
        if shared.servings == 0:
            print(f"savage {i}: wakes all cooks")
            shared.empty_pot.signal(COOKS)
            shared.full_pot.wait()
        get_serving_from_pot(shared, i)
        shared.mutex.unlock()
        eat(i)
        shared.barrier1.wait(last=" ")


def main():
    shared = Shared()

    savages = [Thread(savage, shared, i) for i in range(SAVAGES)]
    cooks = [Thread(cook, shared, i) for i in range(COOKS)]

    for t in savages + cooks:
        t.join()


if __name__ == "__main__":
    main()
