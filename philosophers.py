"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements the The Dining Philosopher Problem and it's solution
by implementing right-handed and left-handed philosophers.
"""

from time import *
from random import randint
from fei.ppds import Thread, Semaphore, print

PHIL_NUM = 5


def think(philosopher_id):
    """
    Simulate thinking by sleep() for a random time.

    Args:
        philosopher_id(int): ID of a philosopher
    """
    print(f'{philosopher_id:02d}: thinking')
    sleep(randint(40, 50) / 1000)


def eat(philosopher_id):
    """
    Simulate eating by sleep() for a random time.

    Args:
        philosopher_id(int): ID of a philosopher
    """
    print(f'{philosopher_id:02d}: eating')
    sleep(randint(40, 50) / 1000)


def get_forks(forks, footman, philosopher_id):
    """
    Acquire forks.

    Args:
        forks(Semaphore[]): list of forks represented by ADT Semaphore
        footman(Semaphore): footman represented by ADT Semaphore
        philosopher_id(int): ID of a philosopher
    """
    footman.wait()
    print(f'{philosopher_id:02d}: try to get forks')
    forks[philosopher_id].wait()
    forks[(philosopher_id + 1) % PHIL_NUM].wait()
    print(f'{philosopher_id:02d}: forks taken')


def put_forks(forks, footman, philosopher_id):
    """
    Put forks down.

    Args:
        forks(Semaphore[]): list of forks represented by ADT Semaphore
        footman(Semaphore): footman represented by ADT Semaphore
        philosopher_id(int): ID of a philosopher
    """
    forks[philosopher_id].signal()
    forks[(philosopher_id + 1) % PHIL_NUM].signal()
    print(f'{philosopher_id:02d}: forks put down')
    footman.signal()


def philosopher(forks, footman, philosopher_id):
    """
    Infinite cycle for The Dining Philosopher Problem.

    Args:
        forks(Semaphore[]): list of forks represented by ADT Semaphore
        footman(Semaphore): footman represented by ADT Semaphore
        philosopher_id(int): ID of a philosopher
    """
    sleep(randint(40, 100) / 1000)

    while True:
        think(philosopher_id)
        get_forks(forks, footman, philosopher_id)
        eat(philosopher_id)
        put_forks(forks, footman, philosopher_id)


def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)
    philosophers = [Thread(philosopher,
                           forks,
                           footman,
                           philosopher_id)
                    for philosopher_id in range(PHIL_NUM)]
    [p.join() for p in philosophers]


if __name__ == "__main__":
    main()
