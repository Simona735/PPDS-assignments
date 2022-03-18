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


def pusher_tobacco(shared):
    """
    Simulate tobacco pusher. When he receives tobacco, he checks for paper
    and match. He signals to given smoker based on the available supplies.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        order = randint(0, 1)
        if order:
            if shared.numPaper:
                shared.numPaper -= 1
                shared.pusherMatch.signal()
            elif shared.numMatch:
                shared.numMatch -= 1
                shared.pusherPaper.signal()
            else:
                shared.numTobacco += 1
        else:
            if shared.numMatch:
                shared.numMatch -= 1
                shared.pusherPaper.signal()
            elif shared.numPaper:
                shared.numPaper -= 1
                shared.pusherMatch.signal()
            else:
                shared.numTobacco += 1

        shared.mutex.unlock()


def pusher_paper(shared):
    """
    Simulate paper pusher. When he receives paper, he checks for tobacco
    and match. He signals to given smoker based on the available supplies.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        order = randint(0, 1)
        if order:
            if shared.numMatch:
                shared.numMatch -= 1
                shared.pusherTobacco.signal()
            elif shared.numTobacco:
                shared.numTobacco -= 1
                shared.pusherMatch.signal()
            else:
                shared.numPaper += 1
        else:
            if shared.numTobacco:
                shared.numTobacco -= 1
                shared.pusherMatch.signal()
            elif shared.numMatch:
                shared.numMatch -= 1
                shared.pusherTobacco.signal()
            else:
                shared.numPaper += 1
        shared.mutex.unlock()


def pusher_match(shared):
    """
    Simulate match pusher. When he receives match, he checks for tobacco
    and paper. He signals to given smoker based on the available supplies.

    Args:
        shared(Shared): shared object with sync mechanisms.
    """
    while True:
        shared.match.wait()
        shared.mutex.lock()
        order = randint(0, 1)
        if order:
            if shared.numTobacco:
                shared.numTobacco -= 1
                shared.pusherPaper.signal()
            elif shared.numPaper:
                shared.numPaper -= 1
                shared.pusherTobacco.signal()
            else:
                shared.numMatch += 1
        else:
            if shared.numPaper:
                shared.numPaper -= 1
                shared.pusherTobacco.signal()
            elif shared.numTobacco:
                shared.numTobacco -= 1
                shared.pusherPaper.signal()
            else:
                shared.numMatch += 1
        shared.mutex.unlock()


def main():
    shared = Shared()

    pushers = [Thread(pusher_tobacco, shared),
               Thread(pusher_paper, shared),
               Thread(pusher_match, shared)]

    smokers = [Thread(smoker_tobacco, shared),
               Thread(smoker_paper, shared),
               Thread(smoker_match, shared)]

    agents = [Thread(agent_1, shared),
              Thread(agent_2, shared),
              Thread(agent_3, shared)]

    for t in pushers + smokers + agents:
        t.join()


if __name__ == "__main__":
    main()
