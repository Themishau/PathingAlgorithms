from field import Field
from AlgorithmPlayer import AlgorithmPlayer


class LevelConfig:
    def __init__(self, pathName, levelOption, xSize):
        # * ---- init some variables ----
        self.pathName = pathName
        self.levelOption = levelOption
        self.backGroudSpace = []
        self.bg_image = None
        self.PlaygroundLevel = Field(xSize)
        self.AlgorithmPlayer = []
        self.speed = 0
        self.playMode = self.levelOption.winCondition.playType
        self.otherPathAlgorithmn = []
        self.itemList = []

        # init level
        self.loadLevel()

    def loadLevel(self):
        if self.levelOption.playGroundSize == 2:
            gridfield = 50
            # gridSizeScale = canvasDimensions.height / gridfield
            # gridSizey = canvasDimensions.height / gridfield
            # gridSizex = canvasDimensions.height / gridfield

        elif self.levelOption.playGroundSize == 1:
            gridfield = 35
            # gridSizeScale = canvasDimensions.height / gridfield
            # gridSizey = canvasDimensions.height / gridfield
            # gridSizex = canvasDimensions.height / gridfield

        elif self.levelOption.playGroundSize == 0:
            gridfield = 25
            # gridSizeScale = canvasDimensions.height / gridfield
            # gridSizey = canvasDimensions.height / gridfield
            # gridSizex = canvasDimensions.height / gridfield

        if self.levelOption.movementAcc == 2:
            self.speed = 0.35

        elif self.levelOption.movementAcc == 1:
            self.speed = 0.20

        elif self.levelOption.movementAcc == 0:
            self.speed = 0.15

        # / * create pathalgorithm and set color * /
        if self.pathName == 'astar':
            self.AlgorithmPlayer.append(AlgorithmPlayer())

        # / * init items * /
        #this.itemlist[0] = new item(1, "wall", getRandomIntInclusive(3, gridfield - 3), getRandomIntInclusive(3, gridfield - 3), assets.clover);


        # / * add item to playground * /
        for item in self.itemList:
            self.PlaygroundLevel.add_to_field(item.gridx, item.gridy, item.id)
