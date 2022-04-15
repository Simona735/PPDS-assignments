# @Simona735/PPDS-assignments - 08
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
Simple python application demonstrating the use of synchronous vs asynchronous programming. 

# Assignment

Write your own single-threaded application in two versions: synchronous and asynchronous (using native coroutines). In the attached documentation, explain the goal of the application and make a performance comparison between the synchronous and asynchronous versions. Be sure to justify the results obtained (speedup, slowdown, unchanged performance).

# Solution

We created two files, each associated with one version.

**Synchronous**: [synchronous.py](synchronous.py)

**Asynchronous**: [asynchronous.py](asynchronous.py)

## General description of program purpose

In general, both versions do the following. Firstly, the queue is initialized with a series of numbers. Those numbers are passed to a method squared. This method computes the squared value of each number in the queue until there is non left. The computation is simulated by sleep method. There are also printouts present for verification purposes. 

## Performance comparison:
We compared the results on a series of numbers: 1, 2, 3, 4, 5, 6. Let's list the output for each version of the program.

**Synchronous**: 

As it is synchronous, we only executed one task (task A).
```
Task A: Computing 1*1
Task A: Result is 1
Task A: Elapsed time: 1.0

Task A: Computing 2*2
Task A: Result is 4
Task A: Elapsed time: 2.1

Task A: Computing 3*3
Task A: Result is 9
Task A: Elapsed time: 3.2

Task A: Computing 4*4
Task A: Result is 16
Task A: Elapsed time: 4.2

Task A: Computing 5*5
Task A: Result is 25
Task A: Elapsed time: 5.3

Task A: Computing 6*6
Task A: Result is 36
Task A: Elapsed time: 6.4

Total elapsed time: 6.41 sec
```
The total elapsed time is 6.41 seconds.

**Asynchronous**: 
We have executed 2 tasks in this case.
```
Task A: Computing 1*1
Task B: Computing 2*2
Task A: Result is 1
Task A: Elapsed time: 1.0
Task A: Computing 3*3
Task B: Result is 4
Task B: Elapsed time: 1.1
Task B: Computing 4*4
Task A: Result is 9
Task A: Elapsed time: 2.1
Task A: Computing 5*5
Task B: Result is 16
Task B: Elapsed time: 2.1
Task B: Computing 6*6
Task A: Result is 25
Task A: Elapsed time: 3.1
Task B: Result is 36
Task B: Elapsed time: 3.2
Total elapsed time: 3.20 sec
```

The total elapsed time is 3.20 seconds. It is a significant speedup from the synchronous version. To be precise, it is a double speed up, because there were 2 tasks used to perform the actions. To prove this, we also executed the version with 3 tasks(A, B, C)

```
Task A: Computing 1*1
Task B: Computing 2*2
Task C: Computing 3*3
Task A: Result is 1
Task A: Elapsed time: 1.0
Task A: Computing 4*4
Task B: Result is 4
Task B: Elapsed time: 1.1
Task B: Computing 5*5
Task C: Result is 9
Task C: Elapsed time: 1.1
Task C: Computing 6*6
Task A: Result is 16
Task A: Elapsed time: 2.1
Task B: Result is 25
Task B: Elapsed time: 2.1
Task C: Result is 36
Task C: Elapsed time: 2.1
Total elapsed time: 2.12 sec
```

The total elapsed time is 2.12 seconds which is three times (hence three tasks) better than the synchronous version. To be noted, there will be no improvement with the use of 4 tasks for example, because in that case, there will be still a task that has to compute 2 values and the other tasks have to wait for this one to finish.
Example of 4 tasks used:

```
Task A: Computing 1*1
Task B: Computing 2*2
Task C: Computing 3*3
Task D: Computing 4*4
Task A: Result is 1
Task A: Elapsed time: 1.0
Task A: Computing 5*5
Task B: Result is 4
Task B: Elapsed time: 1.1
Task B: Computing 6*6
Task D: Result is 16
Task D: Elapsed time: 1.1
Task C: Result is 9
Task C: Elapsed time: 1.1
Task A: Result is 25
Task A: Elapsed time: 2.1
Task B: Result is 36
Task B: Elapsed time: 2.1
Total elapsed time: 2.14 sec
```

Task A and task B were each assigned two values to compute.

## Synchronous version:

The synchronous version is a classical version of a program which means that all the values are computed one by one. Every computation needs to finish before the next one starts. 

## Asynchronous version:

The asynchronous version is implemented with the use of asyncio library and its components. Each task can perform its actions asynchronously, which leads to a speedup.
