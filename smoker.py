"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements Cigarette smokers problem and it's solution.
"""

from time import *
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, Event, print


class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatch = Semaphore(0)

        self.numTobacco = 0
        self.numMatch = 0
        self.numPaper = 0

        self.mutex = Mutex()


def agent_1(shared):
    """
    Simulate agent who provides paper and tobacco.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: tobacco, paper --> smoker 'match'")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    """
    Simulate agent who provides paper and match.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: paper, match --> smoker 'tobacco'")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    """
    Simulate agent who provides match and tobacco.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        sleep(randint(0, 10) / 100)
        print("agent: tobacco, match --> smoker 'paper'")
        shared.tobacco.signal()
        shared.match.signal()
