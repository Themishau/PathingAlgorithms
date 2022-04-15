import random
from field import field

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



# The aStar is a commonly used algorithm for pathfinding. This is a custom implementation of the algorithm.
# It looks for the shortest path from a starting point to a given goal. Any obstacles, represented
# through the obstacles Table, will not be traversed.
class aStar:
    def __init__(self, obstaclesTable, goalPosition, startPosition):
        self.obstaclesTable = obstaclesTable
        self.goalPosition   = goalPosition
        self.startPosition  = startPosition

    def compute(self):
        # The closedTable describes, which elements have already been visited by the algorithm
        closedTable = field(len(self.obstaclesTable), len(self.obstaclesTable)).fields
        startField = Node(self.startPosition, 0, None, self.goalPosition)

        # The open List represents the possible neighbouring fields which could be visited next.
        openList = PriorityQueue()

        # At first, the starting field is added to the open List
        openList.enqueue(startField, startField.fCost)

        # If there are no more entries in the openList, this means that the algorithm has visited
        # all possible fields without finding the goal along its path.
        for index in ((self.obstaclesTable.length * self.obstaclesTable.length) * 2):
            if openList is None:
                pass
            # The field with the shortest estimated costs (FCosts) towards the goal is removed from the open list
            smallestFScoreField = openList.dequeue().element

            x = smallestFScoreField.position.x
            y = smallestFScoreField.position.y

            # and then added to the closed list
            closedTable[x][y] = 1

            # If this field has the same coordinates as the goal, the goal has been found.
            if self.positionsAreEqual(smallestFScoreField.position, self.goalPosition):
                return { 'pathFound': True, 'nextNode': self.reconstruct_path(smallestFScoreField) }

            # bottom neighbour
            if y + 1 < self.obstaclesTable.length and self.obstaclesTable[x][y + 1] == 0 and closedTable[x][y + 1] == 0:
                neighbour = Node({ 'x': x, 'y': y + 1 }, smallestFScoreField.gCost + 1, smallestFScoreField, self.goalPosition)
                openList.enqueue(neighbour, neighbour.fCost)


            # upper neighbour
            if y - 1 >= 0 and self.obstaclesTable[x][y - 1] == 0 and closedTable[x][y - 1] == 0:
                neighbour = Node({ 'x': x, 'y': y - 1 }, smallestFScoreField.gCost + 1, smallestFScoreField, self.goalPosition)
                openList.enqueue(neighbour, neighbour.fCost)


            # right neighbour
            if x + 1 < self.obstaclesTable.length and self.obstaclesTable[x + 1][y] == 0 and closedTable[x + 1][y] == 0:
                neighbour = Node({ 'x': x + 1, 'y': y }, smallestFScoreField.gCost + 1, smallestFScoreField, self.goalPosition)
                openList.enqueue(neighbour, neighbour.fCost)


            # left neighbour
            if x - 1 >= 0 and self.obstaclesTable[x - 1][y] == 0 and closedTable[x - 1][y] == 0:
                neighbour = Node({ 'x': x - 1, 'y': y }, smallestFScoreField.gCost + 1, smallestFScoreField, self.goalPosition)
                openList.enqueue(neighbour, neighbour.fCost)

        return { 'pathFound': False, 'nextNode': None }

    # The aStar algorithm delivers a path to the goal. Going it backwards to the first node of the path
    # allows to find the next position to move, in order to follow the path calculated by aStar

    def reconstruct_path(self, current):
        while current.parent is not None:
            if current.parent.parent is not None:
                current = current.parent
            else:
                return current
        return current



    # This function determines to which position the AI will move next, using the aStar algorithm or a random free field
    # in case of the aStar not finding a path. This can happen when there is no path to the goal, for example if the goal is encircled by
    # obstacles. It returns if there is a free field to move at all, and if there is, the change on the x and y axis of the playfield needed
    # in order to reach that next field.

    def calculateNextMove(self, obstaclesTable, currentPosition, itemPosition, serpent):

        # aStar is the Pathfinding algorithm used to find a shortest path from the snakehead to the food
        aStarResult = aStar(obstaclesTable, itemPosition, currentPosition)

        if aStarResult.pathFound() is True:
        # aStar can only find a path, if the food position is reacheable in the current state of the game

            nextNode = aStarResult.nextNode
            if nextNode.position.x > currentPosition.x:
                #move right!
                return { 'movementIsPossible': True, 'direction': { 'dx': 1, 'dy': 0 }}

            if nextNode.position.x < currentPosition.x:
                #move left!
                return { 'movementIsPossible': True, 'direction': { 'dx': -1, 'dy': 0 }}

            if nextNode.position.y > currentPosition.y:
                #move down!
                return { 'movementIsPossible': True, 'direction': { 'dx': 0, 'dy': 1 }}

            if nextNode.position.y < currentPosition.y:
                #move up!
                return { 'movementIsPossible': True, 'direction': { 'dx': 0, 'dy': -1 }}

        #if aStar can not find a valid path, an adjacent free field will be chosen
        else:
            if currentPosition.y + 1 < obstaclesTable.length and obstaclesTable[currentPosition.x][currentPosition.y + 1] == 0:
                #move down!
                return { 'movementIsPossible': True, 'direction': { 'dx': 0, 'dy': 1 } }

            if currentPosition.y - 1 >= 0 and obstaclesTable[currentPosition.x][currentPosition.y - 1] == 0:
                #move up!
                return { 'movementIsPossible': True, 'direction': { 'dx': 0, 'dy': -1 } }

            if currentPosition.x + 1 < obstaclesTable.length and obstaclesTable[currentPosition.x + 1][currentPosition.y] == 0:
                #move right!
                return { 'movementIsPossible': True, 'direction': { 'dx': 1, 'dy': 0 } }

            if currentPosition.x - 1 >= 0 and obstaclesTable[currentPosition.x - 1][currentPosition.y] == 0:
                #move left!
                return { 'movementIsPossible': True, 'direction': { 'dx': -1, 'dy': 0 } }
            return { 'movementIsPossible': False, 'direction': { 'dx': 1, 'dy': 0 } }


    #Compares two positions
    def positionsAreEqual(self, positionA, positionB):
        return positionA.x == positionB.x and positionA.y == positionB.y


    # The aStar algorithm delivers a path to the goal. Going it backwards to the first node of the path
    # allows to find the next position to move, in order to follow the path calculated by aStar

    def reconstruct_path(self, current):
        while current.parent is not None:
            if current.parent.parent is not None:
                current = current.parent
            else:
                return current
        return current