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

## Task 2 - Reusable barrier:

**Task**: To further test the ADT SimpleBarrier, implement a reusable barrier. Use the ADT SimpleBarrier implemented by you in the previous task.

**Associated file**: [reusable barrier.py](reusable%20barrier.py)

## Task 3 - Fibonacci sequence:

**Task**: Create N threads. Let thread i represent the node where the element at position i+2 of the Fibonacci sequence is calculated. Let all threads share a list into which the computed elements of the sequence are stored sequentially during the computation. 

Design, using the synchronization tools discussed so far, a synchronization such that thread i+2 can perform the computation of its assigned Fibonacci number only after the threads that compute the previous numbers of the sequence have stored their results in the list. 

Use semaphores to synchronize first. Then create a second version with events. Design the solution so that the synchronization implementation can be modified without interfering with the application logic of the program.

**Associated file**: [fibonacci.py](fibonacci.py)

**Questions to think about**:
1) What is the smallest number of synchronization objects (semaphores, mutexes, events) needed to solve this problem?

2) Which of the synchronization patterns discussed (mutual exclusion, signaling, rendezvous, barrier) can be used to solve this problem? Specifically describe how that-some synchronization pattern is used in your solution.
