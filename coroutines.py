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


def main():
    pass


if __name__ == "__main__":
    main()
