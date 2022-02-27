"""
2022 Simona Richterova.

This module computes fibonacci sequence using various synchronization ADT.
"""

from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, Event


def compute_fibonacci(i):
    sleep(randint(1, 10)/10)
    fibonacci_seq[i + 2] = fibonacci_seq[i + 1] + fibonacci_seq[i]


THREADS_NUM = 10

fibonacci_seq = [0] * (THREADS_NUM + 2)
fibonacci_seq[1] = 1

ads_list = [Semaphore(0) for i in range(THREADS_NUM)]
ads_list[0].signal()

threads = list()
for i in range(THREADS_NUM):
    t = Thread(compute_fibonacci, i)
    threads.append(t)

for t in threads:
    t.join()

print(fibonacci_seq)
