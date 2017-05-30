import threading
import random
import os
from time import sleep




n = 4
customers = 0
custMutex = threading.Lock()
cust = threading.Semaphore(0)
barb = threading.Semaphore(0)

def customer():
    custMutex.acquire(True)
    if(customers == n):
        custMutex.release()
        # Exit

    customers += 1
    custMutex.release()

    cust.release()
    barb.acquire()

    # Cut hair



def barber():






if __name__ == "__main__":

    for i in range(0,n):
        customer = threading.Thread(target = customer)















    # for Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
