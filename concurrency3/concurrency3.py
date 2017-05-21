import threading
import random
import os
from time import sleep


class Node:
    """ Represents a node in the singly-linked list.
    """
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """ A data structure that maintains two semaphores: one for locking searchers, and
        one for locking inserters.
    """
    def __init__(self):
        self.head = None
        self.block_insert_or_delete = threading.BoundedSemaphore(value=1)
        self.block_search_or_delete = threading.BoundedSemaphore(value=1)


def search(list, value):
    """ Traverses the given list to find the given value.
        Blocks deletion.
    """
    print "Searching for " + str(value)

    # FIXME: Acquire mutex to block deleters without blocking other searchers
    # list.block_search_or_delete.acquire()

    head = list.head
    while head is not None:
        if head.data == value:
            print "Found value " + str(value)
            return
        else:
            head = head.next

    print "Could not find value " + str(value)

    # FIXME: Acquire mutex to block deleters without blocking other searchers
    # list.block_search_or_delete.release()


def insert(list, value):
    """ Adds a node with the given value to the end of the list.
        Blocks both insertion and deletion.
    """
    print "Inserting " + str(value)

    node = Node(value)

    # Acquire mutex
    list.block_insert_or_delete.acquire()

    if list.head is None:
        list.head = node
    else:
        while list.head.next is not None:
            list.head = list.head.next

        list.head.next = node

    print "Inserted new node with data " + str(value)

    list.block_insert_or_delete.release()


def delete(list, position):
    """ Delete a node from the list at the given position. Assume the position
        is less than the length of the list.
        Blocks both insertion and search.
    """
    print "Deleter released!"

    head = list.head
    last = list.head
    current_position = 0

    # Acquire mutexes
    list.block_search_or_delete.acquire()
    list.block_insert_or_delete.acquire()

    while head.next is not None:
        if current_position == position:
            last.next = head.next
            head = None
            print "Deleted node at position " + str(position)
            break
        else:
            last = head
            head = head.next

    list.block_search_or_delete.release()
    list.block_insert_or_delete.release()


if __name__ == "__main__":
    list = LinkedList()

    for i in range(0, 10):
        # Start a new inserter, searcher, and deleter in their own respective threads
        inserter = threading.Thread(target=insert, args=(list, i))
        searcher = threading.Thread(target=search, args=(list, i))
        deleter = threading.Thread(target=delete, args=(list))

        inserter.start()
        sleep(1)
        searcher.start()
        # deleter.start()


    # For Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
