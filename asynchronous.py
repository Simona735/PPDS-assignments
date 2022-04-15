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


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())
