import pygame

class conwayGame:
    def __init__(self, canvas, fgColor, bgColor, gridWidth, gridHeight, startX = 0, startY = 0, endX = 0, endY = 0, equalebreumAfter = 3) :
        self.canvas = canvas
        self.fgColor = fgColor
        self.bgColor = bgColor
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.equalebreumAfter = equalebreumAfter
        self.grid = []
        self.oldGrid = None
        self.lastChanges = 0
        self.lastChangeValue = 0
        if self.endX == 0 or self.endY == 0:
            self.endX, self.endY = self.canvas.get_size()

    def init(self, function):
        self.grid = []
        self.lastChanges = 0
        self.lastChangeValue = 0
        for i in range(self.gridHeight):
            self.grid.append([])
            for j in range(self.gridWidth):
                self.grid[i].append(function(j, i))

    def drawGrid(self):
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                if (self.oldGrid and self.grid[i][j] != self.oldGrid[i][j]):
                    self.drawRect(j, i, self.grid[i][j])
        self.oldGrid = self.grid.copy()

    def setAlive(self, x, y, alive):
        self.oldGrid[y][x] = self.grid[y][x]
        self.grid[y][x] = alive

    def getRect(self):
        xmouse, ymouse = pygame.mouse.get_pos()
        x = None
        y = None
        if int(xmouse) in range(self.startX, self.endX) and int(ymouse) in range(self.startY, self.endY):
            x = xmouse-self.startX
            y = ymouse-self.startY
            x = int(x/((self.endX-self.startX)/self.gridWidth))
            y = int(y/((self.endY-self.startY)/self.gridHeight))
        return x, y

    def getRectAlive(self, x, y):
        return self.grid[y][x]

    def drawRect(self, x, y, alive):
        drawWidth = self.endX-self.startX
        drawHeight = self.endY - self.startY
        color = self.bgColor
        if alive:
            color = self.fgColor
        pygame.draw.rect(self.canvas, color, pygame.Rect(x*drawWidth/self.gridWidth + self.startX, y*drawHeight/self.gridHeight + self.startY, drawWidth/self.gridWidth, drawHeight/self.gridHeight))

    def countAliveCells(self, x, y):
        aliveCells = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if y+i in  range(0, self.gridHeight) and x+j in range(0, self.gridWidth) and (i != 0 or j != 0):
                    aliveCells +=self.grid[y+i][x+j]
        return aliveCells
    
    def getNextState(self):
        changedCells = 0
        nextGrid = []
        for i in range(self.gridHeight):
            nextGrid.append([])
            for j in range(self.gridWidth):
                aliveCells = self.countAliveCells(j, i)
                becomesAlive = (self.grid[i][j] and aliveCells in range(2,4)) or (not(self.grid[i][j]) and aliveCells == 3)
                nextGrid[i].append(int(becomesAlive))
                changedCells += abs(self.grid[i][j]-nextGrid[i][j])
        self.grid = nextGrid.copy()
        return changedCells
    
    def reachedEqualebreum(self, changedCells):
        if changedCells == self.lastChangeValue:
            self.lastChanges += 1
        else:
            self.lastChangeValue = changedCells
            self.lastChanges = 1
        return self.lastChanges >= self.equalebreumAfter

