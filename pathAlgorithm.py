import pygame
from linearfield import LinearField, QuadtreeField, QuadTree, Rect
from AlgorithmPlayer import AlgorithmPlayer
import astar
from button import Button
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





# for i, j in zip(a,b):
#     print(i,j)


class AlgoGame:
    def __init__(self):
        # Define constants for the screen width and height

        self.screen_height = 800
        self.screen_width = 1000

        self.field_WIDTH = 800
        self.field_HEIGHT = 800
        self.clock = pygame.time.Clock()

        # example 800 / 20 = 40
        # block size is 20x20
        self.blocksize = 20
        self.gridsizeX = 800 / self.blocksize
        self.gridsizeY = 800 / self.blocksize

        self.field = LinearField(800, True)
        self.quadfield = QuadtreeField(QuadTree(Rect({'x': 0, 'y':0},{'x': self.gridsizeX, 'y': self.gridsizeY}), 0), size=int(self.field_WIDTH))
        # self.quadfield.initilizeQuadtree()
        self.quadfield.set_random_obstacles_to_field(40)
        self.quadfield.print_field()
        self.deltatimeupdate = 0

        # self.field.print_field()
        self.algorithmPlayer = AlgorithmPlayer('TestAlgorithm')

        self.play_button = None
        self.play_button = Button(image=None, pos=(850, 50), text_input='play', font=self.get_font(20), base_color='#d7fcd4',
                                  hovering_color='Yellow')

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def init_game(self):
        self.draw_objects_on_field(self.field.get_field())

    def quit_game(self):
        pass

    def update(self):
        pass

    def render(self, screen):

        # Draw a solid white circle in the center
        circle = pygame.Surface((50, 50))
        circle.fill((255, 255, 255))
        getTicksLastFrame = pygame.time.get_ticks()

        ### Fill the background with white ###
        screen.fill((0, 0, 0))
        surf = self.draw_objects_on_field(self.field.field)

        screen.blit(surf, (0, 0))
        # screen.blit(circle, (300, 300))
        pygame.display.flip()

        self.play_button.update(screen)

        ### Flip the display (refresh) ###
        pygame.display.flip()

        ### Ensure program maintains a rate of 30 frames per second ###
        self.clock.tick(60)

        t = pygame.time.get_ticks()
        # deltaTime in seconds.

        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t
        self.deltatimeupdate += deltaTime
        if self.deltatimeupdate > 3:
            self.deltatimeupdate = 0
            self.field.set_random_obstacles_to_field()



    def draw_objects_on_field(self, field):
        surf = pygame.Surface((self.field_WIDTH, self.field_HEIGHT))
        for i, column in enumerate(field, start=0):
            for j, row in enumerate(field[i], start=0):
                # empty field
                if row == 0:
                    pygame.draw.rect(surf, (122, 122, 122),
                                     ((j * self.blocksize, i * self.blocksize), (self.blocksize, self.blocksize)),
                                     width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1,
                                     border_bottom_left_radius=-1, border_bottom_right_radius=-1)
                # obstacle
                if row == 2:
                    pygame.draw.rect(surf, (22, 255, 22),
                                     ((j * self.blocksize, i * self.blocksize), (self.blocksize, self.blocksize)),
                                     width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1,
                                     border_bottom_left_radius=-1, border_bottom_right_radius=-1)
                # goal
                if row == 1:
                    pygame.draw.rect(surf, color='yellow',
                                     rect=((j * self.blocksize, i * self.blocksize), (self.blocksize, self.blocksize)),
                                     width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1,
                                     border_bottom_left_radius=-1, border_bottom_right_radius=-1)

                pygame.draw.rect(surf, (255, 255, 255),
                                 ((j * self.blocksize, i * self.blocksize), (self.blocksize, self.blocksize)),
                                 width=1, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1,
                                 border_bottom_left_radius=-1, border_bottom_right_radius=-1)

                # print("{} {} {} {}".format(j, i, j , i ))
        return surf



def startGame():

    """ creating an instance of AlgoGame """
    pygame.init()
    pathalgo = AlgoGame()

    # Set up the drawing window
    screen = pygame.display.set_mode((pathalgo.screen_width, pathalgo.screen_height))

    # Run until the user asks to quit
    running = True

    while running:

        ### check for actions ###
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:

                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:

                running = False

        ### game logic ###
        pathalgo.quadfield.update()

        ### draw objects ###
        pathalgo.render(screen)

    pygame.quit()



