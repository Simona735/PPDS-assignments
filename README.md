# @Simona735/PPDS-assignments - 06
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
Simple python application solving a less classical synchronization problem - building H2O.

# Assignment

Various less classical synchronization problems were introduced at the lecture and our job was to pick one of them and implement it together with its solution. My choice is Building H2O. Building H2O is a concurrency problem where there are two kinds of threads, oxygen, and hydrogen. 

The goal is to group these threads to form water molecules. To assemble these molecules we will need triplets of elements with the correct number - one oxygen and 2 hydrogens. Because of this, we have to create a barrier that makes each thread wait until a complete molecule set is ready. This means that threads should pass the barrier in groups of three, and they must be able to immediately bond with each other to form a water molecule. It must be guaranteed that all the threads from one molecule bond before any other threads from the next molecule do. 

In other words:
- If an oxygen thread arrives at the barrier when no hydrogen threads are present, it has to wait for two hydrogen threads.
- If a hydrogen thread arrives at the barrier when no other threads are present, it has to wait for an oxygen thread and another hydrogen thread.

The key is that the threads pass the barrier in complete sets; thus, if we examine the sequence of threads that invoke bond and divide them into groups of three, each group should contain one oxygen and two hydrogens.

## Analysis

As it was said, we are going to need two types of threads - oxygen and hydrogen. We are also going to need a barrier to form molecules, a waiting queue for elements waiting to bond and we will need counters to keep track of the number of elements. To protect the integrity of these shared objects, we will need a mutex. 
To sum up, let's look at the shared object of mentioned synchronization mechanisms:

```python
class Shared(object):
    def __init__(self):
        self.mutex = Mutex()
        self.barrier = SimpleBarrier(3)
        self.oxygen = 0
        self.hydrogen = 0
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)
```

The thread's logic goes as follows. Oxygen for example: Oxygen enters the thread and checks in, meaning that it increases a counter for oxygens. Next, it checks the hydrogen counter to see wheater it can bond molecule or not. Molecule needs only one oxygen so it doesn't have to check for other oxygens. If there are not enough hydrogens, it has to wait for them. If there is enough, we can proceed to form a molecule. How does this happen? Counters are counting only the waiting elements so we have to decrement them: ```oxygen -= 1``` and ```hydrogen -= 2```. 

As mentioned, there are also queues present. When there are not enough elements to form a molecule, the elements are sent to wait in the queue. There must be a queue for each element type because to let elements out of the queue, we must let out the correct number of elements. So if we use two queues, we will pass one element from the oxygen queue and 2 elements from the hydrogen queue. In our case, the queue is implemented with Semaphore for easy use. This means there is a certain point where all threads are queued by ```queue.wait()```. When we decided that there are enough elements to form a molecule, we have to let the appropriate number of elements pass through the queue:

```python
oxyQueue.signal()
hydroQueue.signal(2)
```

Last needed element is used to signal to queues. And we want that element to continue to bond a molecule as quickly as possible, so we firstly decrement the counters and signal to queues after that.

To properly describe all the parts, let's go back to the part where there are not enough elements for a molecule. When this happens, we have to send the element to the queue and because we use a mutex to protect the integrity, we have to unlock it so that another thread can proceed to the evaluation. 

The whole part before the queue(included):
```python
shared.mutex.lock()
shared.oxygen += 1

if shared.hydrogen < 2:
    shared.mutex.unlock()
else:
    shared.oxygen -= 1
    shared.hydrogen -= 2
    shared.oxyQueue.signal()
    shared.hydroQueue.signal(2)

shared.oxyQueue.wait()
```

We cannot unlock the mutex at the end of queue signaling. As there is a possibility that another thread can enter the process, overtake the signaling thread, and take its place in the bonding process. Therefore, there is no ```mutex.unlock()``` in this part.

After the queue is passed, we will build a molecule. This action is simulated by method ```bond()``` which takes as a parameter the molecule type in a form of string. 
H - hydrogen, O - oxygen.

The method simulates the bonding process by printing out the molecule type which also serves for verification purposes. 

Earlier, we have mentioned a barrier and now it comes to place. The barrier is placed after the bond method. It can be interpreted as that the elements are forming a molecule and this formation continues until all elements meet at the barrier and thus the molecule is formed into one. The problem's requirement says: It must be guaranteed that all the threads from one molecule bond before any other threads from the next molecule do. This is too a reason why there is a barrier after the bonding process. If it wasn't there, another triplet might get to form a molecule before this one finishes. A barrier with a combination of mutex takes care of this, but we will get to mutex below. 

There is another possibility of arrangement. We can implement two barriers, one before bonding and the other after bonding. But why would we do that when we can use fewer synchronization means to accomplish the task? 

Lastly, the mutex question remains. One thread still keeps the mutex locked and to fulfill the requirement of guaranteed molecule bonding before any other threads from the next molecule, it has to be unlocked after the threads pass the barrier. Which thread will unlock the mutex? We have one locked mutex and exactly one oxygen thread present so the answer is crystal clear. 

**Oxygen and hydrogen solutions:**
```python
oxygen():
    mutex.lock()
    oxygen += 1

    if hydrogen < 2:
        mutex.unlock()
    else:
        oxygen -= 1
        hydrogen -= 2
        oxyQueue.signal()
        hydroQueue.signal(2)

    oxyQueue.wait()
    bond("O")
    barrier.wait()
    mutex.unlock()
```

```python
hydrogen():
    mutex.lock()
    hydrogen += 1

    if hydrogen < 2 or oxygen < 1:
        mutex.unlock()
    else:
        oxygen -= 1
        hydrogen -= 2
        oxyQueue.signal()
        hydroQueue.signal(2)

    hydroQueue.wait()
    bond("H")
    barrier.wait()
```

## Running the program

We decided to run the program for a period of time, during which we randomly generate threads of hydrogen and oxygen in a 2:1 ratio.  
The random generation is impleneted like this:

```python
element_type = randint(0, 2)
if not element_type:
    threads.append(Thread(oxygen, shared))
else:
    threads.append(Thread(hydrogen, shared))
```

This process runs in a cycle, which we will have to terminate. To achieve this, we added a 'finished' variable to sync mechanisms and initialized it to False. The while cycle evaluates this variable and runs while it remains set to False. We have created a third type of thread - guardian. This thread is initialized before the while loop and is sleeps for a given time, after that, it sets the 'finished' variable to True and this stops the thread generating process.

We have to take into account that the generated threads may not exactly form the desired triplets and it could happen that for example two oxygens were left. We have to release the remaining elements from the queue. This can't happen right away, because there may have been many generated threads and molecules may still be forming. Therefore, we use sleep to make sure that all valid triplets have time to form into molecules. 

After that, we will release the remaining amount of elements from queues. We have to take into account that these elements can't form a molecule so we have to interrupt the code after that. This can be achieved by adding another shared variable called 'rest' initially set to False. When we get to the part of releasing the remaining elements, we set the variable to True. We also add a condition after the queue's waiting point to check if the element belongs to the group of remaining elements and if so, the element shall exit the method. The 'rest' variable has to be set before signaling for it to work as intended.

**Code of main module:**
```python
main():
    shared = Shared()

    run_time = 3
    threads = [Thread(guardian, shared, run_time)]

    while not shared.finished:
        sleep(randint(0, 2)/1000)
        element_type = randint(0, 2)
        if not element_type:
            threads.append(Thread(oxygen, shared))
        else:
            threads.append(Thread(hydrogen, shared))

    sleep(1)
    # taking care of stuck/unbonded threads.
    if shared.hydrogen > 0 or shared.oxygen > 0:
        print(f"---- not boned elements ----\n" +
              f"hydrogen: {shared.hydrogen}, oxygen: {shared.oxygen}")
        shared.rest = True
        shared.hydroQueue.signal(shared.hydrogen)
        shared.oxyQueue.signal(shared.oxygen)

    for t in threads:
        t.join()
```

Note: The sleep() in while cycle serves only for generation purposes. Without it, the element amounts were way outside of a ratio of 2:1.

**The rest condition in hydrogen method**
```python
    ...
    shared.hydroQueue.wait()
    if shared.rest:
        print("H", end='')
        return
    bond("H")
    ...
```
Note: We have also added printouts for verification. 

## Output

The guardian thread lets the while loop run for 3 seconds, but we have set it this time to 1 second for a shorter output. Meanwhile, the threads are generated randomly. We decided that we will set the sleep after the while loop to one second:

```python
main():
    ...
    while not shared.finished:
        ...

    sleep(1)          # <-- this sleep
    
    # taking care of stuck/unbonded threads.
    if shared.hydrogen > 0 or shared.oxygen > 0:
        ...
```
This was decided by experimenting and running the program multiple times. The sleep has to have a duration long enough for all the valid triplets to bond. 

The output of the program:
```
OHH
OHH
OHH
OHH
OHH
OHH
OHH
OHH
OHH
OHH
OHH
OHH
OHH
HHO
HHO
HOH
HOH
HOH
HOH
HOH
HOH
HOH
HHO
HHO
HOH
HHO
HOH
HHO
HOH
HHO
HOH
HHO
HHO
HHO
HHO
---- not boned elements ----
hydrogen: 1, oxygen: 7
HOOOOOOO
```

You can see different arrangements of triples and the leftover elements at the end.
