import pygame
import math
import random
from dataclasses import dataclass, field, asdict
from enum import Enum, auto

max_depth = 8

object_table = {
    "empty": 0,
    "goal": 1,
    "obstacle": 2,
    "player": 3}

class WeightScale(Enum):
    """ Types of Items """
    light = 1
    medium = 5
    heavy = 10


class ItemType(Enum):
    """ Types of Items """
    empty = auto()
    goal = auto()
    obstacle = auto()
    player = auto()



@dataclass(order=True, repr=True, eq=True)
class Rect:
    pos: {'"x"': int, '"y"': int}
    size: {'"x"': int, '"y"': int}

    def __truediv__(self, other):
        size = self.size
        return {'x': size['x'] / other, 'y': size['y'] / other}

    def resizeRect(self, Rect):
        self.pos = Rect.pos
        self.size = Rect.size

    def contains_point(self, point) -> bool:
        return not (point.pos['x'] < self.pos['x']
                    or point.y < self.pos['y']
                    or point.x >= (self.pos['x'] + self.size['x'])
                    or point.y >= (self.pos['y'] + self.size['y']))

    def contains_rect(self, rect: 'Rect') -> bool:
        return (rect.pos['x'] < self.pos['x']) \
               and (rect.pos['x'] + rect.size['x'] < self.pos['x'] + self.size['x']) \
               and (rect.pos['y'] < self.pos['y']) \
               and (rect.pos['y'] + rect.size['y'] < self.pos['y'] + self.size['y'])

    def overlaps_rect(self, rect: 'Rect') -> bool:
        return self.pos['x'] < rect.pos['x'] + rect.size['x'] \
               and self.pos['x'] + self.size['x'] >= rect.pos['x'] \
               and self.pos['y'] < rect.pos['y'] + rect.size['y'] \
               and self.pos['y'] + self.size['y'] >= rect.pos['y']

@dataclass(order=True, repr=True, eq=True)
class Item:
    rect: Rect
    item: ItemType = ItemType.empty
    weight: WeightScale = WeightScale.light

@dataclass(order=True, repr=True, eq=True)
class QuadTree(object):
    # field based on grid example for grid 40x40
    mRect: Rect
    depth: int
    # array of field of children
    mRectOfChildren: list[Rect] = field(default_factory=list)
    # max 4 quadtree children
    quadtreechildren: list['QuadTree'] = field(default_factory=list)
    # stored im this quadtree with area + object itself
    items: list[dict[object, Rect]] = field(default_factory=list)



    def add_depth(self):
        self.depth += 1


    def resize(self, rArea):
        self.ClearItems()
        self.mRect = rArea
        print(self.mRect)
        childSize = self.mRect / 2
        self.mRectOfChildren = [Rect(self.mRect.pos, childSize),
                                Rect({'x': self.mRect.pos['x'] + childSize['x'], 'y': self.mRect.pos['y']}, childSize),
                                Rect({'x': self.mRect.pos['x'], 'y': self.mRect.pos['y'] + childSize['y']}, childSize),
                                Rect({'x': self.mRect.pos['x'] + childSize['x'], 'y': self.mRect.pos['y'] + childSize['y']},
                                     childSize)]
        print(self.mRectOfChildren)

    def ClearItems(self):
        self.items = []

    # get size of all quadtrees and its children
    def size(self):

        count = len(self.items)

        for children in self.quadtreechildren:
            # count all children and call children
            count += children.size()

        return count

    def insert(self, item, rectItemSize: Rect):
        for i in range(4):
            print(f' children number : {i} with properties of: {self.mRectOfChildren[i]}')
            if self.mRectOfChildren[i] is not None\
                    and self.mRectOfChildren[i].contains_rect(rectItemSize):
                # max depth reached?
                if self.depth + 1 < max_depth:
                    # does child exists?
                    try:
                        self.quadtreechildren[i]
                    except IndexError:
                        # create child
                        self.quadtreechildren.append(QuadTree(self.mRectOfChildren[i], depth=self.depth + 1))
                    # child exists
                    self.quadtreechildren[i].insert(item, rectItemSize)
                    return True

        # if it does not fit into the children, so the item belongs to this object
        self.items.append({'item': item, 'itemsize': rectItemSize})

    def searchAllItems(self, rectItemSize: Rect) -> list:

        listItems = []
        listItems = self.search_item(rectItemSize, listItems)
        return listItems

    def search_item(self, rectItemSize: Rect, listItems: list) -> list:
        """ searches items and returns a list of items """
        for item in self.items:
            if rectItemSize.overlaps_rect(item['itemsize']):
                listItems.append(item['item'])

        for index, children in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if rectItemSize.contains_rect(self.mRectOfChildren[index]):
                listItems = self.quadtreechildren[index].fillIItemsTolistItems(listItems)
                return listItems
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(rectItemSize):
                listItems = self.quadtreechildren[index].search_item(rectItemSize, listItems)
                return listItems

    def change_item(self, position: Rect, item: ItemType) -> None:

        for index, item in enumerate(self.items):
            if position.overlaps_rect(item['itemsize']):
                # delete by index
                del self.items[index]

        for index, children in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if position.contains_rect(self.mRectOfChildren[index]):
                self.items[index] = {'item': item, 'itemsize': self.items[index]['itemsize'] }
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(position):
                self.quadtreechildren[index].change_item(position, item)

    def remove_item(self, position: Rect) -> None:

        for index, item in enumerate(self.items):
            if position.overlaps_rect(item['itemsize']):
                # delete by index
                del self.items[index]

        for index, children in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if position.contains_rect(self.mRectOfChildren[index]):
                del self.items[index]
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(position):
                self.quadtreechildren[index].remove_item(position)


    def fillIItemsTolistItems(self, listItems: list) -> list:
        """ add items to list and returns it """
        for item in self.items:
            listItems.append(item)
        # call children recursively
        for index, children in enumerate(self.quadtreechildren):
            listItems = self.quadtreechildren[index].fillIItemsTolistItems(listItems)

        return listItems

    def getArea(self):
        return self.mRect


# easy implementation of field
@dataclass(order=True, repr=True, eq=True)
class QuadtreeField(pygame.sprite.Sprite):
    # super(QuadtreeField, self).__init__()
    # quadtree "field" filled with objects
    quadtree: QuadTree
    size: int = 0
    gridSizeScale: int = 20
    gridSizey: int = 20
    gridSizex: int = 20
    gridfield: int = 25
    weightscale: int = 10

    xSize = math.ceil(size / gridSizeScale)
    ySize = math.ceil(size / gridSizeScale)

    surf = pygame.Surface((75, 25))
    surf.fill((255, 255, 255))
    rect = surf.get_rect()

    # # easy field with objects in it
    # self.field = []

    object_table = {
        "empty": 0,
        "goal": 1,
        "obstacle": 2,
        "player": 3}

    # self.reset_playground_field()
    # self.set_random_goal()
    #
    # if testmode is True:
    #     self.set_random_obstacles_to_field()

    def initilizeQuadtree(self) -> None:
        self.xSize = math.ceil(self.size / self.gridSizeScale)
        self.ySize = math.ceil(self.size / self.gridSizeScale)
        self.quadtree.resize(Rect({'x': 0, 'y': 0}, {'x': self.xSize, 'y': self.ySize}))

    def add_to_field(self, gridx: int, gridy: int, item: ItemType) -> None:
        self.quadtree.insert(item, Rect({'x': gridx, 'y': gridy}))

    def remove_from_field(self, gridx: int, gridy: int) -> None:
        """ removes item from field """
        self.quadtree.remove_item(Rect({'x': gridx, 'y': gridy}))

    def get_field(self) -> list:
        """ returns a list of items """
        return self.quadtree.searchAllItems(self.quadtree.mRect)

    def add_obstacle_to_playground(self, position):
        self.quadtree.insert({"item": self.object_table["obstacle"],
                              "weight": random.randrange(self.weightscale)}, Rect(position, {'x': 1, 'y': 1}))

    def reset_playground_field(self):
        self.quadtree.resize(Rect({'x': 0, 'y': 0}, {'xSize': self.xSize, 'ySize': self.ySize}))

    def set_random_obstacles_to_field(self, obstacles: int) -> None:
        for i in range(obstacles):
            if self.quadtree is not None:
                self.quadtree.insert({"item": self.object_table["obstacle"],
                                      "weight": random.randrange(self.weightscale)}, Rect({'x': random.randrange(self.xSize), 'y': random.randrange(self.ySize)}, {'x': 1, 'y': 1}))
            # self.print_field()

    def set_random_goal(self):
        if self.quadtree is not None:
            self.quadtree.insert({"item": self.object_table["obstacle"],
                                  "weight": random.randrange(self.weightscale)}, Rect({'x': random.randrange(self.xSize), 'y': random.randrange(self.ySize)}, {'x': 1, 'y': 1}))

    def print_field(self):
        print(f' print_field: {self.quadtree.searchAllItems(self.quadtree.mRect)}')


class LinearField(pygame.sprite.Sprite):
    """ easy implementation of field """
    def __init__(self, xSize, testmode):
        super(LinearField, self).__init__()

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
            self.field[random.randrange(len(self.field[0]))][random.randrange(len(self.field[0]))] = self.object_table[
                "goal"]

    def print_field(self):
        for i, row in enumerate(self.field):
            print("column {} {}".format(i, len(row)))
