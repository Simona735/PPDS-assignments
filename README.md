# @Simona735/PPDS-assignments - 04
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
The assignment consists of two individual tasks. Task one was to implement The Dining Philosophers Problem and its solution by using right-handed and left-handed philosophers. Task two was to write a pseudocode solution for a given assignment which we will describe below.

- [Task 1 - The Dining Philosophers Problem](#task-1---the-dining-philosophers-problem)
- [Task 2 - The Nuclear Power Plant](#task-2---the-nuclear-power-plant)

# Task 1 - The Dining Philosophers Problem

**Associated file**: [philosophers.py](philosophers.py)

A solution using a footman was presented at the seminar, and our task is to implement a solution using right-handed and left-handed philosophers.

**The Dining Philosophers Problem:**

The dining philosopher's problem is the classical problem of synchronization which says that five philosophers are sitting around a circular table and their job is to think and eat alternatively. 

There are five forks on the table, one on each side of each philosopher. To eat a philosopher needs two forks. 
A philosopher can only eat if both immediate left and right fork is available. In case both forks are not available then the philosopher waits until they are. 

**Assignment conditions:**

1. Only one philosopher can hold the fork at a time.
2. There must be no deadlock (i.e. no philosopher eats),
3. It must not happen that any of the philosophers does not eat.
4. And finally, the solution must allow multiple philosophers to eat at the same time.

The task was to implement a solution in which right-handed and left-handed people are randomly selected. The idea is for philosophers to take forks in different orders.  So someone will take the right fork first and then the left, or vice versa. A right-handed person always takes the right fork first and a left-handed person always takes the left as his first fork.

**Solution explanation:**

We proceeded by first implementing the solution from the lecture. Then we added a function to randomly generate right and left-handers. We added right-handers and left-handers to the existing solution. Then we removed the use of a footman and modified the printouts to test our solution.

**Random generation:**

```python
philosopher_hands = [0, 1]

for x in range(PHIL_NUM - 2):
    philosopher_hands.append(choice([0, 1]))
shuffle(philosopher_hands)

return philosopher_hands
```

We have created the generation of right and left-handers by creating a list, in which we write zeros or ones. Each element of the list represents a philosopher, and the value at that index indicates whether the philosopher is left-handed or right-handed. 
0 means left-handed.
1 means right-handed.

Condition 2 states that we must prevent deadlock. To meet this condition we need at least one right-handed person and at least one left-handed person. Therefore, we initialize the list to the values 0 and 1. Then we randomly generate ones and zeros to determine the main hand for each philosopher. And if we want to achieve truly random generation, we rearrange the list randomly.

The solution was taken from StackOverflow [article](https://stackoverflow.com/questions/48572819/random-choice-from-list-at-least-once).

After that, we continue to the main philosopher's code.

```python
sleep(randint(40, 100) / 1000)

if main_hand:
    first_fork = philosopher_id
    second_fork = (philosopher_id + 1) % PHIL_NUM
else:
    second_fork = philosopher_id
    first_fork = (philosopher_id + 1) % PHIL_NUM

while True:
    think(philosopher_id)
    get_forks(forks, philosopher_id, first_fork, second_fork)
    eat(philosopher_id)
    put_forks(forks, philosopher_id, first_fork, second_fork)
```

The condition and the beginning assigns the first and second taken fork considering whether the person is right or left-handed. These values are then passed to the functions get_fork and put_fork. Let's take a look at them.

```python
def get_forks(forks, philosopher_id, first, second):
    print(f'{philosopher_id:02d}: try to get forks')
    forks[first].wait()
    print(f'{philosopher_id:02d}: first fork taken - {first}')
    forks[second].wait()
    print(f'{philosopher_id:02d}: second fork taken - {second}')
```

```python
def put_forks(forks, philosopher_id, first, second):
    forks[first].signal()
    print(f'{philosopher_id:02d}: first fork put down - {first}')
    forks[second].signal()
    print(f'{philosopher_id:02d}: second fork put down - {second}')
```

The semaphores representing forks are initialized to 1 at the beginning. It says that the fork is free to be taken. So the first thread that attempts to take the fork is able to do that. Other threads have to wait until the philosopher puts it down and signals free fork in put_fork function. I have added outputs to see which fork was taken or put down. This is because the philosopher puts the forks down one at a time. So if philosopher 1 wants philosopher 2's first fork, he doesn't have to wait for philosopher 2 to put down both forks, but only fork number 1. And the outputs are here to test that fact.

**Output:**

```
01: thinking
00: thinking
04: thinking
03: thinking
02: thinking
01: try to get forks
00: try to get forks
04: try to get forks
03: try to get forks
03: first fork taken - 3
01: first fork taken - 1
01: second fork taken - 2
01: eating                      // 01 is eating 
04: first fork taken - 4
04: second fork taken - 0
04: eating                      // 04 is eating 
02: try to get forks
01: first fork put down - 1
01: second fork put down - 2
01: thinking
04: first fork put down - 4     // < -- 04 first fork put down
03: second fork taken - 4       // < -- 03 second fork taken
03: eating                      // 03 is eating 
04: second fork put down - 0    // < -- 04 second fork put down
04: thinking
01: try to get forks
00: first fork taken - 1
00: second fork taken - 0
00: eating                      // 00 is eating 
03: first fork put down - 3
03: second fork put down - 4
03: thinking
04: try to get forks
04: first fork taken - 4
01: first fork taken - 1
02: first fork taken - 3
00: first fork put down - 1
00: second fork put down - 0
00: thinking
01: second fork taken - 2
01: eating
03: try to get forks
04: second fork taken - 0
04: eating
00: try to get forks
00: first fork taken - 1
01: first fork put down - 1
01: second fork put down - 2
01: thinking
02: second fork taken - 2
02: eating                       // 02 is eating 
04: first fork put down - 4
04: second fork put down - 0
04: thinking
 ...
```

I have highlighted important things by adding comments. As you can see, all philosophers managed to eat - we fulfilled condition no. 3. I have let the code run for a while and there was no deadlock (condition no. 2). Condition no. 4 - you can see at the beginning that the philosophers number 1 and 4 are eating at the same time. And I have also highlighted the case when one philosopher can eat before another puts away both of his forks.

# Task 2 - The Nuclear Power Plant

In a nuclear power plant they have 3 sensors:

1. one primary circuit coolant flow sensor (sensor P)
2. one primary coolant temperature sensor (sensor T)
3. one control rod insertion depth sensor (sensor H)

These sensors are constantly trying to update the measured values. They store the data in a common data storage. Each sensor has a dedicated space in the data storage (take this into account when synchronizing). The sensors perform an update every 50-60 ms. The data update itself takes 10-20 ms for sensor P and sensor T, but 20-25 ms for sensor H.

In addition to the sensors, they have eight operators in that plant who are each constantly looking at their monitor where the sensor readings are displayed. The request for data updates is sent by the monitor constantly and continuously in a cycle. One update takes 40-50 ms. Monitors can only start working when all sensors have already delivered valid data to the storage.

**Subtasks:**
1. Analyze what types of synchronization tasks (or modifications or combinations thereof) are involved in this task.
2. Exactly map the synchronization tasks (primitives) you have chosen to each part of the task.
3. Write pseudocode to solve the problem.
4. Write a program that will appropriately model this synchronization problem.
5. Printouts:
    1. Place information in the format: 'cidlo "%02d": number_of_writing_cycles=%02d, write_duration=%03d\n' before simulating the data update.
    2. When reading data, place information in the format: 'monit "%02d": number of_reading_monitors=%02d, reading_duration=%03d\n'

### Analysis and synchronization mapping:

The task is dealing with the mutual exclusion of process categories. Sensors are one category and monitors are the second category. Each sensor has its dedicated storage space so there is no need to deal with rewriting data and sensors can write data in parallel.

As we said, monitors and sensors are two different categories, so there will be a different code for both of them. However, each of them will have some common characteristics. For example, monitors and sensors perform their activity in an infinite cycle.  

As there was not specified otherwise, we assume that actions dealing with synchronization have no delay - 0 time. 
Sensors are instructed to perform an update every 50 to 60 ms, so it means we have to make a delay at the beginning (or the end) of the cycle. For sensors, we have to differentiate between sensor types - P, T, and H - because sensor type H makes an update for 20-25 ms and types P and T only take 10-20 ms. We have 3 sensors, one of each type, so let's say that sensor with id 0 will be type H. We have to add a condition to generate the data update time. 

```python
if sensor_id == 0:
    # sensor 0 is sensor type H
    writing_duration = random(50 to 25 ms)
else:
    # sensors P and T
    writing_duration = random(10 to 20 ms)
```

Data writing can be simulated by sleep of the given time. 

When it comes to monitors, they work all the time in a cycle without a delay. There are no monitor types so we don't have to differentiate between them. Reading action will be again simulated by sleep in a time interval of 40 - 50 ms. And because the monitors are constantly working, we need the sensors to interrupt their activity. Sensors are active in intervals of 50-60 ms, so it is alright. 

Here comes the mutual exclusion of process categories. During concurrent execution of processes (monitors and sensors), processes need to enter the critical section (accessing data for read or write) at times for execution. More or less said - no two processes can exist in the critical section at any given point of time. So it is either monitors or sensors. To achieve this, we can use Lightswitch as a means to lock a critical section - access data. This applies to both categories. Each will have its own ADT lightswitch (monitor_lightswitch and sensor_lightswitch) and reference to a common access_data object. The object will be represented by a semaphore so that it can be locked. It will be initialized to 1 because the access data is free at the beginning. 

Now we need to make sure that no process will occupy the resource for eternity. Here is how we do that. Monitors are always working as we said before, so let them work. Sensors are updating data in intervals and that is the perfect opportunity to interrupt the monitor's activity because monitors can read data when sensors are waiting for the next cycle. This means that all processes will get to access data and there will be no starvation. How do we achieve this interruption? The answer is a turnstile. 
The turnstile ensures that the threads will pass through and they will pass it one by one. And when the sensor thread passes the turnstile, it will try to lock the room for the sensors category. When the sensor is in the turnstile, waiting for the access_data resource, no other thread (monitor, or sensor) can pass the turnstile. It means that the resource will be free eventually and the next process to get access to it is the sensor. 

One turnstile has to be implemented for both process:

```python
turnstile.wait()
turnstile.signal()
```

But only sensors can interrupt the resource occupation this way, which means, we have to put the resource locking in the turnstile area for the sensor process:

```python
turnstile.wait()
waiting_sensors = sensor_lightswitch.lock(access_data)
turnstile.signal()
```

Of course, each process has to signal that it finished its update by *lightswitch.unlock(access_data)*.

All requirements are fulfilled except that the monitors should start their activity only when each sensor writes at least one value. This means that there has to be some kind of signalization for updating data successfully. The signalization has to be done for each sensor. We can use a simple Event object for this, but each sensor has to have its Event object. This means we create a list of these events and every time the sensor updates data, it signals that the data is valid - ```valid_data[i].signal()```.

Monitors have to check this signaling before starting the infinite cycle. Each sensor's data has to be checked so we add a for loop to wait for initial data to be added.

```python
for i in range(SENSORS):
    valid_data[i].wait()
```

### Pseudocode:

``` python
monitor(monitor_id, access_data, turnstile, monitor_lightswitch, valid_data):
    # checking if every sensor wrote any data
    for every sensor:
        valid_data[sensor].wait()

    while True:
        # go one by one over turnstile
        turnstile.wait()
        turnstile.signal()
        waiting_monitors = monitor_lightswitch.lock(access_data)
        
        reading_duration = random(40 to 50 ms)
        print('monitor: {monitor_id}: 'waiting monitors={waiting_monitors}, reading duration={reading_duration}')
              
        # simulate reading with sleep 
        sleep(reading_duration)
        monitor_lightswitch.unlock(access_data)


sensor(sensor_id, access_data, turnstile, sensor_lightswitch, valid_data):
    while True:
        # wait 50 to 60 ms to start another update
        sleep(50 to 60 ms)
        
        # block turnstile to block monitors
        turnstile.wait()
        # get storage access
        waiting_sensors = sensor_lightswitch.lock(access_data)
        turnstile.signal()

        if sensor_id == 0:
            # sensor 0 is sensor type H
            writing_duration = random(50 to 25 ms)
        else:
            # sensors P and T
            writing_duration = random(10 to 20 ms)
        print('sensor {sensor_id}: waiting sensors={waiting_sensors}, writing duration={writing_duration}')
        
        # simulate writing with sleep
        sleep(writing_duration)
        valid_data[sensor_id].signal()
        sensor_lightswitch.unlock(access_data)


init():
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    monitor_lightswitch = Lightswitch()
    sensor_lightswitch = Lightswitch()
    valid_data = list of Events for every sensor

    for every monitor:
        # create thread and run function monitor()
        Thread(monitor, monitor_id, access_data, turnstile, monitor_lightswitch, valid_data)
    for every sensor:
        # create thread and run function sensor()
        Thread(sensor, sensor_id, access_data, turnstile, sensor_lightswitch, valid_data)
```

### Program:

We have added some comments in pseudocode but we will explain some parts more thoroughly. Let's start with **sensors**:

```python
while True:
    sleep(randint(50, 60) / 1000)

    turnstile.wait()
    waiting_sensors = sensor_lightswitch.lock(access_data)
    turnstile.signal()

    if not sensor_id:
        writing_duration = randint(20, 25) / 1000
    else:
        writing_duration = randint(10, 20) / 1000
    print(f'sensor {sensor_id:02d}: ' +
          f'waiting sensors={waiting_sensors:02d}, ' +
          f'writing duration={writing_duration:.3f}')
    sleep(writing_duration)
    valid_data[sensor_id].signal()
    sensor_lightswitch.unlock(access_data)
```

If condition serves to determine the sensor type. As stated in the assignment, one sensor is type H and its update takes 20 - 25 ms.
After the update itself, we signalize to valid_data that the given sensor updated the value.

Let's take a look at **monitors**:

```python
    for i in range(SENSORS):
        valid_data[i].wait()

    while True:
        turnstile.wait()
        turnstile.signal()
        waiting_monitors = monitor_lightswitch.lock(access_data)

        reading_duration = randint(40, 50) / 1000
        print(f'monitor: {monitor_id:02d}: ' +
              f'waiting monitors={waiting_monitors:02d}, ' +
              f'reading duration={reading_duration:.3f}')
        sleep(reading_duration)
        monitor_lightswitch.unlock(access_data)
```

There is a for loop at the beginning. It is there to check if all sensors provided at least one valid data. If so, the monitors can start its activity.
They are taking turns with turnstile until the sensors block them. After that, reading is simulated by sleep.

### Printouts:
```
sensor 02: waiting sensors=00, writing duration=0.015
sensor 00: waiting sensors=01, writing duration=0.023
sensor 01: waiting sensors=02, writing duration=0.010
monitor: 00: waiting monitors=00, reading duration=0.042
monitor: 01: waiting monitors=01, reading duration=0.043
monitor: 02: waiting monitors=02, reading duration=0.044
monitor: 04: waiting monitors=03, reading duration=0.049
monitor: 03: waiting monitors=04, reading duration=0.040
monitor: 05: waiting monitors=05, reading duration=0.040
monitor: 06: waiting monitors=06, reading duration=0.043
monitor: 07: waiting monitors=07, reading duration=0.050
sensor 01: waiting sensors=00, writing duration=0.013
sensor 00: waiting sensors=01, writing duration=0.020
sensor 02: waiting sensors=02, writing duration=0.012
monitor: 07: waiting monitors=00, reading duration=0.042
monitor: 05: waiting monitors=01, reading duration=0.049
monitor: 03: waiting monitors=02, reading duration=0.045
monitor: 02: waiting monitors=03, reading duration=0.044
monitor: 04: waiting monitors=04, reading duration=0.044
monitor: 06: waiting monitors=05, reading duration=0.050
monitor: 01: waiting monitors=06, reading duration=0.044
monitor: 00: waiting monitors=07, reading duration=0.041
sensor 01: waiting sensors=00, writing duration=0.010
sensor 02: waiting sensors=01, writing duration=0.014
sensor 00: waiting sensors=02, writing duration=0.022
monitor: 00: waiting monitors=00, reading duration=0.044
monitor: 01: waiting monitors=01, reading duration=0.040
monitor: 03: waiting monitors=02, reading duration=0.041
monitor: 07: waiting monitors=03, reading duration=0.049
monitor: 06: waiting monitors=04, reading duration=0.041
monitor: 02: waiting monitors=05, reading duration=0.043
monitor: 04: waiting monitors=06, reading duration=0.045
monitor: 05: waiting monitors=07, reading duration=0.042
sensor 01: waiting sensors=00, writing duration=0.020
sensor 00: waiting sensors=01, writing duration=0.020
sensor 02: waiting sensors=02, writing duration=0.017
monitor: 04: waiting monitors=00, reading duration=0.044
monitor: 03: waiting monitors=01, reading duration=0.042
monitor: 06: waiting monitors=02, reading duration=0.047
monitor: 05: waiting monitors=03, reading duration=0.045
monitor: 02: waiting monitors=04, reading duration=0.047
...
```

As you can see, the monitors and sensors are taking turns in writing and reading. 



