import threading
import random
import os
from time import sleep


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """ A data structure that maintains two semaphores: one for locking searchers, and
        one for locking inserters.
    """
    def __init__(self, num_searchers):
        self.head = None
        self.no_inserter = threading.BoundedSemaphore(value=1)
        self.no_searcher = threading.BoundedSemaphore(value=1)


def search(list, needle):
    """ Traverses the given list to find the given needle value.
        Blocks deletion.
    """
    head = list.head

    # Acquire mutex
    sema = list.no_searcher.acquire()

    while head.next is not None:
        if head.data == needle:
            print "Found needle " + needle + "!"
            return
        else:
            head = head.next

    print "Could not find needle " + needle + "!"


def insert(list, value):
    """ Adds a node with the given value to the end of the list.
        Blocks both insertion and deletion.
    """
    head = list.head

    # Acquire mutex
    list.no_inserter.acquire()

    while head.next is not None:
        head = head.next

    node = Node(value)
    head.next = node


def delete(list, position):
    """ Delete a node from the list at the given position. Assume the position
        is less than the length of the list.
        Blocks both insertion and search.
    """
    head = list.head
    last = list.head
    current_position = 0

    # Acquire mutexes
    list.no_searcher.acquire()
    list.no_inserter.acquire()

    while head.next is not None:
        if current_position == position:
            last.next = head.next
            head = None
            print "Deleted node at position " + position + "!"
            break
        else:
            last = head
            head = head.next

    list.no_searcher.release()
    list.no_inserter.release()


if __name__ == "__main__":
    num_searchers = 3
    list = LinkedList(num_searchers)

    for i in range(0, 10):
        searcher = threading.Thread(target=search, args=(list))

    # For Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
