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

        self.pusher_to_tobacco_smoker = Semaphore(0)
        self.pusher_to_paper_smoker = Semaphore(0)
        self.pusher_to_match_smoker = Semaphore(0)

        self.num_tobacco = 0
        self.num_match = 0
        self.num_paper = 0

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
        shared.pusher_to_tobacco_smoker.wait()
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
        shared.pusher_to_paper_smoker.wait()
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
        shared.pusher_to_match_smoker.wait()
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
        shared.match.signal()
        shared.tobacco.signal()


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
        if shared.num_paper:
            shared.num_paper -= 1
            shared.pusher_to_match_smoker.signal()
        elif shared.num_match:
            shared.num_match -= 1
            shared.pusher_to_paper_smoker.signal()
        else:
            shared.num_tobacco += 1
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
        if shared.num_match:
            shared.num_match -= 1
            shared.pusher_to_tobacco_smoker.signal()
        elif shared.num_tobacco:
            shared.num_tobacco -= 1
            shared.pusher_to_match_smoker.signal()
        else:
            shared.num_paper += 1
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
        if shared.num_tobacco:
            shared.num_tobacco -= 1
            shared.pusher_to_paper_smoker.signal()
        elif shared.num_paper:
            shared.num_paper -= 1
            shared.pusher_to_tobacco_smoker.signal()
        else:
            shared.num_match += 1
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
