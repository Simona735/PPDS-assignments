"""
2022 Simona Richterova.

This module is an example of ADT SimpleBarrier implementation.
Event signaling is used to implement the turnstile. 
"""


from random import randint
from time import sleep
from fei.ppds import Thread, Event, Mutex
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
 
 
def barrier_example(barrier, thread_id):
    """
    Simple barrier test with on-screen printouts.
    
    Args:
        barrier(SimpleBarrier): SimpleBarrier object.
        thread_id(int): id of thread.
    """
    sleep(randint(1,10)/10)
    print("thread %d before barrier" % thread_id)
    barrier.wait()
    print("thread %d after barrier" % thread_id)
 
 
sb = SimpleBarrier(5)
 
threads = [Thread(barrier_example, sb, i) for i in range(5)]
[t.join for t in threads]
