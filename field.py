import pygame
import math

class Field(pygame.sprite.Sprite):
    def __init__(self, xSize):
        super(Field, self).__init__()

        self.gridSizeScale = 40
        self.gridSizey = 40
        self.gridSizex = 40
        self.gridfield = 25

        self.xSize = math.ceil(xSize / self.gridSizeScale)
        self.ySize = math.ceil(xSize / self.gridSizeScale)

        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.field = []

        self.object_table = {
            "empty": 0,
            "food": 1,
            "obstacle": 2,
            "player": 3}

        self.reset_playground()

    def add_to_field(self, gridx, gridy, id):
        self.field[gridx][gridy] = id

    def remove_from_field(self, gridx, gridy):
        self.field[gridx][gridy] = None

    def reset_playground(self):
        for column in self.field:
            self.field[column] = []
            for row in self.field[column]:
                self.field[column][row] = self.object_table["empty"]