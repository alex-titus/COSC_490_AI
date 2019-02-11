import pygame, sys, time
from pygame.locals import *
import DecisionFactory

# THE COMPUTER IS ALIVE!
AI = DecisionFactory.DecisionFactory()

def player(playerX, playerY):
    pygame.transform.scale(pygame.image.load('PLAYER copy.png'), [TILESIZE, TILESIZE])
    display.blit(textures[PLAYER],(playerX*TILESIZE, playerY*TILESIZE))

def tile(tileX, tileY):
    display.blit(textures[TILE], (tileX*TILESIZE, tileY*TILESIZE))

# Which map we are going to be opening
currentMap = open("firstmap.txt", 'r')

# Information about the map we are creating
TILESIZE = 60
MAPWIDTH = 10
MAPHEIGHT = 10

# Setting up numbers to keep track
WALL = 0
TILE = 1
PLAYER = 2
PORTAL = 3
playerX = 0
playerY = 0
portalX = 0
portalY = 0

# Dictating TILEs and how they are images
textures = {
    WALL : pygame.transform.scale(pygame.image.load('WALL copy.png'),
    [TILESIZE, TILESIZE]),
    TILE : pygame.transform.scale(pygame.image.load('TILE copy.png'),
    [TILESIZE, TILESIZE]),
    PLAYER: pygame.transform.scale(pygame.image.load('PLAYER copy.png'),
    [TILESIZE, TILESIZE]),
    PORTAL : pygame.transform.scale(pygame.image.load('PORTAL copy.png'),
    [TILESIZE, TILESIZE]),
}

# Initializing pygame and creating the map
pygame.init()
display = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

FPS = 60
fpsClock = pygame.time.Clock()

# Map creation
column = 0
for line in currentMap:
    row = 0
    for ch in line:
        if ch == '1':
            display.blit(textures[WALL], (row*TILESIZE, column*TILESIZE))
            row += 1
        elif ch == '.':
            display.blit(textures[TILE], (row*TILESIZE, column*TILESIZE))
            row += 1
        elif ch == '0':
            display.blit(textures[TILE], (row*TILESIZE, column*TILESIZE))
            playerX = row
            playerY = column
            row += 1
        elif ch == '2':
            display.blit(textures[PORTAL], (row*TILESIZE, column*TILESIZE))
            portalX = row
            portalY = column
            row += 1
        else:
            row += 1
    column += 1
print("Map drawn")
print("Player is at: X" + str(playerX) + " Y" + str(playerY))
print("Portal is at: X" + str(portalX) + " Y" + str(portalY))

while True:
    # Get all the user events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                playerX -= 1
                print("Player moved left to: X" + str(playerX) + " Y" + str(playerY))
            if event.key == K_RIGHT or event.key == ord('d'):
                playerX += 1
                print("Player moved right to: X" + str(playerX) + " Y" + str(playerY))
            if event.key == K_UP or event.key == ord('w'):
                playerY -= 1
                print("Player moved up to: X" + str(playerX) + " Y" + str(playerY))
            if event.key == K_DOWN or event.key == ord('s'):
                playerY += 1
                print("Player moved down to: X" + str(playerX) + " Y" + str(playerY))

    if playerX == portalX:
        if playerY == portalY:
            pygame.quit()
            sys.exit()

    direction = AI.random_direction()
    if direction == 'up':
        if playerY > 1:
            tile(playerX, playerY)
            playerY -= 1
            print("step up")
    if direction == 'down':
        if playerY < 8:
            tile(playerX, playerY)
            playerY += 1
            print("step down")
    if direction == 'left':
        if playerX > 1:
            tile(playerX, playerY)
            playerX -= 1
            print("step left")
    if direction == 'right':
        if playerX < 9:
            tile(playerX, playerY)
            playerX += 1
            print("step right")

    player(playerX, playerY)
    pygame.display.update()
    fpsClock.tick(FPS)
