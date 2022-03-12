"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements the The Dining Philosopher Problem and it's solution
by implementing right-handed and left-handed philosophers.
"""

from time import *
from random import randint, choice, shuffle
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


def get_forks(forks, footman, philosopher_id, first, second):
    """
    Acquire forks.

    Args:
        forks(Semaphore[]): list of forks represented by ADT Semaphore
        footman(Semaphore): footman represented by ADT Semaphore
        philosopher_id(int): ID of a philosopher
        first(int): ID of fork that is taken first. 
        second(int): ID of fork that is taken second.
    """
    footman.wait()
    print(f'{philosopher_id:02d}: try to get forks')
    forks[first].wait()
    forks[second].wait()
    print(f'{philosopher_id:02d}: forks taken')


def put_forks(forks, footman, philosopher_id, first, second):
    """
    Put forks down.

    Args:
        forks(Semaphore[]): list of forks represented by ADT Semaphore
        footman(Semaphore): footman represented by ADT Semaphore
        philosopher_id(int): ID of a philosopher
        first(int): ID of fork that is taken first.
        second(int): ID of fork that is taken second.
    """
    forks[first].signal()
    forks[second].signal()
    print(f'{philosopher_id:02d}: forks put down')
    footman.signal()


def philosopher(forks, footman, philosopher_id, main_hand):
    """
    Infinite cycle for The Dining Philosopher Problem.

    Args:
        forks(Semaphore[]): list of forks represented by ADT Semaphore
        footman(Semaphore): footman represented by ADT Semaphore
        philosopher_id(int): ID of a philosopher
        main_hand(int): philosopher's main hand. Values:
            0 - left-handed,
            1 - right-handed.
    """
    sleep(randint(40, 100) / 1000)

    if main_hand:
        first_fork = philosopher_id
        second_fork = (philosopher_id + 1) % PHIL_NUM
    else:
        second_fork = philosopher_id
        first_fork = (philosopher_id + 1) % PHIL_NUM

    while True:
        think(philosopher_id)
        get_forks(forks, footman, philosopher_id, first_fork, second_fork)
        eat(philosopher_id)
        put_forks(forks, footman, philosopher_id, first_fork, second_fork)


def get_random_hands():
    """
    Assign right and left-handed philosophers randomly with at least
    one right-haned and one left-handed.
    0 - left-handed.
    1 - right-handed.

    Returns:
        int[]: list of zeros and ones representing right and
        left-handed people. 
    """
    philosopher_hands = [0, 1]

    for x in range(PHIL_NUM - 2):
        philosopher_hands.append(choice([0, 1]))
    shuffle(philosopher_hands)

    return philosopher_hands


def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)

    philosopher_hands = get_random_hands()

    philosophers = [Thread(philosopher,
                           forks,
                           footman,
                           philosopher_id,
                           philosopher_hands[philosopher_id])
                    for philosopher_id in range(PHIL_NUM)]
    [p.join() for p in philosophers]


if __name__ == "__main__":
    main()
