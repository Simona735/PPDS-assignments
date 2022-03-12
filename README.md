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





