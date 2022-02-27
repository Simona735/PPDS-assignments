"""
2022 Simona Richterova.

This module is an example of and reusable ADT SimpleBarrier implementation.
"""


from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Event
from fei.ppds import print


class SimpleBarrier:
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
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Event()
 
    def wait(self):
        """
        The wait() function shall synchronize participating threads
        at the barrier until all threads have reached wait() specifying
        the barrier. After that all threads are released to continue.
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads_num:
            self.counter = 0
            self.turnstile.signal()
        self.mutex.unlock()
        self.turnstile.wait()
 
 
def rendezvous(thread_name):
    """
    Imitate rendezvous using sleep. 
    """
    sleep(randint(1, 10)/10)
    print('rendezvous: %s' % thread_name)
 
 
def ko(thread_name):
    """
    Imitate critical area using sleep.
    """
    print('ko: %s' % thread_name)
    sleep(randint(1, 10)/10)
 
 
def barrier_example(barrier1, barrier2, thread_name):
    """
    Barrier infinite cycle test.
    """
 
    while True:
        barrier1.wait()
        rendezvous(thread_name)
        barrier2.wait()
        ko(thread_name)
 
 
THREADS_NUM = 10

sb1 = SimpleBarrier(THREADS_NUM)
sb2 = SimpleBarrier(THREADS_NUM)

threads = list()
for i in range(THREADS_NUM):
    t = Thread(barrier_example, sb1, sb2, 'Thread %d' % i)
    threads.append(t)
 
for t in threads:
    t.join()
