from threading import Semaphore, BoundedSemaphore, Thread
import os
import random
from time import sleep


class Agent:
    """ Represents an agent containing all of the synchronization constructs and boolean flags indicating which
        ingredients are currently on the table.
    """
    def __init__(self):
        self.agent_semaphore = BoundedSemaphore(value=1)
        self.tobacco = Semaphore(value=0)
        self.paper = Semaphore(value=0)
        self.match = Semaphore(value=0)

        # Indicate which ingredients are currently on the table
        self.is_tobacco = False
        self.is_paper = False
        self.is_match = False

        self.tobacco_semaphore = Semaphore(value=0)
        self.paper_semaphore = Semaphore(value=0)
        self.match_semaphore = Semaphore(value=0)

        self.mutex = Semaphore(value=1)


def smoker(agent, initial_ingredient, id):
    """ Represents a smoker, which has a given initial ingredient.
    """

    if initial_ingredient == "tobacco":
        print "Smoker " + str(id) + " needs paper & matches"

    elif initial_ingredient == "paper":
        print "Smoker " + str(id) + " needs matches & tobacco"

    elif initial_ingredient == "match":
        print "Smoker " + str(id) + " needs tobacco & paper"


    while True:
        if initial_ingredient == "tobacco":
            agent.tobacco_semaphore.acquire()
        elif initial_ingredient == "paper":
            agent.paper_semaphore.acquire()
        elif initial_ingredient == "match":
            agent.match_semaphore.acquire()


        # Critical section
        print "Smoker " + str(id) + " is making cigarette"
        sleep(0.2)

        agent.agent_semaphore.release()

        print "Smoker " + str(id) + " is smoking"
        sleep(1)


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

    # sleep(1)

    print "\nSmokers will make cigarettes for 0.2 seconds."
    # sleep(1.5)
    print "\nAgent will wait for smokers to finish making cigarettes."
    # sleep(1.5)
    print "\nSmokers will smoke for 1 second.\n"
    # sleep(2)


    agent = Agent()
    ingredients = ['tobacco', 'paper', 'match']
    for smokerid in range(0,3):
        smoker_thread = Thread(target=smoker, args=(agent, ingredients[smokerid], smokerid+1))
        pusher_thread = Thread(target=pusher, args=(agent, ingredients[smokerid]))
        print "Smoker " + str(smokerid+1) + " has " + str(ingredients[smokerid])

        smoker_thread.start()
        pusher_thread.start()

    sleep(0.5)

    # For Ctrl+C
    try:
        while True:
            print "Agent is waiting for smoker..."
            agent.agent_semaphore.acquire()
            tempIng = list(ingredients)

            # Agent puts out two different ingredients
            for amount in range(0,2):
                i = random.choice(tempIng)

                if i is 'tobacco':
                    print "Agent puts tobacco on the table."
                    agent.tobacco.release()
                    tempIng.remove('tobacco')

                elif i is 'paper':
                    print "Agent puts paper on the table."
                    agent.paper.release()
                    tempIng.remove('paper')

                elif i is 'match':
                    print "Agent puts matches on the table."
                    agent.match.release()
                    tempIng.remove('match')



    except KeyboardInterrupt:
        print "Smoker accidentally lit everyone on fire."
        os._exit(0)
