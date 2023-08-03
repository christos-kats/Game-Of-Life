import conwaygame
import configparse
import pygame
import time
import random
import ctypes

class game():
    def __init__(self, gridHeight, gridWidth, blockSize, bgColor, fgColor, interval, intervalRange, randomChance = 7, font='joystix-monospace.ttf'):
        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.startingInterval = interval
        self.interval = interval
        self.intervalRange = intervalRange
        self.randomChance = randomChance
        self.font = font
        self.aspectRatio = gridHeight/gridWidth
        self.width = blockSize*gridWidth
        self.height = self.aspectRatio*(self.width + self.width/10)
        self.screen = None
        self.conwayGame = None
        self.paused = True
        self.updateTime = 0
        self.mousePressed = False
        self.oldX = None
        self.oldY = None
        self.topBar = 0
        self.initPygame()
        self.initTopbar()
        self.initGame()
        self.updateTopBar()

    def initPygame(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Conway's Game Of Life")
        pygame.init()

    def initTopbar(self, relativeLineThicknes = 15):
        self.topBar = int(self.height-self.aspectRatio*self.width)
        lineThickness =  int((self.topBar)/relativeLineThicknes)
        pygame.draw.line(self.screen, self.fgColor, (0, self.topBar-lineThickness), (self.width, self.topBar-lineThickness), lineThickness)
        pygame.display.flip()

    def updateTopBar(self, relativeSize = 0.7, pausedRelativeSize = 0.85,  offset = -0.2):
        border = 10
        overlap = 0.1
        font = pygame.font.Font(self.font, int(self.topBar*relativeSize))
        textY = (self.topBar-self.topBar*relativeSize)/2 + offset*self.topBar*relativeSize
        multiplierText = font.render(str(round((self.startingInterval/self.interval), 3)) + "x    ", True, self.fgColor, self.bgColor)
        pausedPlaySize = self.topBar*relativeSize*pausedRelativeSize
        multiplierRect = multiplierText.get_rect()
        multiplierRect.topleft = (border, textY)
        pygame.draw.rect(self.screen, self.bgColor, pygame.Rect(self.width-pausedPlaySize-border-overlap*pausedPlaySize, (self.topBar -pausedPlaySize)/2-overlap*pausedPlaySize, (1+2*overlap)*pausedPlaySize, (1+2*overlap)*pausedPlaySize))
        if self.paused:
            self.drawPaused(self.width-pausedPlaySize-border, (self.topBar -pausedPlaySize)/2, pausedPlaySize)
        else:
            self.drawPlay(self.width-pausedPlaySize-border, (self.topBar -pausedPlaySize)/2, pausedPlaySize)
        self.screen.blit(multiplierText, multiplierRect)
        pygame.display.flip()
        pygame.display.update()
    
    def drawPaused(self, x, y, size):
        pygame.draw.rect(self.screen, self.fgColor, pygame.Rect(x, y, size/3, size))
        pygame.draw.rect(self.screen, self.fgColor, pygame.Rect(x+ 2*size/3, y, size/3, size))
    
    def drawPlay(self, x, y, size):
        pygame.draw.polygon(self.screen, self.fgColor, [(x+size/3, y), (x+size, y+ size/2), (x+size/3, y+size)])

    def initGame(self):
        self.conwayGame = conwaygame.conwayGame(self.screen, self.fgColor, self.bgColor, self.gridWidth, self.gridHeight, startY=self.topBar)
    
    def startGame(self, fillFunction):
        self.conwayGame.init(fillFunction)
        self.conwayGame.drawGrid()
        pygame.display.flip()
    
    def updateNow(self):
        self.updateTime = 0
    
    def updateOnTime(self):
        self.updateTime = time.time() + self.interval

    def updateDue(self):
        return time.time() > self.updateTime and not(self.paused)
    
    def updateGame(self):
        changedCells= self.conwayGame.getNextState()
        self.conwayGame.drawGrid()
        pygame.display.flip()
        self.updateOnTime()
    
    def mouseEventDue(self):
        return self.mousePressed and self.paused
        
    def handleMouseEvent(self):
        x, y = self.conwayGame.getRect()
        if (x != None and y != None) and (x != self.oldX or y != self.oldY):    
            alive = self.conwayGame.getRectAlive(x,y)
            self.conwayGame.setAlive(x, y, not (alive))
            self.conwayGame.drawRect(x, y, not(alive))
            self.oldX = x
            self.oldY = y
            pygame.display.flip()
            
    def getPygameEvents(self):
        return pygame.event.get()
    
    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not(self.paused)
                self.updateNow()
            if event.key == pygame.K_UP:
                if self.interval > self.intervalRange[0]:
                    self.interval = self.interval/2
                    self.updateOnTime()
            if event.key == pygame.K_DOWN:
                if  self.interval < self.intervalRange[1]:
                    self.interval = self.interval*2
                    self.updateOnTime()
            if event.key == pygame.K_RETURN:
                self.startGame(lambda x, y: int(random.randint(0, 10)> 10-self.randomChance))
                self.paused = True
            if event.key == pygame.K_BACKSPACE:
                self.startGame(lambda x, y: 0)
                self.paused = True
            self.updateTopBar()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.oldX = None
            self.oldY = None
            self.mousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mousePressed = False
        return True
    
        

try:
    config = configparse.readConfig("config.txt")
except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Error reading configuration file", 0)
else:
    newGame = game(50, 100, config["pixelSize"], config["bgColor"], config["fgColor"], config["startingInterval"], config["intervalLimits"], randomChance=config["randomChances"], font= config["font"])
    running = True
    newGame.startGame(lambda x, y: 0)
    while running:
        for event in newGame.getPygameEvents(): 
            running = newGame.handleEvent(event)
        if newGame.updateDue():
            newGame.updateGame()
        if newGame.mouseEventDue():
            newGame.handleMouseEvent()
    
            

    

    
        
        