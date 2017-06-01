from threading import BoundedSemaphore, Thread
import os
from time import sleep


class SharedResource:
    """ Represents a shared resource.
    """
    def __init__(self, data):
        self.data = data
        self.active = 0
        self.waiting = 0
        self.must_wait = False
        self.mutex = BoundedSemaphore(value=1)
        self.block = BoundedSemaphore(value=3)


def search(id, resource):
    """ Using the pattern found here: https://pdfs.semanticscholar.org/93af/99143f8123032fbcc805656d63617a2268ab.pdf
    """
    print "ID-" + str(id) + " initialized"

    resource.mutex.acquire()
    if resource.must_wait:
        print "ID-" + str(id) + " needs to wait"

        resource.waiting += 1
        resource.mutex.release()
        resource.block.acquire()

    else:
        print "ID-" + str(id) + " does not need to wait"

        resource.active += 1
        resource.must_wait = (resource.active == 3)
        resource.mutex.release()

    # Critical Section
    print "ID-" + str(id) + " sees " + str(resource.data)
    sleep(3)

    resource.mutex.acquire()
    resource.active -= 1
    if resource.active == 0:
        n = min(resource.waiting, 3)
        resource.waiting -= n
        resource.active = n

        while n > 0:
            resource.block.release()
            n -= 1
        resource.must_wait = (resource.active == 3)

    resource.mutex.release()


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
