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
        self.fields = []

    def add_from_field(self, gridx, gridy, id):
        self.fields[gridx][gridy] = id

    def remove_from_field(self, gridx, gridy):
        self.fields[gridx][gridy] = None

    def reset_playground(self):
        print()