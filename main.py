import pygame, sys, time
from pygame.locals import *

# Which map we are going to be opening
currentMap = open("firstmap.txt", 'r')

# Information about the map we are creating
TILESIZE = 30
MAPWIDTH = 10
MAPHEIGHT = 10

WALL = 0
TILE = 1
PLAYER = 2
PORTAL = 3

# Dictating TILEs and how they are images
textures = {
    WALL : pygame.transform.scale(pygame.image.load('WALL copy.png'), [TILESIZE, TILESIZE]),
    TILE : pygame.transform.scale(pygame.image.load('TILE copy.png'), [TILESIZE, TILESIZE]),
    PLAYER : pygame.transform.scale(pygame.image.load('PLAYER copy.png'), [TILESIZE, TILESIZE]),
    PORTAL : pygame.transform.scale(pygame.image.load('PORTAL copy.png'), [TILESIZE, TILESIZE]),
}


# Initializing pygame and creating the map
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

FPS = 60
fpsClock = pygame.time.Clock()

while True:
    # First initialize the map, player, and portal
    row = 0
    for line in currentMap:
        column = 0
        for ch in line:
            if ch == '1':
                print("Attempting to draw a WALL")
                DISPLAYSURF.blit(textures[WALL], (column*TILESIZE, row*TILESIZE))
                column = column+1
            elif ch == '.':
                print("Attempting to draw a TILE")
                DISPLAYSURF.blit(textures[TILE], (column*TILESIZE, row*TILESIZE))
                column = column+1
            elif ch == '0':
                print("Attempting to draw a TILE, remembers PLAYER COORDS")
                # Place tile, remembers where playerX and playerX are init at
                DISPLAYSURF.blit(textures[TILE], (column*TILESIZE, row*TILESIZE))
                playerX = row
                playerY = column
                column = column+1
            elif ch == '2':
                print("Attempting to draw a PORTAL")
                DISPLAYSURF.blit(textures[PORTAL], (column*TILESIZE, row*TILESIZE))
                column = column+1
            else:
                column = column+1
        row = row+1

    # Get all the user events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Initalize player for movement
        PLAYER = pygame.transform.scale(pygame.image.load('PLAYER copy.png'),
        [TILESIZE, TILESIZE])

        playerPos = [playerY, playerY]

        DISPLAYSURF.blit(PLAYER,(playerPos[playerX]*TILESIZE,
        playerPos[playerY]*TILESIZE))
        
        # Movement of player initialied here
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            playerX -= 1
            print("left")
        if keys_pressed[pygame.K_RIGHT]:
            playerX += 1
            print("right")
        if keys_pressed[pygame.K_UP]:
            playerY -= 1
            print("up")
        if keys_pressed[pygame.K_DOWN]:
            playerY += 1
            print("down")


    pygame.display.update()
    fpsClock.tick(FPS)
