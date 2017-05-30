from threading import BoundedSemaphore, Thread
import os
from time import sleep


class SharedResource:
    """ Represents a shared resource, with a semaphore 'hot' for indicating if 3 threads have accessed the
        resource before being reset.
    """
    def __init__(self, data):
        self.data = data
        self.hot = BoundedSemaphore(value=3)


def search(id, resource):
    print "ID-" + str(id) + " initialized"

    resource.hot.acquire()

    # Critical Section
    print "ID-" + str(id) + " sees " + str(resource.data)
    sleep(5)

    resource.hot.release()



if __name__ == "__main__":
    num = 6
    resource = SharedResource(1)

    for i in range(0, num):
        searcher = Thread(target=search, args=(i, resource))
        searcher.start()
        sleep(1)

    # For Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
