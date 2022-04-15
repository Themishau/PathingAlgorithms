class field:
    def __init__(self):
        self.gridSizeScale = 40
        self.gridSizey = 40
        self.gridSizex = 40
        self.gridfield = 25
        self.object_table = {
            "empty": 0,
            "food": 1,
            "obstacle": 2,
            "player": 3}
        self.field = []
        self.reset_playground()

    def add_from_field(self, gridx, gridy, id):
        self.field[gridx][gridy] = id

    def remove_from_field(self, gridx, gridy):
        self.field[gridx][gridy] = None

    def reset_playground(self):
        for column in self.field:
            self.field[column] = []
            for row in self.field[column]:
                self.field[column][row] = self.object_table["empty"]