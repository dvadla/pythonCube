import pygame
import numpy as np

class Cube:
    
    def __init__(self, cell, dimention):
        self.qHeading = 0
        self.movement = (0, 0)
        self.speed = 3
        self.state = [5,3,1,4,2,6]
        self.center = cell.center
        self.dim = dimention
        self.img = []
        for num in range(1,7):
            loadedImg = pygame.image.load('img/Cube'+str(num)+'.png')            
            self.img.append(pygame.transform.scale(loadedImg,(self.dim, self.dim)))

    def goLeft(self):
        if self.movement[0] == 0:
            temp = self.state[5]
            self.state[5] = self.state[3]
            self.state[3] = self.state[2]
            self.state[2] = self.state[1]
            self.state[1] = temp
            self.movement = (-self.speed, 0)
        

    def goRight(self):
        if self.movement[0] == 0:
            temp = self.state[5]
            self.state[5] = self.state[1]
            self.state[1] = self.state[2]
            self.state[2] = self.state[3]
            self.state[3] = temp
            self.movement = (self.speed, 0)

    def goForward(self):
        if self.movement[1] == 0:
            temp = self.state[5]
            self.state[5] = self.state[0]
            self.state[0] = self.state[2]
            self.state[2] = self.state[4]
            self.state[4] = temp
            self.movement = (0, -self.speed)

    def goBack(self):
        if self.movement[1] == 0:
            temp = self.state[5]
            self.state[5] = self.state[4]
            self.state[4] = self.state[2]
            self.state[2] = self.state[0]
            self.state[0] = temp
            self.movement = (0, self.speed)

    def draw(self,background):
        background.blit(self.img[self.state[2]-1],(self.center[0] - self.dim/2, self.center[1] - self.dim/2))

    def move(self, cell):
        cx, cy = cell.center
        sx, sy = self.center
        dy, dx = self.movement
        if ( abs(cx - sx) <= abs(dx) and abs(cy - sy) <= abs(dy)):
            
            self.center = cell.center

            if (self.qHeading == 0):
                self.movement = (0, 0)
            elif (self.qHeading == 1):
                self.goForward()
            elif (self.qHeading == 2):
                self.goRight()
            elif (self.qHeading == 3):
                self.goBack()
            elif (self.qHeading == 4):
                self.goLeft()

            return True

        else:
            self.center = (self.center[0] + self.movement[0], self.center[1] + self.movement[1])
            return False

    def speedUp(self):
        if self.speed < 5:
            self.speed += 1

    def speedDown(self):
        if self.speed > 0:
            self.speed -= 1

    def getDiceSide(self):
        return self.state[2];


