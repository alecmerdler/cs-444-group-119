import threading
import random
import os
from time import sleep



class SharedResource:
    def __init__(self):
        self.maxChairs = 4
        self.customers = 0
        self.custMutex = threading.Lock()
        self.cust = threading.Semaphore(0)
        self.barb = threading.Semaphore(0)
        self.custDone = threading.Semaphore(0)
        self.barbDone = threading.Semaphore(0)
        self.custID = 0
        self.clientCount = 0

class barber(threading.Thread):
    def __init__(self, resource):
        threading.Thread.__init__(self)
        self.r = resource
        self.lastClient = resource.clientCount

    def run(self):
        self.wait()

    def wait(self):
        print "Barber is waiting for a customer"
        self.r.cust.acquire(True)
        self.r.barb.release()

        self.cut_hair()

    def cut_hair(self):
        # Make sure the next customer is the one getting a hair cut so we can make the pretty print statement
        while True:
            sleep(0.1)
            if(self.lastClient != self.r.custID):
                break


        print "Barber is cutting hair for Customer " + str(self.r.custID) + "."
        sleep(4)
        self.r.barbDone.release()
        self.r.custDone.acquire()
        self.lastClient = self.r.custID
        self.wait()



def customer(id, r):
    print "Customer " + str(id) + " has walked in"
    r.custMutex.acquire(True)
    if(r.customers == 4):
        r.custMutex.release()
        print "Customer " + str(id) + " exits because the room is full."
        r.clientCount += 1
        # Exit
    else:
        r.customers += 1
        r.custMutex.release()
        print "Customer " + str(id) + " sits down."
        print "There are " + str(r.customers) + " customers waiting."

        r.cust.release()
        r.barb.acquire()
        r.custID = id

        # Get off chair if ready to get hair cut
        r.custMutex.acquire(True)
        r.customers -=1
        r.custMutex.release()

        # Cut hair
        get_hair_cut(id, r)


def get_hair_cut(id, r):
    sleep(4)
    r.custDone.release()
    r.barbDone.acquire()
    print "Customer " + str(id) + " is done with their hair cut and exits."
    r.clientCount += 1


if __name__ == "__main__":
    n = 12
    resource = SharedResource()
    barb = barber(resource)
    barb.start()
    for i in range(0,n):
        sleep(2)
        cust = threading.Thread(target = customer, args=(i+1, resource))
        cust.start()






    # for Ctrl+C
    try:
        while True:
            sleep(0.1)
            if(resource.clientCount == n):
                sleep(0.3)
                print "Barber closes up shop for the day."
                os._exit(0)
    except KeyboardInterrupt:
        os._exit(0)
