from pathAlgorithm import AlgoGame
from field import field
from astar import *


# Compares two positions
def positionsAreEqual(positionA, positionB):
    return positionA.x == positionB.x and positionA.y == positionB.y



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pathalgo = AlgoGame()
    pathalgo.startGame()

