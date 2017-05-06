import threading
import random
import os
from time import sleep

numPhilos = 5
philos = []
forks = []
random.seed()


def check_deadlock():
    """ Determine if deadlock has occured.
    """

    for fork in forks:
        if not fork.lock.locked():
            return False

    return True


def fix_deadlock():
    """ Fix deadlock by forcing the unlock of a fork.
    """

    forks[0].letGo()


def askWaiter(philo):
    # Check for deadlock
    if check_deadlock():
        print("Found deadlock")
        fix_deadlock()

    left = forks[philo.leftFork].lock
    right = forks[philo.rightFork].lock
    s = 'Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.leftFork + 1)
    print(s)
    #Try to pick up the left fork. If the left fork is busy,
    if(left.acquire(False) != True):
        f = 'Fork ' + str(philo.leftFork + 1) + ' is busy.'
        print(f)
        s = 'Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.rightFork + 1)
        print(s)
        # then try to pick up the right fork. If the right fork is busy,
        if(right.acquire(False) != True):
            f = 'Fork ' + str(philo.rightFork + 1) + ' is busy.'
            print(f)
            s = 'Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.leftFork + 1)
            print(s)
            # then wait for the left fork,
            left.acquire()
            s = 'Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.leftFork + 1)
            print(s)
            s = 'Philosopher ' + str(philo.index + 1) + 'wants to pick up fork ' + str(philo.rightFork + 1)
            print(s)
            # then wait for the right fork.
            right.acquire()
            s = 'Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.rightFork + 1)
            print(s)
        # If the right fork was not busy,
        else:
            s = 'Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.rightFork + 1)
            print(s)
            s = 'Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.leftFork + 1)
            print(s)
            # then wait for the left fork.
            left.acquire()
            s = 'Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.leftFork + 1)
            print(s)
    # If the left fork was not busy,
    else:
        s = 'Philosopher ' + str(philo.index + 1) + ' picked up fork ' + str(philo.leftFork + 1)
        print(s)
        s = 'Philosopher ' + str(philo.index + 1) + ' wants to pick up fork ' + str(philo.rightFork + 1)
        print(s)
        # wait for the right fork.
        right.acquire()
        s = 'Philosopher ' + str(philo.index + 1) + ' is picking up fork ' + str(philo.rightFork + 1)
        print(s)


class Philosopher(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index
        self.leftFork = index
        self.rightFork = (index+1) % numPhilos
    def run(self):
        self.think()
    def think(self):
        s = 'Philosopher ' + str(self.index + 1) + ' is thinking.'
        print(s)
        sleep(random.randint(1,20))
        self.pickUp()

    def eat(self):
        s = 'Philosopher ' + str(self.index + 1) + ' is eating.'
        print(s)
        sleep(random.randint(2,9))
        self.putDown()

    def pickUp(self):
        # pick up forks
        askWaiter(self)
        self.eat()

    def putDown(self):
        # put down forks
        s = 'Philosopher ' + str(self.index + 1) + ' is putting down fork ' + str(self.leftFork + 1)
        print(s)
        forks[self.leftFork].letGo()
        s = 'Philosopher ' + str(self.index + 1) + ' is putting down fork ' + str(self.rightFork + 1)
        print(s)
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
