import threading
import random
import time
import os


# Inspired by: https://rosettacode.org/wiki/Dining_philosophers#Python


# Dining philosophers, 5 philosophers with 5 forks. Must have two forks to eat.
#
# Deadlock is avoided by never waiting for a fork while holding a fork (locked)
# Procedure is to do block while waiting to get first fork, and a nonblocking
# acquire of second fork.  If failed to get second fork, release first fork,
# swap which fork is first and which is second and retry until getting both.
class Philosopher(threading.Thread):
    """ Represents a philosopher, who has the ability to think, get forks, eat, and drop forks.
    """

    # Static class variable indicating the simulation is running
    running = True

    def __init__(self, xname, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.name = xname
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.has_forks = False

    def run(self):
        """ Method that is executed on thread start.
        """

        while self.running:
            while self.has_forks is False:
                self.think()
                self.get_forks()
            self.eat()
            self.put_forks()

    def think(self):
        print '%s is thinking.' % self.name
        time.sleep(random.uniform(1, 21))
        print '%s is finished thinking.' % self.name

    def get_forks(self):
        """ Wait for left fork to be available. Then try and pick up right fork. If it isn't available, drop left fork.
        """

        self.left_fork.acquire(True)
        available = self.right_fork.acquire(False)
        if not available:
            print '%s\'s right fork isn\'t available, so they put down their left fork.' % self.name
            self.left_fork.release()
            self.has_forks = False
        else:
            print '%s picks up both forks.' % self.name
            self.has_forks = True

    def eat(self):
        if self.has_forks:
            print '%s starts eating.' % self.name
            time.sleep(random.uniform(2, 10))
            print '%s finished eating.' % self.name
        else:
            raise ValueError('%s tried to eat without both forks.' % self.name)

    def put_forks(self):
        if self.has_forks:
            print '%s drops both forks.'% self.name
            self.left_fork.release()
            self.right_fork.release()
            self.has_forks = False
        else:
            raise ValueError('%s tried to drop forks it didn\'t have.'% self.name)


def DiningPhilosophers():
    """ Run the dining philosopher simulation.
    """

    # Build the simulation
    forks = [threading.Lock() for n in range(5)]
    philosopher_names = ('Aristotle', 'Kant', 'Buddha', 'Marx', 'Russel')
    random.seed(507129)
    philosophers = [Philosopher(philosopher_names[i], forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]

    # Start the simulation
    Philosopher.running = True
    for p in philosophers:
        p.start()

    # Stop the simulation after n seconds
    time.sleep(100)
    Philosopher.running = False
    print ("Now we're finishing.")


if __name__ == "__main__":
    # for Ctrl+C
    try:
        while True:
            DiningPhilosophers()
    except KeyboardInterrupt:
        os._exit(0)
