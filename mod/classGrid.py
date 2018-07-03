import pygame
import random as rd

from classCube import Cube

class  Cell:
    def __init__(self, i, j, x, y, dim):
        self.index = (i, j)
        self.center = (x, y)
        self.corner = (x - dim/2, y - dim/2)
        self.dim = dim
        self.isObjective = False
        self.value = None

    def setObjective(self, value):
        self.isObjective = True
        self.value = value

class Grid:

    def __init__(self, screenWidth, screenHeight, cellNum):    
        self.gridDim = screenWidth if screenWidth < screenHeight else screenHeight
        self.cellDim = self.gridDim/cellNum    
        self.cellNum = cellNum

        self.bounds = {
            "left":     (screenWidth - self.gridDim)/2,
            "right":    screenWidth - (screenWidth - self.gridDim)/2,
            "top":      (screenHeight - self.gridDim)/2,
            "bottom":   screenHeight - (screenHeight - self.gridDim)/2,
        }   

        self.cellsArray = []
        for i in range(0, cellNum):
            centersLine = []
            for j in range(0, cellNum):
                centersLine.append( ( Cell(i, j, (j*self.cellDim + self.cellDim/2 + self.bounds["left"]), (i*self.cellDim + self.cellDim/2 + self.bounds["top"]), self.cellDim) ) )
            self.cellsArray.append(centersLine)

        self.player = Cube(self.cellsArray[cellNum/2][cellNum/2], self.cellDim)

        self.currentTarget = self.cellsArray[cellNum/2][cellNum/2]
        self.nextTarget = self.cellsArray[cellNum/2][cellNum/2]

        self.maxObjectives = 1
        self.numObjectives = 0
        self.objectivesArray = []

        self.playerInBounds = True
    

    def draw(self, background):
        #draw horizontal lines
        for y in range(self.bounds["top"], self.bounds["bottom"]+1, self.cellDim):
            pygame.draw.line(background, (0,255,0), (self.bounds["left"], y), (self.bounds["right"], y))
        #draw vertical lines
        for x in range(self.bounds["left"], self.bounds["right"]+1, self.cellDim):
            pygame.draw.line(background, (0,255,0), (x, self.bounds["top"]), (x, self.bounds["bottom"]))

        self.drawObjectives(background)
        self.player.draw(background)
        self.drawTarget(background)
    
    def drawCenters(self, background):    
        #draw centers
        for line in self.cellsArray:
            for pt in line:
                pygame.draw.circle(background, (0,0,255), pt, 2)

    def drawTarget(self, background):    
        #draw centers
        pygame.draw.circle(background, (0,0,255), self.currentTarget.center, 2)
        pygame.draw.circle(background, (255,0,0), self.nextTarget.center, 2)

    def checkBoundaries(self):
        x, y = self.player.center
        if (
            (x + self.cellDim/2) > self.bounds["right"] or 
            (x - self.cellDim/2) < self.bounds["left"] or 
            (y + self.cellDim/2) > self.bounds["bottom"] or
            (y - self.cellDim/2) < self.bounds["top"]
        ):
            return False
        return self.playerInBounds

    def setObjective(self):
        if self.numObjectives < self.maxObjectives:
            i = rd.randint(0, self.cellNum-1)
            j = rd.randint(0, self.cellNum-1)
            self.cellsArray[i][j].setObjective(rd.randint(1,6))
            self.objectivesArray.append((i, j))
            self.numObjectives += 1

    def drawObjectives(self, background):
        for i, j in self.objectivesArray:
            objFont = pygame.font.Font('freesansbold.ttf', 20)
            textSurface = objFont.render(str(self.cellsArray[i][j].value), True, (255, 255, 255))
            typTextRect = textSurface.get_rect()
            typTextRect.center = self.cellsArray[i][j].center
            background.blit(textSurface, typTextRect)

    def checkObjectives(self):
        cell = self.getPlayerCell()
        for i, j in self.objectivesArray:
            if self.cellsArray[i][j] == cell:
                if self.player.getDiceSide() == cell.value:
                    self.objectivesArray.remove((i, j))
                    self.numObjectives -= 1
                else:
                    self.playerInBounds = False
                return 1

        return 0

    def getPlayerCell(self):
        x, y = self.player.center
        return self.cellsArray[(y - self.bounds["top"]) / self.cellDim][(x - self.bounds["left"]) / self.cellDim]

    def movePlayer(self):
        if self.player.move(self.currentTarget) == True:
            i, j  = self.currentTarget.index
            index1 = i + self.player.movement[1] / self.player.speed
            index2 = j + self.player.movement[0] / self.player.speed
            self.currentTarget = self.nextTarget
            try:
                self.nextTarget = self.cellsArray[index1][index2]
            except IndexError:
                self.playerInBounds = False

    def inputForward(self):
        if self.player.movement[1] == 0:
            i, j  = self.currentTarget.index
            try:
                self.nextTarget = self.cellsArray[i - 1][j]
            except IndexError:
                self.playerInBounds = False
            self.player.qHeading = 1

    def inputRight(self):
        if self.player.movement[0] == 0:
            i, j  = self.currentTarget.index
            try:
                self.nextTarget = self.cellsArray[i][j + 1]
            except IndexError:
                self.playerInBounds = False
            self.player.qHeading = 2

    def inputBack(self):
        if self.player.movement[1] == 0:
            i, j  = self.currentTarget.index
            try:
                self.nextTarget = self.cellsArray[i + 1][j]
            except IndexError:
                self.playerInBounds = False
            self.player.qHeading = 3

    def inputLeft(self):
        if self.player.movement[0] == 0:
            i, j  = self.currentTarget.index
            try:
                self.nextTarget = self.cellsArray[i][j - 1]
            except IndexError:
                self.playerInBounds = False
            self.player.qHeading = 4