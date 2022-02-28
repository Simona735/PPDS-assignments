# @Simona735/PPDS-assignments - 02 
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About

The branch contains 3 main files. Each of them solves a different task. In general, all of them deal with synchronization mechanisms.
- [Task 1 - ADT SimpleBarrier](#task-1---adt-simplebarrier)
- [Task 2 - Reusable barrier](#task-2---reusable-barrier)
- [Task 3 - Fibonacci sequence](#task-3---fibonacci-sequence)

# Assignment

The whole assignment consists of 3 tasks. Each task has a separate file. For each task, we will first list the task assignment, then its associated file and finally describe the solution. 

## Task 1 - ADT SimpleBarrier:

**Task**: Implement ADT SimpleBarrier according to the specification from the lecture. In it, we used ADT Semaphore for synchronization. After successful implementation in this way, try to use event signaling to implement the turnstile.

**Associated file**: [ADT SimpleBarrier.py](ADT%20SimpleBarrier.py)

**Describiton**: 
At the beginning, we initialize 5 threads that will start executing the barrier_example function. This function tests the functionality of the barrier using on-screen printouts. The barrier object itself has a wait() function implemented that synchronizes the threads on the barrier until all threads have reached the wait() function. Then all threads are released to continue.

**_The solution is designed so that the barrier works exactly once!_**

## Task 2 - Reusable barrier:

**Task**: To further test the ADT SimpleBarrier, implement a reusable barrier. Use the ADT SimpleBarrier implemented by you in the previous task.

**Associated file**: [reusable barrier.py](reusable%20barrier.py)

**Describiton**: The main part of the program is a cycle that tests the reusable barrier. In the loop there are 2 functions outside the barrier - rendezvous() and ko() imitating the handler code using the sleep() function.

``` python
while True:
    barrier1.reset()
    barrier1.wait()
    rendezvous(thread_name)
    barrier2.reset()
    barrier2.wait()
    ko(thread_name)
```

The barrier is implemented as a SimpleBarrier object with two functions - wait() and reset(). The first thread that reaches a given point in the code resets the barrier and from that point on the barrier is active. The wait function represents the barrier. The reset function is necessary because it was specified to use events to implement the barrier, and the barrier must be reusable compared to the first task.

The loop uses two barriers to prevent the threads from interfering with the randevouz and ko parts at the same time.

## Task 3 - Fibonacci sequence:

**Task**: Create N threads. Let thread i represent the node where the element at position i+2 of the Fibonacci sequence is calculated. Let all threads share a list into which the computed elements of the sequence are stored sequentially during the computation. 

Design, using the synchronization tools discussed so far, a synchronization such that thread i+2 can perform the computation of its assigned Fibonacci number only after the threads that compute the previous numbers of the sequence have stored their results in the list. 

Use semaphores to synchronize first. Then create a second version with events. Design the solution so that the synchronization implementation can be modified without interfering with the application logic of the program.

**Associated file**: [fibonacci.py](fibonacci.py)

**Describiton**: The program calculates the fibonacci sequence according to the task. The program is divided into main module and calculation function.

``` python
THREADS_NUM = 10

fibonacci_seq = [0] * (THREADS_NUM + 2)
fibonacci_seq[1] = 1

# adt_list = [Semaphore(0) for i in range(THREADS_NUM)]
adt_list = [Event() for i in range(THREADS_NUM)]

threads = [Thread(compute_fibonacci, i, adt_list, fibonacci_seq)
           for i in range(THREADS_NUM)]
```

The main module initializes the threads, the list of fibonacci sequence elements derived from the number of threads, and also initializes one synchronization object per thread.
The commented line represents the version with the use of semaphores. By uncommenting it and commenting out the line below it, we can modify the implementation without affecting the application logic of the program.

The main mechanism works as follows. Each thread has to wait for the previous thread to finish its activity, so the "i" thread will signal to the "i+1" thread that it can start its activity. In other words, a thread waits for the preceding thread **before** calculating and signals the following thread **after** calculating. See below:

``` python
def compute_fibonacci(i, adt_list, fibonacci_seq):
    sleep(randint(1, 10)/10)
    adt_list[i].wait()
    fibonacci_seq[i + 2] = fibonacci_seq[i + 1] + fibonacci_seq[i]
    if i + 1 < len(adt_list):
        adt_list[i + 1].signal()
```
Sleep provides thread shuffling for the purpose of demonstrating the correct functioning of the program. The condition ensures that we do not signal to a thread that does not exist - index out of range.

The first two elements of the sequence are given so that we can derive other elements from them and therefore we have to perform the initial signaling manually to start the calculation. This process is to be done after the threads are created in the main module.

``` python
  threads = [Thread(compute_fibonacci, i, adt_list, fibonacci_seq)
             for i in range(THREADS_NUM)]

  adt_list[0].signal()

  [t.join() for t in threads]
```

**Questions to think about**:
1) What is the smallest number of synchronization objects (semaphores, mutexes, events) needed to solve this problem?

2) Which of the synchronization patterns discussed (mutual exclusion, signaling, rendezvous, barrier) can be used to solve this problem? Specifically describe how that-some synchronization pattern is used in your solution.


All solutions were inspired by the knowledge from the lecture and the skelets of codes provided by the lecturer Mgr. Ing. Matúš Jókay, PhD..
