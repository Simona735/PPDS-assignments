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
    sleep(randint(1,10)/10)
    print('rendezvous: %s' % thread_name)
 
 
def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1,10)/10)
 
 
def barrier_example(thread_name):
    """Kazde vlakno vykonava kod funkcie 'barrier_example'.
    Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    nielen pred vykonanim funkcie 'ko', ale aj
    *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
    """
 
    while True:
        # ...
        rendezvous(thread_name)
        # ...
        ko(thread_name)
        # ...
 
 
"""Vytvorime vlakna, ktore chceme synchronizovat.
Nezabudnime vytvorit aj zdielane synchronizacne objekty,
a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
synchronizovat.
"""
threads = list()
for i in range(5):
    t = Thread(barrier_example, 'Thread %d' % i)
    threads.append(t)
 
for t in threads:
    t.join()
