# @Simona735/PPDS-assignments - 03
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
As part of the assignment, it was possible to choose one of two tasks, implement it and experiment with its settings. I chose the **Producer-Consumer problem**.

# Assignment

Implement the solution to the Consumer-Producer problem. Experiment with different system settings. Try to find out experimentally what parameters are optimal for your system. Choose one of two optimality criterion. For experiments, average the values of 10 repetitions of the experiment at the same system settings; plot the graphs for at least 100 different settings of the modelled system.

My choice of optimality criterion was: let the optimality criterion be the number of products produced per unit time (in what relationship are product production time, storage size, number of producers, and number of consumers?)

I take no credit for the problem implementation. Credit for the solution code belongs to Mgr. Ing. Matúš Jókay, PhD.

**Associated file**: [producer-consumer.py](producer-consumer.py)

# Producer–Consumer problem

In computing, the producer-consumer problem is a classic example of a multiprocess synchronization problem. The problem describes two processes, a producer and a consumer, which share a common fixed-size storage/buffer that is used as a queue. 

The producer’s job is to generate data, put it into storage, and start again.
At the same time, the consumer is consuming the data (i.e. removing it from the storage), one piece at a time.

Problem 
Ensure that the producer does not attempt to add data to the storage when it is full and that the consumer does not attempt to remove data from empty storage.

Although I do not take credit for developing the solution, I will give an explanation of it.

Code contains object class for the shared storage - class Shared. It also contains methods for producer and consumer processes and the "producer_consumer" method where these processes are initialized and started.

**Method producer**
``` python
def producer(shared, produce_time):
    """
    The method models the producers process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        produce_time(int): production time in seconds
    """
    while True:
        sleep(produce_time)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        shared.produced += 1
        shared.mutex.unlock()
        shared.items.signal()
```
The method contains an execution loop in which certain actions take place. These actions are in the following order. sleep(produce_time) models the time when the product is produced. Next, shared.free.wait() is used to check for free space in the storage. If the space is free, the execution continues, if not, the thread waits for the necessary capacity to be released. 
The condition that follows ensures that the loop is finite, so if True is written to the "finished" parameter and the thread reaches this part of the loop, it will terminate its operation. 
If the end of the program has not yet occurred, it continues by trying to add the produced item to the shared storage. The mutex is used to ensure the integrity of the repository. After gaining exclusive access to the repository, we will add the product. This process is simulated by incrementing the variable "produced", which in the end is used to evaluate the optimality criterion.
After adding a product to the repository, it is necessary to unlock the mutex and then signal that there is a new item in the repository using shared.items.signal().

**Method consumer**
``` python
def consumer(shared, consume_time):
    """
    The method models the consumer process. Producers create items of
    some kind and add them to a shared data structure (i.e., warehouse).

    Args:
        shared(Shared): shared object representing a warehouse
        consume_time(int): time of consuming in seconds
    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 1000)
        shared.mutex.unlock()
        shared.free.signal()
        sleep(consume_time)
```
The method, like the previous one, contains an execution loop in which certain actions take place. These actions are in the following order. shared.items.wait() is used to check if there are any items in the storage. If the items are there, the execution continues, if not, the thread waits for the producer to add the item to the repository. 
The condition that follows ensures that the loop is finite as it did with the producer, so when True is written to the "finished" parameter and the thread reaches that part of the loop, it will terminate. If the end of the program has not yet occurred, it continues by trying to retrieve the item from the shared storage. 
The mutex is used to ensure the integrity of the repository. After gaining exclusive access to the repository, the product is removed from the repository. This process is simulated by sleep(randint(1, 10) / 1000) - sleeping for a random time in the range 0.001 - 0.01. After removing the product from the storage it is necessary to unlock the mutex and immediately afterward signal that there is one more free slot in the storage with shared.free.signal() 
The actual processing/consumption of the product is simulated by sleep. 

Signaling and waiting for variables "free" and "items" solves the producer-consumer problem - ensure that the producer does not attempt to add data to the storage when it is full and that the consumer does not attempt to remove data from empty storage.

**Method producer_consumer**
``` python
def producer_consumer(produce, process, producers, consumers, size):
    """
    Model the problem of Producers-consumers.

    Args:
        produce(double): production time in seconds
        process(double): processing time in seconds
        producers(int): number of producers
        consumers(int): number of consumers 
        size(int): storage size 
    """
    shared = Shared(size)
    producers = [Thread(producer,
                        shared,
                        produce) for _ in range(producers)]
    consumers = [Thread(consumer,
                        shared,
                        process) for _ in range(consumers)]

    sleep(0.2)
    shared.finished = True
    shared.items.signal(100)
    shared.free.signal(100)
    [t.join() for t in producers + consumers]
    return shared.produced
```
As mentioned, the method initializes the necessary elements and starts the actual execution of the individual methods mentioned above. The program is set to terminate after 0.2 seconds, due to the length of the following experiments. After that, you can see the signaling for "items" and "free". The signaling is used to free the threads to complete the cycle. The method returns the number of all produced items that were added to the storage. The number is later used to compute the optimal criterion value.

# Experiments

The assignment was to experiment with the following parameters:
- product production time,
- product processing time,
- number of consumers,
- number of producers,
- the size of the storage facility (warehouse).

The assignment further states that we should try to experimentally find out what parameters are optimal for your system by choosing an optimality criterion and evaluating the results of the experiments. 
The criterion chosen was the number of products produced per unit time.

## Experiment 01

In the first experiment, we considered the relationship between the number of producers and production time. It is expected that we will get higher values the more consumers we use and also higher values the less production time we choose.

Selected values for experiment:

```python
processing_time = 0.01
consumers_count = 5
storage_size = 5

param1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]                                       # Producers count
param2 = [0.001, 0.002, 0.005, 0.007, 0.01, 0.02, 0.05, 0.07, 0.1, 0.5]        # Production time
```

Resulting chart:

![Experiment 01](images/experiment%201.png?raw=true "Experiment 01")

The values changed exactly as expected. It goes without saying that this increase must end somewhere, because the number of consumers and the size of the storage are constant and therefore the increase in products per second has a certain limit.

Let's slightly change the values to show that the increase stops.

Selected values:

```python
processing_time = 0.01
consumers_count = 5
storage_size = 5

param1 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]                                  # Producers count
param2 = [0.001, 0.002, 0.005, 0.007, 0.01, 0.02, 0.05, 0.07, 0.1, 0.2]        # Production time
```

Resulting chart:

![Experiment 01-2](images/experiment%201-2.png?raw=true "Experiment 01-2")

I have highlighted the increase on line for time value 0.1 and we can see that the increase stops after a certain amount of producers, specifically 10.
Let's set the default producers amount to 10.

## Experiment 02

In the second experiment, we considered the relationship between the number of producers and storage size. 

Selected values for experiment:

```python
production_time = 0.02
processing_time = 0.01
consumers_count = 5

param1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]            # Producers count
param2 = [10, 12, 15, 17, 20, 22, 25, 27, 30, 32]   # Storage size
```
Resulting chart:

![Experiment 02](images/experiment%202.png?raw=true "Experiment 02")

In the graph we observe that with 10 producers and a storage capacity of 20, the growth is maximized. Therefore, let's set the default storage capacity to 20.

## Experiment 03

We have set 2 values, namely the number of producers and the storage size. Let's see what effect this has on other values. Specifically, let's look at the relationship between production time and processing time.

Selected values for experiment:

```python
producers_count = 10
consumers_count = 5
storage_size = 20

param1 = [0.001, 0.002, 0.005, 0.007, 0.01, 0.02, 0.05, 0.07]    # Production time
param2 = [0.001, 0.002, 0.005, 0.007, 0.01, 0.02, 0.05, 0.07]    # Processing time
```
Resulting chart from two views:

![Experiment 03a](images/experiment%203a.png?raw=true "Experiment 03a")
![Experiment 03b](images/experiment%203b.png?raw=true "Experiment 03b")

Personally, I would expect the graph to be symmetrical along its diagonal. 

We can observe that for a production time of 0.05 the total production decreases if the processing time also decreases. One would expect production to increase with decreasing times, as it means faster process overall, but in this case it is the other way around. The conclusion is that the correct ratio of these times is important. If the times are different, the processing time must be at least twice as large. We choose a value of 0.02 for both times.

# Conclusion


Selected optimal parameters:

```python
production_time = 0.02
processing_time = 0.02
producers_count = 10
consumers_count = 5
storage_size = 20
```

The parameters are linked together in such a way that if we increase the number of producers, the number of consumers, or the size of the storage, the number of products produced per second will also increase. If we increase only 2 of these parameters, there will be a limit where the increase stops, because the third parameter will be limiting (see experiment 2). 

If we decrease the production time and the processing time, the number of products produced will increase. We have to decrease the values in the same way or according to the instructions in the conclusion of experiment 3.

If we adjust the time variable and the number variable at the same time, we will again reach a point where we will not achieve further improvement because some of the other parameters will be limiting (see experiment 1).
