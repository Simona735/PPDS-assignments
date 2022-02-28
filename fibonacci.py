"""
2022 Simona Richterova.

This module computes fibonacci sequence using various synchronization ADT.
"""


from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, Event


def compute_fibonacci(i, adt_list, fibonacci_seq):
    """
    Computes fibonacci sequence using multiple threads and sync mechanism.

    Args:
        adt_list(object[]): list of sync objects. One for each thread.
        fibonacci_seq(int[]): list of fibonacci sequence. 
    """
    sleep(randint(1, 10)/10)
    adt_list[i].wait()
    fibonacci_seq[i + 2] = fibonacci_seq[i + 1] + fibonacci_seq[i]
    if i + 1 < len(adt_list):
        adt_list[i + 1].signal()


def main():
    THREADS_NUM = 10

    fibonacci_seq = [0] * (THREADS_NUM + 2)
    fibonacci_seq[1] = 1

    # adt_list = [Semaphore(0) for i in range(THREADS_NUM)]
    adt_list = [Event() for i in range(THREADS_NUM)]

    threads = [Thread(compute_fibonacci, i, adt_list, fibonacci_seq)
               for i in range(THREADS_NUM)]
    
    adt_list[0].signal()
    
    [t.join() for t in threads]

    print(fibonacci_seq)


if __name__ == '__main__':
    main()
