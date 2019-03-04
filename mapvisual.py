import pygame, numpy, time, sys
import MemoryMap
from Enums import *
from pygame.locals import *
import DecisionFactory

filename = "./maps/bigmaze.txt"
slowmode = False
results = True

for x in sys.argv:
    if x == "-s":
        slowmode = True

# Which map we are going to be opening
currentMap = open(filename, 'r')

# Information about the map we are creating
TILESIZE = 30
MAPWIDTH = 37
MAPHEIGHT = 37

#Setting up numbers to keep track
RED = 0
WHITE = 1
GRAY = 2
BLACK = 3
PLAYER = 4
#PORTAL = 5
playerX = 1
playerY = 1
portalX = 0
portalY = 0

# Dictating TILEs and how they are images
textures = {
    RED: pygame.transform.scale(pygame.image.load('./textures/redtile.png'),
                                 [TILESIZE, TILESIZE]),
    WHITE: pygame.transform.scale(pygame.image.load('./textures/whitetile.png'),
                                 [TILESIZE, TILESIZE]),
    GRAY: pygame.transform.scale(pygame.image.load('./textures/graytile.png'),
                                 [TILESIZE, TILESIZE]),
    BLACK: pygame.transform.scale(pygame.image.load('./textures/blacktile.png'),
                                 [TILESIZE, TILESIZE]),
    PLAYER: pygame.transform.scale(pygame.image.load('./textures/player.png'),
                                 [TILESIZE, TILESIZE]),
}
def updateclock(FPS, slowmode_enabled):
    fpsClock.tick(FPS)
    if slowmode_enabled == True: pygame.time.wait(225)

# GFX
def redtile(playerX, playerY):
    display.blit(textures[RED], (playerX*TILESIZE, playerY*TILESIZE))

def whitetile(playerX, playerY):
    display.blit(textures[WHITE], (playerX*TILESIZE, playerY*TILESIZE))

def graytile(playerX, playerY):
    display.blit(textures[GRAY], (playerX*TILESIZE, playerY*TILESIZE))

def blacktile(playerX, playerY):
    display.blit(textures[BLACK], (playerX*TILESIZE, playerY*TILESIZE))

def player(playerX, playerY):
    display.blit(textures[PLAYER], (playerX*TILESIZE, playerY*TILESIZE))

# Movement
def attemptUp(playerX, playerY):
    if tilemap[playerY - 1, playerX] == 1:
        results = False
        print("Failure: Up")
        return results
    else:
        results = True
        print("Success: Up")
        return results

def attemptDown(playerX, playerY):
    if tilemap[playerY + 1, playerX] == 1:
        results = False
        print("Failure: Down")
        return results
    else:
        results = True
        print("Success: Down")
        return results

def attemptleft(playerX, playerY):
    if tilemap[playerY, playerX - 1] == 1:
        results = False
        print("Failure: Left")
        return results
    else:
        results = True
        print("Success: Left")
        return results

def attemptright(playerX, playerY):
    if tilemap[playerY, playerX + 1] == 1:
        results = False
        print("Failure: Right")
        return results
    else:
        results = True
        print("Success: Right")
        return results

def up(playerX, playerY):
    results = attemptUp(playerX, playerY)
    #if results:
    #    tile(playerX, playerY)
    return results

def down(playerX, playerY):
    results = attemptDown(playerX, playerY)
    #if results:
    #    tile(playerX, playerY)
    return results

def left(playerX, playerY):
    results = attemptleft(playerX, playerY)
    #if results:
    #    tile(playerX, playerY)
    return results

def right(playerX, playerY):
    results = attemptright(playerX, playerY)
    #if results:
    #    tile(playerX, playerY)
    return results

def paintmap():
    spots = [[playerX, playerY], [playerX-1, playerY], [playerX, playerY-1], [playerX+1, playerY], [playerX, playerY+1]]
    for spot in spots:
        x = spot[0]
        y = spot[1]
        AI.memory.expand_if_needed(x, y)
        if AI.memory.map[x][y] == TileType.white:
            whitetile(x, y)
        elif AI.memory.map[x][y] == TileType.gray:
            graytile(x, y)
        elif AI.memory.map[x][y] == TileType.black:
            blacktile(x, y)
        elif AI.memory.map[x][y] == TileType.wall:
            redtile(x, y)
        else:
            sys.exit()

# Initializing pygame and creating the map
pygame.init()
FPS = 24
fpsClock = pygame.time.Clock()  # type: None
display = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))  # type: None

# Map creation
tilemap = numpy.zeros(shape=(MAPWIDTH, MAPHEIGHT), dtype=numpy.int16)
column = 0
for line in currentMap:
    row = 0
    for ch in line:
        whitetile(row, column)
        if ch == '1':
            tilemap[column, row] = 1
        #elif ch == '.':
        #    tile(row, column)
        elif ch == '0':
            playerX = row
            playerY = column
        elif ch == '2':
            #portal(row, column)
            portalX = row
            portalY = column
        row += 1
    column += 1

steps = 0
fail = 0
success = 0
print(tilemap)

# THE COMPUTER IS ALIVE!
AI = DecisionFactory.DecisionFactory()

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

    direction = AI.get_decision(playerX, playerY)
    print('(' + str(playerX) + ", " + str(playerY) + ')')
    if direction == 'up':
        results = up(playerX, playerY)
        AI.put_result(playerX, playerY, results)
        if results is False:
            fail += 1
        else:
            playerY -= 1
            success += 1
        steps += 1
    if direction == 'down':
        results = down(playerX, playerY)
        AI.put_result(playerX, playerY, results)
        if results is False:
            fail += 1
        else:
            playerY += 1
            success += 1
        steps += 1
    if direction == 'left':
        results = left(playerX, playerY)
        AI.put_result(playerX, playerY, results)
        if results is False:
            fail += 1
        else:
            playerX -= 1
            success += 1
        steps += 1
    if direction == 'right':
        results = right(playerX, playerY)
        AI.put_result(playerX, playerY, results)
        if results is False:
            fail += 1
        else:
            playerX += 1
            success += 1
        steps += 1

    paintmap()
    player(playerX, playerY)
    pygame.display.update()
    updateclock(FPS, slowmode)
    print("\n")
