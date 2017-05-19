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


def search(list, needle):
    """ Traverses the given list to find the given needle value.
        Blocks deletion.
    """
    head = list.head

    # Acquire mutex
    list.block_search_or_delete.acquire()

    while head.next is not None:
        if head.data == needle:
            print "Found needle " + str(needle) + "!"
            return
        else:
            head = head.next

    print "Could not find needle " + str(needle) + "!"


def insert(list, value):
    """ Adds a node with the given value to the end of the list.
        Blocks both insertion and deletion.
    """
    head = list.head
    node = Node(value)

    # Acquire mutex
    list.block_insert_or_delete.acquire()

    if head is None:
        head = node
    else:
        while head.next is not None:
            head = head.next

        head.next = node

    print "Inserted new node with data " + str(value) + "!"

    list.block_insert_or_delete.release()


def delete(list, position):
    """ Delete a node from the list at the given position. Assume the position
        is less than the length of the list.
        Blocks both insertion and search.
    """
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
            print "Deleted node at position " + str(position) + "!"
            break
        else:
            last = head
            head = head.next

    list.block_search_or_delete.release()
    list.block_insert_or_delete.release()


if __name__ == "__main__":
    list = LinkedList()

    for i in range(0, 10):
        # Start a new inserter, searcher, and deleter in their own threads
        inserter = threading.Thread(target=insert, args=(list, i))
        inserter.start()
        # threading.Thread(target=search, args=(list, i))
        # threading.Thread(target=delete, args=(list))

    # For Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
