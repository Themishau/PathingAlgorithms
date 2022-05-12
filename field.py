import pygame
import math
import random

class Rect:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def contains_point(self, point):
        return not (point.pos.x < self.pos.x
                    or point.y < self.pos.y
                    or point.x >= (self.pos.x + self.size.x)
                    or point.y >= (self.pos.y + self.size.y))

    def contains_rect(self, rect):
        return (rect.pos.x < self.pos.x) \
                and (rect.pos.x + rect.size.x < self.pos.x + self.size.x) \
                and (rect.pos.y < self.pos.y) \
                and (rect.pos.y + rect.size.y < self.pos.y + self.size.y)

    def overlaps_rect(self, rect):
        return self.pos.x < rect.pos.x + rect.size.x \
               and self.pos.x + self.size.x >= rect.pos.x \
               and self.pos.y < rect.pos.y + rect.size.y \
               and self.pos.y + self.size.y >= rect.pos.y



class Field(pygame.sprite.Sprite):
    def __init__(self, xSize, testmode):
        super(Field, self).__init__()

        self.gridSizeScale = 40
        self.gridSizey = 40
        self.gridSizex = 40
        self.gridfield = 25
        self.weightscale = 10

        self.xSize = math.ceil(xSize / self.gridSizeScale)
        self.ySize = math.ceil(xSize / self.gridSizeScale)

        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.field = []

        self.object_table = {
            "empty": 0,
            "goal": 1,
            "obstacle": 2,
            "player": 3}

        self.reset_playground()
        self.set_random_goal()
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
                self.field[column].append({"fieldtype": self.object_table["empty"],
                                           "fieldweight": random.randrange(self.weightscale)})

    def set_random_obstacles(self):
        if self.field is not None:
            for column in self.field:
                column[random.randrange(len(column))] = self.object_table["obstacle"]

        # self.print_field()

    def set_random_goal(self):
        if self.field is not None:
            self.field[random.randrange(len(self.field[0]))][random.randrange(len(self.field[0]))] = self.object_table["goal"]

    def print_field(self):
        for i, row in enumerate(self.field):
            print("column {} {}".format(i, len(row)))
