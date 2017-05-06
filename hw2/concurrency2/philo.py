import threading
import random
import os
from time import sleep

numPhilos = 5
philos = []
forks = []
random.seed()


def askWaiter(philo):

    left = forks[philo.leftFork].lock
    right = forks[philo.rightFork].lock
    print('Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.leftFork + 1))

    # Try to pick up the left fork.
    if left.acquire(False) != True:
        print('Fork ' + str(philo.leftFork + 1) + ' is busy.')
        print('Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.rightFork + 1))
        # If the left fork is busy, then try to pick up the right fork.
        if right.acquire(False) != True:
            print('Fork ' + str(philo.rightFork + 1) + ' is busy.')
            print('Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.leftFork + 1))
            # If the right fork is busy, then wait for the left fork,
            left.acquire()
            print('Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.leftFork + 1))
            print('Philosopher ' + str(philo.index + 1) + 'wants to pick up fork ' + str(philo.rightFork + 1))
            # then wait for the right fork.
            right.acquire()
            print('Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.rightFork + 1))
        # If the right fork was not busy,
        else:
            print('Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.rightFork + 1))
            print('Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.leftFork + 1))
            # then wait for the left fork.
            left.acquire()
            print('Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.leftFork + 1))
    # If the left fork was not busy,
    else:
        print('Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.leftFork + 1))
        print('Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.rightFork + 1))
        # wait for the right fork.
        right.acquire()
        print('Philosopher ' + str(philo.index + 1) + ' is picking up fork ' + str(philo.rightFork + 1))


class Philosopher(threading.Thread):

    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index
        self.leftFork = index
        self.rightFork = (index+1) % numPhilos

    def run(self):
        self.think()

    def think(self):
        print('Philosopher ' + str(self.index + 1) + ' is thinking.')
        sleep(random.randint(1,20))
        self.pickUp()

    def eat(self):
        print('Philosopher ' + str(self.index + 1) + ' is eating.')
        sleep(random.randint(2,9))
        self.putDown()

    def pickUp(self):
        # pick up forks
        askWaiter(self)
        self.eat()

    def putDown(self):
        # put down forks
        print('Philosopher ' + str(self.index + 1) + ' is putting down fork ' + str(self.leftFork + 1))
        forks[self.leftFork].letGo()
        print('Philosopher ' + str(self.index + 1) + ' is putting down fork ' + str(self.rightFork + 1))
        forks[self.rightFork].letGo()
        self.think()


class Fork():

    def __init__(self, index):
        self.lock = threading.Lock()

    def letGo(self):
        self.lock.release()


if __name__ == "__main__":
    for i in range(0,numPhilos):
        philos.append(Philosopher(i))
        forks.append(Fork(i))

    for philo in philos:
        philo.start()

    # for Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
