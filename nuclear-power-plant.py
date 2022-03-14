"""
Copyright 2022 Simona Richterova.
Licensed to MIT https://spdx.org/licenses/MIT.html

This module implements various synchronization mechanisms.
You can find the complete description in a README.md file - Task 2.
"""


from time import *
from random import randint, choice, shuffle
from fei.ppds import Thread, Semaphore, Mutex, Event, print


MONITORS = 8
SENSORS = 3


class Lightswitch:
    """
    Lightswitch object. Synchronization object that implements
    two methods - lock and unlock.
    """

    def __init__(self):
        """ Initialize Lightswitch. """
        self.counter = 0
        self.mutex = Mutex()

    def lock(self, semaphore):
        """
        The lock() function works on the principle that the first thread
        to use the resource calls wait() on the semaphore to signal
        that the resource is occupied (i.e., locked).
        
        Args:
            semaphore(Semaphore): semaphore object
            
        Returns:
            int: number of objects using resource
        """
        self.mutex.lock()
        counter = self.counter
        if not self.counter:
            semaphore.wait()
        self.counter += 1
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        """
        The unlock() function works on the principle that the last thread
        to leave the resource calls signal() on the semaphore to signal
        that the resource is free (i.e., unlocked).
        
        Args:
            semaphore(Semaphore): semaphore object
        """
        self.mutex.lock()
        self.counter -= 1
        if not self.counter:
            semaphore.signal()
        self.mutex.unlock()


def monitor(monitor_id, access_data,
            turnstile, monitor_lightswitch, valid_data):
    """
    Method to simulate monitor actions. Main purpose of monitors is
    to access data. The access takes from 40 to 50 ms.

    Args:
        monitor_id(int): id of monitor
        access_data(Semaphore): semaphore to simulate data resource,
            and it's availability
        turnstile(Semaphore): Semaphore object implemented as turnstile.
            It is used to block sensors.
        monitor_lightswitch(Lightswitch): lightswitch object to lock and
            unlock data for access
        valid_data(Event[]): list of Events. Used for initial monitor
            startup.
    """
    for i in range(SENSORS):
        valid_data[i].wait()

    while True:
        turnstile.wait()
        turnstile.signal()
        waiting_monitors = monitor_lightswitch.lock(access_data)

        reading_duration = randint(40, 50) / 1000
        print(f'monitor: {monitor_id:02d}: ' +
              f'waiting monitors={waiting_monitors:02d}, ' +
              f'reading duration={reading_duration:.3f}')
        sleep(reading_duration)
        monitor_lightswitch.unlock(access_data)


def sensor(sensor_id, access_data, turnstile, sensor_lightswitch, valid_data):
    """
    Method to simulate sensors actions. Main purpose of sensors is
    to write data. This action is repeated every 50 to 60 ms.

    Args:
        sensor_id(int): id of sensor
        access_data(Semaphore): semaphore to simulate data resource,
            and it's availability
        turnstile(Semaphore): Semaphore object implemented as turnstile.
            It is used to block sensors.
        sensor_lightswitch(Lightswitch): lightswitch object to lock and
            unlock data for access
        valid_data(Event[]): list of Events. Used for initial monitor
            startup.
    """
    while True:
        sleep(randint(50, 60) / 1000)

        turnstile.wait()
        waiting_sensors = sensor_lightswitch.lock(access_data)
        turnstile.signal()

        if not sensor_id:
            writing_duration = randint(20, 25) / 1000
        else:
            writing_duration = randint(10, 20) / 1000
        print(f'sensor {sensor_id:02d}: ' +
              f'waiting sensors={waiting_sensors:02d}, ' +
              f'writing duration={writing_duration:.3f}')
        sleep(writing_duration)
        valid_data[sensor_id].signal()
        sensor_lightswitch.unlock(access_data)


def init():
    """
    Initialize all values, create threads and execute thier methods. 
    """
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    monitor_lightswitch = Lightswitch()
    sensor_lightswitch = Lightswitch()
    valid_data = [Event() for _ in range(SENSORS)]

    for monitor_id in range(MONITORS):
        Thread(monitor, monitor_id, access_data,
               turnstile, monitor_lightswitch, valid_data)
    for sensor_id in range(SENSORS):
        Thread(sensor, sensor_id, access_data,
               turnstile, sensor_lightswitch, valid_data)

if __name__ == '__main__':
    init()

