# @Simona735/PPDS-assignments - 07
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/npm/l/@tandil/diffparse?color=%23007ec6)](https://github.com/Simona735/PPDS-assignments/blob/main/LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-blue.svg)](https://conventionalcommits.org)

# About
Simple python application demonstrating the use of generators. 

# Assignment

Write an application that will use N (N>2) coprograms (using extended generators) and use a custom scheduler to alternate between them.

# Solution

We have decided to create 3 generators with different purposes and a custom Scheduler with it's own functionality.

## Generators

**Generator 1:**

Purpose of first generator is to generate a random number in range given by arguments and send it back to the caller. It also prints the number for easier behaviour observations.

```python
def generate_random(from_val, to_val):
    try:
        value = 0
        while True:
            value = yield value
            value = randint(from_val, to_val)
            print(f'New value {value}')
    except GeneratorExit:
        print(f'increment_by_random closed')
```

**Generator 2:**

Second generator computed a squared value of a given number. The number is being yieled (sent) to the generator by a our scheduler object. It also yields the result back to the sender and prints result on the output.

```python
def squared():
    try:
        square = 0
        while True:
            number = yield square
            square = number * number
            print(f'Squared value: {square} = {number} * {number}')
    except GeneratorExit:
        print(f'squared closed')
```

**Generator 3:**

The last generator is used to compute and store a sum of given numbers until certail limit given as a parameter to the function. The sum value is yielded back to the sender every iteration. When the limit is reached, the while loop terminates and raises StopIteration exception. 

```python
def values_sum(limit):
    try:
        total_sum = 0
        while True:
            total_sum += yield total_sum
            print(f'Total sum {total_sum}')
            if total_sum > limit:
                break
    except GeneratorExit:
        print(f'values_sum closed')
```

## Scheduler

Our custom scheduler object is used to store generator objects in a list. The object implements a method new() which is used to add a new generator to the list. It also implements a method loop() which is used to loop over the generators. We have added a slight delay of ```sleep(0.2)``` to properly observe the printouts.
The loop method also closes the generator when it rises StopIteration exception and removed the generator from the list.

Source of [inspiration](https://stackoverflow.com/questions/43162825/infinite-loop-and-rotation-of-array) 

```python
class Scheduler(object):
    def __init__(self):
        self.tasks = []
        self.index = 0

    def new(self, task):
        next(task)
        self.tasks.append(task)

    def loop(self):
        value = 0
        while len(self.tasks):
            try:
                task = self.tasks[self.index % len(self.tasks)]
                value = task.send(value)
                sleep(0.2)
                self.index += 1
            except StopIteration:
                task = self.tasks[self.index % len(self.tasks)]
                self.index = self.index % len(self.tasks)
                self.tasks.remove(task)
                task.close()
                print("Generator closed")
```

## Output

There are multiple prints in our code to properly observe the behaviour of our generators. We have initializes the code as follows:

```python
scheduler = Scheduler()
scheduler.new(generate_random(10, 500))
scheduler.new(squared())
scheduler.new(values_sum(500000))
scheduler.loop()
```

And we have run the code and copied the output.

```
New value 394
Squared value: 155236 = 394 * 394
Total sum 155236
New value 340
Squared value: 115600 = 340 * 340
Total sum 270836
New value 445
Squared value: 198025 = 445 * 445
Total sum 468861
New value 274
Squared value: 75076 = 274 * 274
Total sum 543937
Generator closed       //<--- generator closed
New value 123
Squared value: 15129 = 123 * 123
New value 105
Squared value: 11025 = 105 * 105
New value 196
Squared value: 38416 = 196 * 196
New value 409
Squared value: 167281 = 409 * 409
New value 269
Squared value: 72361 = 269 * 269
...
```

As you can see, the generators took turns in carrying out their operations. You can also see when the third generator reached it's limit and got closed. 
