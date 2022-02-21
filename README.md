# @Simona735/PPDS-assignments - 01 
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About

Simple python application with 2 threads and one shared object (list). Threads increment each list item and try not to interfere with each other by using mutex.

# Assignment
Implement two threads that will use a common index into a common array (initialized to 0 values) of some size. Let each thread increment the element of the array where the common index is currently pointing. Then let it increment the index. If the index is already pointing outside the array, the thread will terminate. When the threads are finished, count how many elements of the array have a value of 1. If you find that not every element of the array has a value of 1, modify the program to find out the frequencies (histogram) of the values that are in the array at the end (after the threads have finished running). 

For homework, try to create three variations of using the lock in different places in the code (so that their use makes sense, not misuse), and include in your solution documentation what effect a given lock location has on code execution (from a parallel programming perspective).

# Files
Branch contains 3 files as 3 variations of using the lock.
- [cvicenie 1_1.py](cvicenie%201_1.py)
- [cvicenie 1_2.py](cvicenie%201_2.py)
- [cvicenie 1_3.py](cvicenie%201_3.py)

I will first list the identical parts of the code and then describe the differences.
## Identical parts

Each file contains class definition of object Shared

```python
class Shared():
    """
    Shared array.
    Keyword arguments:
    counter -- current array index
    end -- array size
    elms -- array itself
    """
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * end
```

As per the assignment, each file also contains a method to print a histogram of integer occurrences in the list.
Source: [matplotlib.pyplot](https://matplotlib.org/stable/api/pyplot_summary.html)
```python
def histogram(data):
    """Print histogram."""
    plt.hist(data)
    plt.show()
```

The main code consists of creating an instacne of the shared object, two threads which perform the given method (different in each file, see below) and printing a histogram of results.

## cvicenie 1_1.py

Part of code specific for this file is:

```python
def counter(shared, mutex):
    """Increment shared array with use of mutex"""
    while shared.counter < shared.end - 1:
        mutex.lock()
        shared.elms[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()
```
**Prerequisities:** made only for 2 theads.

:warning: **Warning:** there is a possibility that the last item of list **_will not_** be incremented as it should be.

**Parallel programming effect:** In ideal state (we suppose all items will be incremented by one), there is partial paralelism. One thread evaluates the condition of while loop while the other thread increments the list item ale list index. 

## cvicenie 1_2.py

Part of code specific for this file is:

```python
def counter(shared, mutex):
    """Increment shared array with use of mutex"""
    mutex.lock()
    while shared.counter < shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()
```

**Prerequisities:** works for N threads.

**Parallel programming effect:** There is basically no paralelism as only one thread is allowed to handle the code, while the other waits for the first one to finish. After that, all the work is done.

## cvicenie 1_3.py

Part of code specific for this file is:

```python
def counter(shared, mutex):
    """Increment shared array with use of mutex"""
    while True:
        mutex.lock()
        if shared.counter >= shared.end:
            mutex.unlock()
            break;
        shared.elms[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()
```

**Prerequisities:** works for N threads.

**Parallel programming effect:** There is no paralelism also. The difference is that the threads take turns in executing the handler code.

**Remark:** Third solution is inspired by Mgr. Ing. Matúš Jókay, PhD.. The base of the solution is no different from cvicenie 1_2.py so it does not count as third variation. 
