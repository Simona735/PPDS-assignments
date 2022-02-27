"""
2022 Simona Richterova.

This module computes fibonacci sequence using various synchronization ADT.
"""

from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, Event


def compute_fibonacci(i, adt_list):
    """
    Computes fibonacci sequence using multiple threads and sync mechanism.

    Args:
        adt_list(object): list of sync objects. One for each thread.
    """
    sleep(randint(1, 10)/10)
    adt_list[i].wait()
    fibonacci_seq[i + 2] = fibonacci_seq[i + 1] + fibonacci_seq[i]
    adt_list[i + 1].signal()


THREADS_NUM = 10

fibonacci_seq = [0] * (THREADS_NUM + 2)
fibonacci_seq[1] = 1

adt_list = [Semaphore(0) for i in range(THREADS_NUM)]
adt_list[0].signal()

threads = list()
for i in range(THREADS_NUM):
    t = Thread(compute_fibonacci, i, adt_list)
    threads.append(t)

for t in threads:
    t.join()

print(fibonacci_seq)
