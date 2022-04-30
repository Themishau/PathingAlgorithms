import pygame
import math
import random

class Field(pygame.sprite.Sprite):
    def __init__(self, xSize, testmode):
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
        if testmode is True:
            self.set_random_obstacles()

    def add_to_field(self, gridx, gridy, id):
        self.field[gridx][gridy] = id

    def remove_from_field(self, gridx, gridy):
        self.field[gridx][gridy] = None

    def get_field(self):
        return self.field

    def add_obstacle_playground(self):
        for column in self.field:
            self.field[column] = []
            for row in self.field[column]:
                self.field[column][row] = self.object_table["obstacle"]

    def reset_playground(self):
        for column in range(0, self.ySize):
            self.field.append([])
            for row in range(0, self.xSize):
                self.field[column].append(self.object_table["empty"])


    def set_random_obstacles(self):
        if self.field is not None:
            for column in self.field:
                column[random.randrange(len(column))] = self.object_table["obstacle"]


        # self.print_field()

    def print_field(self):
        for i,row in enumerate(self.field):
            print("column {} {}".format(i, len(row)))
