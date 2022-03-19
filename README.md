# @Simona735/PPDS-assignments - 04
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
The assignment consists of two individual tasks. Task one was to implement the cigarette smokers problem and solve the problem of favoring smokers. Task two was to write a solution for the Dining savages problem modification which we will describe below.

- [Task 1 - Cigarette smokers problem](#task-1---cigarette-smokers-problem)
- [Task 2 - Dining savages problem](#task-2---dining-savages-problem)

# Task 1 - Cigarette smokers problem

**Associated file**: [smoker.py](smoker.py)

The cigarette smokers problem is a concurrency problem and it was described at the lecture together with the solution. For a reference see [The Little Book of Semaphores](https://greenteapress.com/wp/semaphores/)

Our task was to implement a solution to the problem according to the lecture. For the modification in which the agent does not wait for resource allocation signaling, solve the smoker favoritism problem and describe your solution appropriately in the documentation.

**The smoker favoritism problem:**

Each pusher checks available resources to wake a dedicated smoker. Bud each pusher does this action in a certain order. The favoritism takes place if two pushers are first checking ingredients for the same pusher. Example:

**pusher_tobacco:**
```python
if shared.num_paper:
    shared.num_paper -= 1
    shared.pusher_to_match_smoker.signal()    # <-- match smoker
elif shared.num_match:
    shared.num_match -= 1
    shared.pusher_to_paper_smoker.signal()
else:
    shared.num_tobacco += 1
```

**pusher_paper:**
```python
if shared.num_tobacco:
    shared.num_tobacco -= 1
    shared.pusher_to_match_smoker.signal()    # <-- match smoker
elif shared.num_match:
    shared.num_match -= 1
    shared.pusher_to_tobacco_smoker.signal()
else:
    shared.num_paper += 1
```

Both paper pusher and tobacco pusher are mainly asking for match smoker, so it is clear that he will be preferred most. So if we do in a way, that the asking frequency will be equally distributed then the problem will be solved. To properly ensure this, we have to ensure that the agent distribution will be in a similar way.

**pusher_tobacco:**
```python
if shared.num_paper:
    shared.num_paper -= 1
    shared.pusher_to_match_smoker.signal()    # <-- match smoker
elif shared.num_match:
    shared.num_match -= 1
    shared.pusher_to_paper_smoker.signal()    # <-- paper smoker
else:
    shared.num_tobacco += 1
```

**pusher_paper:**
```python
if shared.num_tobacco:
    shared.num_tobacco -= 1
    shared.pusher_to_match_smoker.signal()    # <-- match smoker
elif shared.num_match:
    shared.num_match -= 1
    shared.pusher_to_tobacco_smoker.signal()  # <-- tobacoo smoker
else:
    shared.num_paper += 1
```

**pusher_match:**
```python
if shared.num_tobacco:
    shared.num_tobacco -= 1
    shared.pusher_to_paper_smoker.signal()    # <-- paper smoker
elif shared.num_paper:
    shared.num_paper -= 1
    shared.pusher_to_tobacco_smoker.signal()  # <-- tobacoo smoker
else:
    shared.num_match += 1
```

**agent_1:**
```python
print("agent: tobacco, paper --> smoker 'match'")
shared.tobacco.signal()
shared.paper.signal()
```

**agent_2:**
```python
print("agent: paper, match --> smoker 'tobacco'")
shared.paper.signal()
shared.match.signal()
```

**agent_3:**
```python
print("agent: match, tobacco --> smoker 'paper'")
shared.match.signal()
shared.tobacco.signal()
```

This will solve the problem. To prove that the solution is correct, we performed an experiment, we have let the program run for a while and counted which smoker has smoked how many times.

**Experiment results:**
1406 smokers managed to smoke in total. 

| Smoker | count | 
| ------ | ----- | 
|  match |  473  |  
|  paper |  466  |  
|  tobacco |  467  | 

There is a small difference. It is not big enough to say that any smoker is favored. So we can say that we solved the problem.


# Task 2 - Dining savages problem

**Associated file**: [savages.py](savages.py)

Implement a program that solves the modified synchronization problem of Dinning Savages.

There are several cooks in a tribe. When a savage discovers that the pot is empty, he wakes up ALL the cooks, who can help each other in cooking and cook together. JUST ONE cook tells the waiting savage that it is done. The cook puts the portions in the pot, not the savage!

Appropriately model the problem according to the following **requirements**:

- Find out what combination of synchronization problems are involved,
- write pseudocode for the solution,
- place appropriate statements to verify the model's functionality,
- choose appropriate characteristics on which to base the model (numbers of threads, timings of activities, values of other variables).

## Analysis:
Let it be understood that the original solution was explained at the lecture, and therefore we will not repeat the explanation. If necessary, I am adding a link to the [lecture](https://www.youtube.com/watch?v=iotYZJzxKf4&t=3996s).  

Let's move to the modification analysis. Modification requirements are:
1. There are several cooks in the tribe. 
2. When the savage discovers that the pot is empty, he wakes up ALL the cooks.
3. Cooks can help each other in cooking and cook together. 
4. JUST ONE cook tells the waiting savage that it is done. 
5. The cook puts the portions in the pot, not the savage!

To fulfill the first requirement, we add a list of cooks/threads to the program.
```python
cooks = [Thread(cook, shared, i) for i in range(COOKS)]
```

To meet the second requirement, we have to signal to ALL the cooks. This means we have to modify the savage method:

```python
shared.barrier2.wait(last=f"savage {i}: all of us are here, let's have dinner")
shared.mutex.lock()
print(f"savage {i}: num of servings in pot is {shared.servings}")
if shared.servings == 0:
    print(f"savage {i}: wakes all cooks")
    shared.empty_pot.signal(COOKS)    # <-- modify this part, from signal() to signal(COOKS)
    shared.full_pot.wait()
get_serving_from_pot(shared, i)
shared.mutex.unlock()
eat(i)
shared.barrier1.wait(last=" ")
```

The second requirement was fulfilled. Let's move to the third one which is that the cooks can help each other in cooking and cook together. Well, there are no further details stated, so we can basically let each of them cook for a certain time concurrently and then declare that all the food is done. This doesn't require any modifications.

Requirement number 4 says that JUST ONE cook tells the waiting savage that it is done. The ONE cook is the last one obviously because all the cooking has to be already done. We need a mechanism to tell which cook is the last one. 

We also need to make sure that there will be no overtaking. As mentioned, the empty_pot signalization will be made for all threads. Semaphore alone only ensures that N cooks will be let in, it doesn't make difference between the case where each cook will be let in once and the second case where one cook will be let in 5 times.

These two things can be achieved with the use of barrier. The barrier captures the case when the thread is last. By modifying the barrier wait function, we can achieve that we return a bool value whether the passing thread was last or not.

**Barrier wait modification:**
```python
def wait(self, each=None, last=None):
    self.mutex.lock()
    if each:
        print(each)
    self.count += 1
    is_last = False     # <-- inital value for every thread
    if self.count == self.threads_num:
        if last:
            print(last)
        self.count = 0
        is_last = True    # <-- change the value to true if it is last thread
        self.barrier.signal(self.threads_num)
    self.mutex.unlock()
    self.barrier.wait()
    return is_last    # return value.
```

Now we need to place the barrier in a correct position and execute the actions of the last thread. 

```python
while True:
    shared.empty_pot.wait()

    print(f"cook {i}: cooking")
    sleep(randint(50, 80) / 100)

    is_last = shared.barrier3.wait()    
    if is_last:
        put_servings_in_pot(shared, i)
        shared.full_pot.signal()
```

Why did we choose this placement? We have to perform the cooking and determine the last cook. This means that the barrier has to be placed between cooking and serving the pot. Based on the return value of the barrier, the last cook adds portions to the pot and signals that the pot is full. Barrier also ensures that there will be no overtaking because all the cooks have to cook their part before continuing. We have thus fulfilled conditions 4 and 5.

## Pseudocode:

This is the pseudocode for the solution.

```python
cook(shared, i):
    while True:
        wait_until_pot_is_empty()
        cook()
        is_last = barrier3.wait_for_all_cooks()
        if is_last:
            put_all_servings_to_pot()
            signal_pot_is_full()


savage(shared, i):
    random_reshuffle_savages()

    while True:
        barrier1.wait_for_all_savages()
        mutex.lock()
        if left_servings == 0:
            signal_empty_pot_to_all_cooks()
            wait_until_pot_is_full()
        get_serving_from_pot()
        mutex.unlock()
        eat()
        barrier2.wait_for_all_savages()


main():
    shared = Shared()

    savages = create_and_run_thread_for_each_savage()
    cooks = create_and_run_thread_for_each_cook()
    join_threads()
```

## Printouts:
Printouts will be displayed for 8 servings, 3 savages, and 5 cooks.

```
savage 1: all of us are here, let's have dinner
savage 1: num of servings in pot is 0
savage 1: wakes all cooks
cook 2: cooking
cook 3: cooking
cook 4: cooking
cook 0: cooking
cook 1: cooking
cook 3: all cooked, servings to pot
savage 1: takes from pot, portions left: 7
savage 1: feasting
savage 0: num of servings in pot is 7
savage 0: takes from pot, portions left: 6
savage 0: feasting
savage 2: num of servings in pot is 6
savage 2: takes from pot, portions left: 5
savage 2: feasting
 
savage 1: all of us are here, let's have dinner
savage 1: num of servings in pot is 5
savage 1: takes from pot, portions left: 4
savage 1: feasting
savage 0: num of servings in pot is 4
savage 0: takes from pot, portions left: 3
savage 0: feasting
savage 2: num of servings in pot is 3
savage 2: takes from pot, portions left: 2
savage 2: feasting
 
savage 1: all of us are here, let's have dinner
savage 1: num of servings in pot is 2
savage 1: takes from pot, portions left: 1
savage 1: feasting
savage 2: num of servings in pot is 1
savage 2: takes from pot, portions left: 0
savage 2: feasting
savage 0: num of servings in pot is 0
savage 0: wakes all cooks
cook 3: cooking
cook 0: cooking
cook 4: cooking
cook 2: cooking
cook 1: cooking
cook 2: all cooked, servings to pot
savage 0: takes from pot, portions left: 7
savage 0: feasting
 
savage 2: all of us are here, let's have dinner
savage 2: num of servings in pot is 7
savage 2: takes from pot, portions left: 6
savage 2: feasting
savage 1: num of servings in pot is 6
savage 1: takes from pot, portions left: 5
savage 1: feasting
savage 0: num of servings in pot is 5
savage 0: takes from pot, portions left: 4
savage 0: feasting
 
savage 1: all of us are here, let's have dinner
savage 1: num of servings in pot is 4
savage 1: takes from pot, portions left: 3
savage 1: feasting
savage 2: num of servings in pot is 3
savage 2: takes from pot, portions left: 2
savage 2: feasting
savage 0: num of servings in pot is 2
savage 0: takes from pot, portions left: 1
savage 0: feasting
 
savage 2: all of us are here, let's have dinner
savage 2: num of servings in pot is 1
savage 2: takes from pot, portions left: 0
savage 2: feasting
savage 0: num of servings in pot is 0
savage 0: wakes all cooks
cook 1: cooking
cook 3: cooking
cook 0: cooking
cook 4: cooking
cook 2: cooking
cook 2: all cooked, servings to pot
savage 0: takes from pot, portions left: 7
savage 0: feasting
savage 1: num of servings in pot is 7
savage 1: takes from pot, portions left: 6
savage 1: feasting
```

As you can see, the solution is correct and it meets all the requirements of the modification.

