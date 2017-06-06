from threading import BoundedSemaphore, Thread
import os
from time import sleep


class Agent:
    """ Represents an agent containing all of the synchronization constructs and boolean flags indicating which
        ingredients are currently on the table.
    """
    def __init__(self):
        self.agent_semaphore = BoundedSemaphore(value=1)
        self.tobacco = BoundedSemaphore(value=0)
        self.paper = BoundedSemaphore(value=0)
        self.match = BoundedSemaphore(value=0)

        # Indicate which ingredients are currently on the table
        self.is_tobacco = False
        self.is_paper = False
        self.is_match = False

        self.tobacco_semaphore = BoundedSemaphore(value=0)
        self.paper_semaphore = BoundedSemaphore(value=0)
        self.match_semaphore = BoundedSemaphore(value=0)

        self.mutex = BoundedSemaphore(value=1)


def smoker(agent, initial_ingredient):
    """ Represents a smoker, which has a given initial ingredient.
    """
    if initial_ingredient == "tobacco":
        agent.tobacco_semaphore.acquire()
    elif initial_ingredient == "paper":
        agent.paper_semaphore.acquire()
    elif initial_ingredient == "match":
        agent.match_semaphore.acquire()

    # Critical section
    print "Making cigarette"

    agent.agent_semaphore.release()

    print "Smoking"


def pusher(agent, ingredient):
    """ Represents a pusher, which is a helper thread which responds to signals from the given agent,
        keep track of ingredients, and signal the appropriate smoker thread.
    """
    while True:
        if ingredient == "tobacco":
            agent.tobacco.acquire()
            agent.mutex.acquire()

            if agent.is_paper:
                agent.is_paper = False
                agent.match_semaphore.release()

            elif agent.is_match:
                agent.is_match = False
                agent.paper_semaphore.release()

            else:
                agent.is_tobacco = True

            agent.mutex.release()

        elif ingredient == "paper":
            agent.paper.acquire()
            agent.mutex.acquire()

            if agent.is_tobacco:
                agent.is_tobacco = False
                agent.match_semaphore.release()

            elif agent.is_match:
                agent.is_match = False
                agent.tobacco_semaphore.release()

            else:
                agent.is_paper = True

            agent.mutex.release()

        elif ingredient == "match":
            agent.match.acquire()
            agent.mutex.acquire()

            if agent.is_tobacco:
                agent.is_tobacco = False
                agent.paper_semaphore.release()

            elif agent.is_paper:
                agent.is_paper = False
                agent.tobacco_semaphore.release()

            else:
                agent.is_match = True

            agent.mutex.release()


if __name__ == "__main__":
    agent = Agent()
    ingredients = ['tobacco', 'paper', 'match']
    for ingredient in ingredients:
        smoker_thread = Thread(target=smoker, args=(agent, ingredient))
        pusher_thread = Thread(target=pusher, args=(agent, ingredient))

        smoker_thread.start()
        pusher_thread.start()

    # For Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)