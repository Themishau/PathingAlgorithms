import pygame
import math
import random

max_depth = 8

class Rect:
    def __init__(self, pos, size):
        # pos has y and x values based on grid
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



class QuadTree:
    def __init__(self, mRect, depth):
        self.depth = depth
        # field based on grid example for grid 40x40
        self.mRect = mRect
        # array of field of children
        self.mRectOfChildren = []
        # max 4 quadtree children
        self.quadtreechildren = []
        # stored im this quadtree with area + object itself
        self.items = []

    def add_depth(self):
        self.depth += 1

    def resize(self, field):
        self.mRect = field

    # get size of all quadtrees and its children
    def size(self):

        count = len(self.items)

        for children in self.quadtreechildren:
            # count all children and call children
            count += children.size()

        return count

    def insert(self, item, rectItemSize):
        for i in range(3):
            if self.mRectOfChildren[i] is not None:

                # max depth reached?
                if self.depth + 1 < max_depth:

                    # does child exists?
                    if self.quadtreechildren[i] is None:
                        # create child
                        self.quadtreechildren[i] = QuadTree(self.mRectOfChildren[i], self.depth + 1)

                    # child exists
                    self.quadtreechildren[i].insert(item, rectItemSize)
                    return True

        # if it does not fit into the children, so the item belongs to this object
        self.items.append({'item': item, 'itemsize': rectItemSize})

    def searchAllItems(self, rectItemSize):

        listItems = []
        listItems = self.search_item(rectItemSize, listItems)
        return listItems

    def search_item(self, rectItemSize, listItems):

        for item in self.items:
            if rectItemSize.overlaps_rect(item.first):
                listItems.append(item.second)

        for children, index in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if rectItemSize.contains_rect(self.mRectOfChildren[index]):
                listItems = self.quadtreechildren[index].fillItems(listItems)
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(rectItemSize):
                listItems = self.quadtreechildren[index].search_item(rectItemSize, listItems)

    def fillItems(self, listItems):
        # add items to list
        for item in self.items:
            listItems.append(item)
        # call children recursively
        for children, index in enumerate(self.quadtreechildren):
            listItems = self.quadtreechildren[index].fillItems(listItems)

        return listItems

    def getArea(self):
        return self.mRect


# easy implementation of field
class Field(pygame.sprite.Sprite):
    def __init__(self, xSize, testmode):
        super(Field, self).__init__()

        self.gridSizeScale = 20
        self.gridSizey = 20
        self.gridSizex = 20
        self.gridfield = 25
        self.weightscale = 10

        self.xSize = math.ceil(xSize / self.gridSizeScale)
        self.ySize = math.ceil(xSize / self.gridSizeScale)

        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        # easy field with objects in it
        self.field = []
        # quadtree "field" filled with objects
        self.quadtree = QuadTree(Rect([0,0], # pos
                                      [self.xSize, self.ySize]), # size
                                 0) # depth


        self.object_table = {
            "empty": 0,
            "goal": 1,
            "obstacle": 2,
            "player": 3}

        self.reset_playground_field()
        self.set_random_goal()
        if testmode is True:
            self.set_random_obstacles_to_field()

    def add_to_field(self, gridx, gridy, id):
        self.field[gridx][gridy] = id

    def remove_from_field(self, gridx, gridy):
        self.field[gridx][gridy] = None

    def get_field(self):
        return self.field

    def add_obstacle_to_playground(self):
        for column in self.field:
            self.field[column] = []
            for row in self.field[column]:
                self.field[column][row] = self.object_table["obstacle"]

    def reset_playground_field(self):
        for column in range(0, self.ySize):
            self.field.append([])
            for row in range(0, self.xSize):
                self.field[column].append({"fieldtype": self.object_table["empty"],
                                           "fieldweight": random.randrange(self.weightscale)})

    def set_random_obstacles_to_field(self):
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
