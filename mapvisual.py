import pygame, numpy, time, sys
import MemoryMap
from Enums import *
from pygame.locals import *
import DecisionFactory

filename = "./maps/rooms.txt"
slowmode = False
results = True

for x in sys.argv:
    if x == "-s":
        slowmode = True

# Which map we are going to be opening
currentMap = open(filename, 'r')

# Information about the map we are creating
TILESIZE = 30
MAPWIDTH = 20
MAPHEIGHT = 15

#Setting up numbers to keep track
RED = 0
WHITE = 1
GRAY = 2
BLACK = 3
PLAYER = 4
#PORTAL = 5
startX = 1
startY = 1
playerX = startX
playerY = startY
dx = 0
dy = 0
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
        AI.mind.map.expand_if_needed(x, y)
        if AI.mind.map.map[x+dx][y+dy] == TileType.white:
            whitetile(x, y)
        elif AI.mind.map.map[x+dx][y+dy] == TileType.gray:
            graytile(x, y)
        elif AI.mind.map.map[x+dx][y+dy] == TileType.black:
            blacktile(x, y)
        elif AI.mind.map.map[x+dx][y+dy] == TileType.wall:
            redtile(x, y)
        else:
            sys.exit()

# Initializing pygame and creating the map
pygame.init()
FPS = 24
fpsClock = pygame.time.Clock()  # type: None
display = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))  # type: None

# Map creation
tilemap = numpy.zeros(shape=(MAPHEIGHT, MAPWIDTH), dtype=numpy.int16)
row = 0
for line in currentMap:
    column = 0
    for ch in line:
        whitetile(column, row)
        if ch == '1':
            tilemap[row, column] = 1
        #elif ch == '.':
        #    tile(row, column)
        elif ch == '0':
            playerX = column
            playerY = row
        elif ch == '2':
            #portal(row, column)
            portalX = column
            portalY = row
        column += 1
    row += 1

steps = 0
fail = 0
success = 0
print(tilemap)

# THE COMPUTER IS ALIVE!
AI = DecisionFactory.DecisionFactory()
dx = AI.mind.relX - playerX
dy = AI.mind.relY - playerY

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
            print("Final Mind Map")
            pygame.quit()
            sys.exit()

    direction = AI.get_decision()
    print('(' + str(playerX) + ", " + str(playerY) + ')')
    print('(' + str(AI.mind.relX) + ", " + str(AI.mind.relY) + ')')
    if direction == 'up':
        results = up(playerX, playerY)
        AI.put_result(results)
        if results is False:
            fail += 1
        else:
            playerY -= 1
            success += 1
        steps += 1
    if direction == 'down':
        results = down(playerX, playerY)
        AI.put_result(results)
        if results is False:
            fail += 1
        else:
            playerY += 1
            success += 1
        steps += 1
    if direction == 'left':
        results = left(playerX, playerY)
        AI.put_result(results)
        if results is False:
            fail += 1
        else:
            playerX -= 1
            success += 1
        steps += 1
    if direction == 'right':
        results = right(playerX, playerY)
        AI.put_result(results)
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
