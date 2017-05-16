import threading
import random
import os
from time import sleep

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class linkedlist:
    def __init__(self):
        self.head = None

# Locked with deleters, but not searchers or inserters
class searcher(threading.Thread):
    def __init__(self, list):
        threading.Thread.__init__(self)
        self.list = list
        self.lock = threading.Lock()

    def run(self):
        # sleep and generate random searches?
        self.search()

    def search(self, index):
        # Acquire own Lock (which deleter might have)
        # Search


# Locked with deleters and inserters
class inserter(threading.Thread):
    def __init__(self, list, lock):
        threading.Thread.__init__(self)
        self.list = list
        self.lock = lock

    def run(self):
        # sleep and generate random inserts?
        self.insert()

    def insert(self, data):
        # Acquire insert lock (which deleter or another inserter might have)

        newNode = Node(data)
        if self.list.head == None:
            self.head = newNode
        else:
            newNode.next = self.head
            newNode.next.prev = newNode # set head prev to new node
            self.head = newNode


# Locked with everyone
class deleter(threading.Thread):
    def __init__(self, index, list):
        threading.Thread.__init__(self)

    def run(self):
        #  sleep and generate random deletes?
        self.delete()

    def delete(self, index):
        # Acquire all searchers locks
        # Acquire the insert lock
        # Delete stuff at index





if __name__ == "__main__":

    # Make the insert lock
    # Initialize linked list
    # Uh.. make threads




    # for Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
