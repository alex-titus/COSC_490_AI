import pygame, numpy, time, sys
from pygame.locals import *
import DecisionFactory

# THE COMPUTER IS ALIVE!
AI = DecisionFactory.DecisionFactory()


def player(playerX, playerY):
    display.blit(textures[PLAYER], (playerX*TILESIZE, playerY*TILESIZE))


def tile(tileX, tileY):
    display.blit(textures[TILE], (tileX*TILESIZE, tileY*TILESIZE))


def wall(wallX, wallY):
    display.blit(textures[WALL], (wallX*TILESIZE, wallY*TILESIZE))


def portal(portalX, portalY):
    display.blit(textures[PORTAL], (portalX*TILESIZE, portalY*TILESIZE))


def updateclock(FPS, slowmode_enabled):
    fpsClock.tick(FPS)
    if slowmode_enabled == True: pygame.time.wait(100)
results = True


def up(playerX, playerY):
    if tilemap[playerY - 1, playerX] == 1:
        results = False
        print('Failure up')
        return results
    else:
        tile(playerX, playerY)
        results = True
        print(' Success up')
        return results


def down(playerX, playerY):
        if tilemap[playerY + 1, playerX] == 1:
            print("Failure down")
            results = False
            return results
        else:
            tile(playerX, playerY)
            print(playerY)
            results = True
            print("Success down")
            return results


def left(playerX, playerY):
    if tilemap[playerY, playerX - 1] == 1:
        results = False
        print("Failure left")
        return results
    else:
        tile(playerX, playerY)
        results = True
        print("Success left")
        return results


def right(playerX, playerY):
    if tilemap[playerY, playerX + 1] == 1:
        results = False
        print("Failure right")
        return results
    else:
        tile(playerX, playerY)
        results = True
        print("Success right")
        return results


filename = "./maps/firstmap.txt"
slowmode = True
human = False

for x in sys.argv:
    if x == "-s":
        slowmode = True
        if x == "-human":
            human = True
# Which map we are going to be opening
currentMap = open(filename, 'r')

# Information about the map we are creating
TILESIZE = 40
MAPWIDTH = 10
MAPHEIGHT = 10

#Setting up numbers to keep track
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
    WALL: pygame.transform.scale(pygame.image.load('./textures/wall.png'),
                                 [TILESIZE, TILESIZE]),
    TILE: pygame.transform.scale(pygame.image.load('./textures/tile.png'),
                                 [TILESIZE, TILESIZE]),
    PLAYER: pygame.transform.scale(pygame.image.load('./textures/player.png'),
                                   [TILESIZE, TILESIZE]),
    PORTAL: pygame.transform.scale(pygame.image.load('./textures/portal.png'),
                                   [TILESIZE, TILESIZE]),
}

# Initializing pygame and creating the map
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()  # type: None
display = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))  # type: None

# Map creation
tilemap = numpy.zeros(shape=(MAPWIDTH, MAPHEIGHT), dtype=numpy.int16)
column = 0
for line in currentMap:
    row = 0
    for ch in line:
        if ch == '1':
            wall(row, column)
            tilemap[column, row] = 1
        elif ch == '.':
            tile(row, column)
        elif ch == '0':
            tile(row, column)
            playerX = row
            playerY = column
        elif ch == '2':
            tile(row, column)
            portal(row, column)
            portalX = row
            portalY = column
        row += 1
    column += 1

steps = 0
fail = 0
success = 0
print(tilemap)


while True:
    # Get all the user events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    # End Condition for ending the "game"
    if playerX == portalX:
        if playerY == portalY:
            print("Portal was found in : " + str(steps) + " steps.")
            print("Failed steps: " + str(fail) + " steps. ")
            print("Succesful steps: " + str(success) + " steps.")
            pygame.quit()
            sys.exit()

    if human is True:
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                if tilemap[playerY, playerX-1] == 1:
                    print("failure left")
                else:
                    tile(playerX, playerY)
                    playerX -= 1
            if event.key == K_RIGHT or event.key == ord('d'):
                if tilemap[playerY, playerX+1] == 1:
                    print("failure right")
                else:
                    playerX += 1
            if event.key == K_UP or event.key == ord('w'):
                if tilemap[playerY-1, playerX] == 1:
                    print("failure up")
                else:
                    playerY -= 1
            if event.key == K_DOWN or event.key == ord('s'):
                if tilemap[playerY+1, playerX] == 1:
                    print("failure down")
                else:
                    playerY += 1
    else:
        direction = AI.random_direction()
        if direction == 'up':
            results = up(playerX, playerY)
            if results is False:
                steps += 1
                fail += 1
            else:
                playerY -= 1
                steps += 1
                success += 1
        if direction == 'down':
            results = down(playerX, playerY)
            if results is False:
                steps += 1
                fail += 1
            else:
                print()
                playerY += 1
                success += 1
                steps += 1
        if direction == 'left':
            results = left(playerX, playerY)
            if results is False:
                steps += 1
                fail += 1
            else:
                playerX -= 1
                success += 1
                steps += 1
        if direction == 'right':
            results = right(playerX, playerY)
            if results is False:
                steps += 1
                fail += 1
            else:
                playerX += 1
                success += 1
                steps += 1

    player(playerX, playerY)
    pygame.display.update()
    updateclock(FPS, slowmode)