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


def main():
    shared = Shared()

    savages = [Thread(savage, shared, i) for i in range(SAVAGES)]
    cooks = [Thread(cook, shared, i) for i in range(COOKS)]

    for t in savages + cooks:
        t.join()


if __name__ == "__main__":
    main()
