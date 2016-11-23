"""
    CUSTOM PRIORITY QUEUE
    link : http://www.redblobgames.com/pathfinding/a-star/implementation.html#org1d80056
"""
import heapq


class PriorityQueue:
    # constructor
    def __init__(self):
        self.elements = []

    # check if queue is empty
    def empty(self):
        return len(self.elements) == 0

    # put dictionary into the queue
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # pop item from queue
    def get(self):
        return heapq.heappop(self.elements)[1]
