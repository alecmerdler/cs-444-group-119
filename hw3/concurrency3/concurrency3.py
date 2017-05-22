from threading import BoundedSemaphore, Thread
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
    """ A singly-linked list data structure.
    """
    def __init__(self):
        self.head = None
        self.block_insert_or_delete = BoundedSemaphore(value=1)
        self.block_search_or_delete = BoundedSemaphore(value=1)

        self.insert_mutex = BoundedSemaphore(value=1)
        self.no_searcher = BoundedSemaphore(value=1)
        self.no_inserter = BoundedSemaphore(value=1)
        self.search_switch = LightSwitch()
        self.insert_switch = LightSwitch()

    def __str__(self):
        list_str = ""
        head = self.head 
        while head is not None:
            list_str += "[ " + str(head.data) + " ] -> "
            head = head.next
        list_str += "Null"

        return list_str


class LightSwitch:
    """ Light switch pattern from http://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf.
    """
    def __init__(self):
        self.counter = 0
        self.mutex = BoundedSemaphore(value=1)

    def lock(self, semaphore):
        """ Given a semaphore, acquire it if internal count is 0. Otherwise, carry on.
        """
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            semaphore.acquire()

        self.mutex.release()

    def unlock(self, semaphore):
        """ Given a semaphore, release it if internal count is 1. Otherwise, carry on.
        """
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            semaphore.release()

        self.mutex.release()


def search(id, list, value):
    """ Traverses the given list to find the given value.
        Blocks deletion.
    """
    print "ID-" + str(id) + ": Searching for " + str(value)

    list.search_switch.lock(list.no_searcher)

    # Critical Section
    head = list.head
    while head is not None:
        if head.data == value:
            print "ID-" + str(id) + ": Found value " + str(value)
            break
        else:
            head = head.next

    # Reached the end of the list without finding the value
    if head is None:
        print "ID-" + str(id) + ": Could not find value " + str(value)

    list.search_switch.unlock(list.no_searcher)



def insert(id, list, value):
    """ Adds a node with the given value to the end of the list.
        Blocks both insertion and deletion.
    """
    print "ID-" + str(id) + ": Inserting " + str(value)

    list.insert_mutex.acquire()
    list.insert_switch.lock(list.no_inserter)

    # Critical Section
    node = Node(value)

    if list.head is None:
        list.head = node
    else:
        while list.head.next is not None:
            list.head = list.head.next

        list.head.next = node

    print "ID-" + str(id) + ": Inserted new node with data " + str(value) + ". New list: " + str(list)

    list.insert_mutex.release()
    list.insert_switch.unlock(list.no_inserter)


def delete(id, list, position):
    """ Delete a node from the list at the given position. Assume the position
        is less than the length of the list.
        Blocks both insertion and search.
    """
    print "ID-" + str(id) + ": Deleter released!"

    list.no_searcher.acquire()
    list.no_inserter.acquire()

    # Critical Section
    head = list.head
    last = list.head
    current_position = 0

    while head is not None:
        if current_position == position:
            last.next = head.next
            head = None
            print "ID-" + str(id) + ": Deleted node at position " + str(position) + ". New list: " + str(list)
            break
        else:
            last = head
            head = head.next

    list.no_inserter.release()
    list.no_searcher.release()


if __name__ == "__main__":
    list = LinkedList()
    num = 3

    for i in range(0, num):
        # Start a new inserter, searcher, and deleter in their own respective threads
        inserter = Thread(target=insert, args=(i, list, i))
        searcher = Thread(target=search, args=(i + 1, list, i))
        deleter = Thread(target=delete, args=(i + 2, list, i))

        inserter.start()
        sleep(1)
        searcher.start()
        deleter.start()

    # For Ctrl+C
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        os._exit(0)
