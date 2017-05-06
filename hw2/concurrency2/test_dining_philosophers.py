from philosopher import Philosopher, dining_philosophers
import threading
import random
import time
import os


def test_prevents_deadlock():
    """ Test that deadlock does not occur if each philosopher is holding exactly one fork.
    """

    forks = [threading.Lock() for n in range(5)]
    philosopher_names = ('Aristotle', 'Kant', 'Buddha', 'Marx', 'Russel')

    # Lock all forks
    for fork in forks:
        fork.acquire(True)

    dining_philosophers(forks, philosopher_names)


if __name__ == "__main__":
    random.seed(507129)

    try:
        while True:
            test_prevents_deadlock()

    # for Ctrl+C
    except KeyboardInterrupt:
        os._exit(0)
