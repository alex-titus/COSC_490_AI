import pygame, numpy, time, sys
from pygame.locals import *
import DecisionFactory


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

filename = "./maps/firstmap.txt"
slowmode = False
human = False

for x in sys.argv:
    if x == "-s":
        slowmode = True
    if x == "-human":
        human = True

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
    if results:
        tile(playerX, playerY)
    return results

def down(playerX, playerY):
    results = attemptDown(playerX, playerY)
    if results:
        tile(playerX, playerY)
    return results

def left(playerX, playerY):
    results = attemptleft(playerX, playerY)
    if results:
        tile(playerX, playerY)
    return results

def right(playerX, playerY):
    results = attemptright(playerX, playerY)
    if results:
        tile(playerX, playerY)
    return results

def movePlayer(direction, playerX, playerY)
    if direction == 'left':
        if tilemap[playerY, playerX - 1] == 1:
            results = False
            print("Failure: Left")
            return results
        else:
            results = True
            tile(playerX, playerY)
            print("Success: Left")
            return results
    if direction == 'right':
        if tilemap[playerY, playerX - 1] == 1:
            results = False
            print("Failure: Right")
            return results
        else:
            results = True
            tile(playerX, playerY)
            print("Success: Right")
            return results
    if direction == 'Up':
        if tilemap[playerY - 1, playerX] == 1:
            results = False
            print("Failure: Up")
            return results
        else:
            results = True
            tile(playerX, playerY)
            print("Success: Up")
            return results
    if direction == 'down':
        if tilemap[playerY + 1, playerX] == 1:
            results = False
            print("Failure: Down")
            return results
        else:
            results = True
            tile(playerX, playerY)
            print("Success: Down")
            return results

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
FPS = 24
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

    if human is True:
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                results = left(playerX, playerY)
                if results:
                    playerX -= 1
            if event.key == K_RIGHT or event.key == ord('d'):
                results = right(playerX, playerY)
                if results:
                    playerX += 1
            if event.key == K_UP or event.key == ord('w'):
                results = up(playerX, playerY)
                if results:
                    playerY -= 1
            if event.key == K_DOWN or event.key == ord('s'):
                results = down(playerX, playerY)
                if results:
                    playerY += 1
    else:
        direction = AI.get_decision(playerX, playerY)
        print('(' + str(playerX) + ", " + str(playerY) + ')')
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

    AI.put_result(playerX, playerY, results)

    player(playerX, playerY)
    pygame.display.update()
    updateclock(FPS, slowmode)
