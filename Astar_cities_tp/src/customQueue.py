"""
    CUSTOM QUEUE
    code used : http://www.redblobgames.com/pathfinding/a-star/implementation.html#org1d80056
"""
import collections


class Queue:
    # constructor
    def __init__(self):
        self.elements = collections.deque()

    # check if queue empty
    def empty(self):
        return len(self.elements) == 0

    # put dictionary into the dictionary
    def put(self, x):
        self.elements.append(x)

    # pop item from queue
    def get(self):
        return self.elements.popleft()
