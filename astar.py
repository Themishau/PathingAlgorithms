import random

class Node:
    def __init__(self, node_position, gCost, parent, goalPosition):
        self.nodePosition = node_position
        # the gCost is determined by the number of nodes that had to be travelles to reach this node
        self.gCost = gCost
        # the hCost is the heuristic used to guess the remaining distance to the goal
        self.hCost = abs(goalPosition.x - node_position.x) + abs(goalPosition.y - node_position.y)
        self.parent = parent
        self.goalPosition = goalPosition
        self.position = node_position
        # the fCost is the gCost and the hCost combined, representing the total cost for this node to get to the goal
        self.fCost = self.gCost + self.hCost

        # in this interpretation of the aStar algorithm, a small random number is added,
        # to prevent the algorithm from discovering multiple paths of the same cost. This improves the performance.
        randomFloat = (random.uniform(1, 20) * (0.1 - 0) + 0)
        self.fCost += randomFloat

        # the parent is the preceding node in the current path
        self.parent = parent


# PriorityQueue element
class QElement:
    def __init__(self, element, priority):
        self.element = element
        self.priority = priority


# queue items for ai serpents
# the priority Queue is used to store the discovered nodes and their fCosts costs.
# The cheaper the costs, the better.
# Selecting the node with the lowest cost is done by applying the deqeue method.
class PriorityQueue:

    def __init__(self):
        self.items = []

    def enqueue(self, element, priority):
        qElement = QElement(element, priority)
        contain = False

        for i in self.items:
            if i.priority > qElement.priority:
                self.items.insert(i, qElement)
                contain = True
                break

        if not contain:
            self.items.append(qElement)

    def dequeue(self):
        if self.items is None:
            return "Underflow"
        # get the first element of an array
        return self.items.pop(0)
