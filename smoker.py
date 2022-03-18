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


def make_cigarette(name):
    """
    Simulate cigarette making by sleep.

    Args:
        name(str): smoker name
    """
    print(f"smoker '{name}' makes cigarette")
    sleep(randint(0, 10) / 100)


def smoke():
    """
    Simulate smoking by sleep.
    """
    sleep(randint(0, 10) / 100)


def smoker_tobacco(shared):
    """
    Simulate smoker with infinite tobacco supplies.
    Smoker waits for pusher to provide paper and match,
    then makes a cigarette and smokes it.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        smoke()


def smoker_paper(shared):
    """
    Simulate smoker with infinite paper supplies.
    Smoker waits for pusher to provide tobacco and match,
    then makes a cigarette and smokes it.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        smoke()


def smoker_match(shared):
    """
    Simulate smoker with infinite match supplies.
    Smoker waits for pusher to provide paper and tobacco,
    then makes a cigarette and smokes it.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        smoke()


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
