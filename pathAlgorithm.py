import pygame
from field import Field
from AlgorithmPlayer import AlgorithmPlayer
import astar
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Compares two positions
def positionsAreEqual(positionA, positionB):
    return positionA.x == positionB.x and positionA.y == positionB.y




class AlgoGame:
    def __init__(self):
        # Define constants for the screen width and height

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.clock = pygame.time.Clock()

        self.field = Field(800)
        self.algorithmPlayer = AlgorithmPlayer('TestALgorithm')

    def startGame(self):

        pygame.init()

        # Set up the drawing window
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Run until the user asks to quit
        running = True

        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:

                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:

                    running = False

            # Fill the background with white
            screen.fill((255, 255, 255))

            # Draw a solid blue circle in the center
            pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)


            # Flip the display
            pygame.display.flip()
            # Ensure program maintains a rate of 30 frames per second

            self.clock.tick(30)

        # Done! Time to quit.
        pygame.quit()