"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements a simple example of synchronous coroutine.
"""


import time
from queue import Queue


def sleep():
    """
    Sleep method that puts the program to sleep for one second.
    """
    time.sleep(1)


def squared(name, start, work_queue):
    """
    Method computes squared value for each item from work_queue.
    The computation is simulated by sleep.
    Method also contains multiple verification printouts.

    Args:
        name(string): task name
        start(float): program start time
        work_queue(Queue): queue containing all numbers to process
    """
    while not work_queue.empty():
        number = work_queue.get()
        print(f'Task {name}: Computing {number}*{number}')
        sleep()
        elapsed = time.perf_counter() - start
        print(f'Task {name}: Result is {number * number}')
        print(f"Task {name}: Elapsed time: {elapsed:.1f}\n")


def main():
    work_queue = Queue()

    for number in [1, 2, 3, 4, 5, 6]:
        work_queue.put(number)

    start = time.perf_counter()
    squared("A", start, work_queue)
    elapsed = time.perf_counter() - start

    print(f'Total elapsed time: {elapsed:.2f} sec')


if __name__ == "__main__":
    main()
