import pygame
import time
from mod.classGrid import Grid, Cell

colorBlack = (0, 0, 0)
colorWhite = (255, 255, 255)

screenWidth = 800
screenHeight = 600
numOfCells = 10

fps = 60

pygame.init()

surface = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Cube turning prototype')
clock = pygame.time.Clock()

def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type in [pygame.KEYDOWN,pygame.KEYUP]:
            return True
        return None

def makeTextObjs(text, font):
    textSurface = font.render(text, True, colorWhite)
    return textSurface, textSurface.get_rect()

def msgSurface(text, surface):
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    largeText = pygame.font.Font('freesansbold.ttf', 80)

    titleTextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = screenWidth/2, screenHeight/2
    surface.blit(titleTextSurf, titleTextRect)

    typTextSurf, typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center = screenWidth/2, screenHeight/2 + 200
    surface.blit(typTextSurf, typTextRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() == None:
        clock.tick()

def gameOver(surface):
    msgSurface('Oops!',surface)

def drawScore(background, score):
    objFont = pygame.font.Font('freesansbold.ttf', 20)
    textSurface = objFont.render(str(score), True, (255, 255, 255))
    typTextRect = textSurface.get_rect()
    typTextRect.center = (20, 20)
    background.blit(textSurface, typTextRect)

def main():
    on = True
    while on:
        escape = False       
        myGrid = Grid(screenWidth, screenHeight, numOfCells)
        playerScore = 0
        while not escape:
            myGrid.setObjective()
            for event in pygame.event.get():
                #quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    #movement
                    if event.key == pygame.K_UP:
                        myGrid.inputForward()
                    if event.key == pygame.K_LEFT: 
                        myGrid.inputLeft()
                    if event.key == pygame.K_DOWN:
                        myGrid.inputBack()
                    if event.key == pygame.K_RIGHT:
                        myGrid.inputRight()
            #refresh parameters and draw
            surface.fill(colorBlack)
            myGrid.movePlayer()
            myGrid.draw(surface)
            drawScore(surface, playerScore)
            pygame.display.update()
            clock.tick(fps)

            playerScore += myGrid.checkObjectives()

            if not myGrid.checkBoundaries():
                gameOver(surface)
                escape = True   

main()

pygame.quit()
quit()