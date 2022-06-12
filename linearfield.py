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
        print(f'Rect CONTAINS: {rect}')
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
    items: list[Item] = field(default_factory=list)



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

    def insert(self, item: Item) -> bool:
        print(f' ---- children :  with properties of: {self.mRectOfChildren} and {self.quadtreechildren}')
        for i in range(4):
            if self.mRectOfChildren[i] is not None\
                    and self.mRectOfChildren[i].contains_rect(item.rect):
                # max depth reached?
                if self.depth + 1 < max_depth:
                    # does child exists?
                    try:
                        self.quadtreechildren[i]
                    except IndexError:
                        # create child
                        self.quadtreechildren.append(QuadTree(self.mRectOfChildren[i], depth=self.depth + 1))
                    # child exists
                    print(f' ---- children EXIST : {self.mRectOfChildren} and {self.quadtreechildren}')
                    self.quadtreechildren[i].insert(item)
                    return True

        # if it does not fit into the children, so the item belongs to this object
        self.items.append(item)

    def search_All_Items_by_name(self, item: Item) -> list:
        listItems = self.search_item_by_name(item)
        return listItems

    def search_item_by_name(self, item: Item) -> list:
        pass

    def search_All_Items_in_Field(self, item_position: Rect) -> list:

        listItems = []
        listItems = self.search_item_in_field(item_position, listItems)
        return listItems

    def search_item_in_field(self, item_position: Rect, listItems: list) -> list:
        """ searches items and returns a list of items """
        for item in self.items:
            if item_position.overlaps_rect(item.rect):
                listItems.append(item.item)

        for index, children in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if item_position.contains_rect(self.mRectOfChildren[index]):
                listItems = self.quadtreechildren[index].fillIItemsTolistItems(listItems)
                return listItems
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(item_position):
                listItems = self.quadtreechildren[index].search_item_in_field(item_position, listItems)
                return listItems

    def change_item(self, item: Item) -> None:

        for index, item in enumerate(self.items):
            if item.rect.overlaps_rect(item.rect):
                # changes the item on this position
                self.items[index] = item

        for index, children in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if item.rect.contains_rect(self.mRectOfChildren[index]):
                self.items[index] = item
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(item.rect):
                self.quadtreechildren[index].change_item(item)

    def remove_item(self, item_to_remove: Item) -> None:
        """ searches in quadtree and sets the item to empty """
        for index, item in enumerate(self.items):
            if item_to_remove.rect.overlaps_rect(item.rect):
                # set it to empty
                item_to_remove.item = ItemType.empty
                self.items[index] = item_to_remove

        for index, children in enumerate(self.quadtreechildren):
            # if in rect, add it to list without checks
            if item_to_remove.rect.contains_rect(self.mRectOfChildren[index]):
                del self.items[index]
            # if overlaps, we need to do some checks
            elif self.mRectOfChildren[index].overlaps_rect(item_to_remove.rect):
                self.quadtreechildren[index].remove_item(item_to_remove)


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

    def add_to_field(self, item: Item) -> None:
        self.quadtree.insert(item)

    def remove_from_field(self, item: Item) -> None:
        """ removes item from field """
        self.quadtree.remove_item(item)

    def get_items_in_field(self) -> list:
        """ returns a list of items """
        return self.quadtree.search_All_Items_in_Field(self.quadtree.mRect)

    def add_obstacle_to_playground(self, position: Rect):
        self.quadtree.insert(Item(position, ItemType.obstacle, WeightScale.heavy))

    def reset_playground_field(self):
        self.quadtree.resize(Rect({'x': 0, 'y': 0}, {'x': self.xSize, 'y': self.ySize}))

    def set_random_obstacles_to_field(self, obstacles: int) -> None:
        for i in range(obstacles):
            if self.quadtree is not None:
                self.quadtree.insert(
                    Item(Rect({'x': random.randrange(self.xSize),
                               'y': random.randrange(self.ySize)},
                               {'x': random.randrange(self.xSize),
                               'y': random.randrange(self.ySize)}),
                               ItemType.obstacle, WeightScale.heavy))
            # self.print_field()

    def set_random_goal(self):
        if self.quadtree is not None:
            self.quadtree.insert(
                Item(Rect({'x': random.randrange(self.xSize),
                           'y': random.randrange(self.ySize)},
                          {'x': random.randrange(self.xSize),
                           'y': random.randrange(self.ySize)}),
                           ItemType.goal, WeightScale.heavy))


    def print_field(self):
        print(f' print_field: {self.quadtree.search_All_Items_in_Field(self.quadtree.mRect)}')


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
