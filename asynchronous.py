"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements a simple example of asynchronous coroutine.
"""


import time
import asyncio


async def sleep():
    """
    Asynchronous sleep method that puts the program to sleep for
    one second.
    """
    await asyncio.sleep(1)


async def squared(name, start, work_queue):
    """
    Method computes squared value for each item from work_queue.
    The computing is done asynchronously and is simulated by sleep
    method. Method also contains multiple verification printouts.

    Args:
        name(string): task name
        start(float): program start time
        work_queue(asyncio.Queue): queue containing all numbers to process
    """
    while not work_queue.empty():
        number = await work_queue.get()
        print(f'Task {name}: Computing {number}*{number}')
        await sleep()
        elapsed = time.perf_counter() - start
        print(f'Task {name}: Result is {number * number}')
        print(f"Task {name}: Elapsed time: {elapsed:.1f}")


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
