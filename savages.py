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
