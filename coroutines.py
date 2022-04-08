"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements an example of 3 generators and a scheduler.
"""


from random import randint
from time import sleep


class Scheduler(object):
    """
    Scheduler object. It is used to add generators to Scheduler object
    and loop over them infinitely. It also closes the generator when it
    raises StopIteration exception.
    """
    def __init__(self):
        """
        Initialize a Scheduler with a list and index set on 0.
        """
        self.tasks = []
        self.index = 0

    def new(self, task):
        """
        Add new task to Scheduler.

        Args:
            task(Generator): generator to be added to Scheduler.
        """
        next(task)
        self.tasks.append(task)

    def loop(self):
        """
        Loop infinitely over the generators in the 'tasks' list.
        Close a generator when it raises StopIteration exception.
        """
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


def generate_random(from_val, to_val):
    """
    Purpose of this generator is to generate a random number in range given
    by arguments.

    Args:
        from_val(int): bottom range for generating
        to_val(int): top range for generating
        
    Yields:
        int: new generated number in range 10-500
    """
    try:
        value = 0
        while True:
            value = yield value
            value = randint(from_val, to_val)
            print(f'New value {value}')
    except GeneratorExit:
        print(f'increment_by_random closed')


def squared():
    """
    Purpose of this generator is computing squared value of input number.

    Yields:
        int: total sum so far
    """
    try:
        square = 0
        while True:
            number = yield square
            square = number * number
            print(f'Squared value: {square} = {number} * {number}')
    except GeneratorExit:
        print(f'squared closed')


def main():
    pass


if __name__ == "__main__":
    main()
