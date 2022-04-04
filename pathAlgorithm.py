import pygame
import field
import algorithm
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

class AlgoGame:
    def __init__(self):
        # Define constants for the screen width and height

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.clock = pygame.time.Clock()

    def startGame(self):

        pygame.init()

        # Set up the drawing window
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Run until the user asks to quit
        running = True

        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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