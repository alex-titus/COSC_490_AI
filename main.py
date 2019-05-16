import pygame, numpy, time, sys
from DecisionFactory import MemoryMap
from DecisionFactory import TileType
from DecisionFactory import TileType
from pygame.locals import *
import DecisionFactory

defaultfilename = "./maps/firstmap.txt"
filename = defaultfilename
custommap = False
slowmode = False
slowmodewait = 100
human = False
results = True

argi = 0
for x in sys.argv:
	if argi == 1:
		if x == "-m":
			custommap = True
	elif argi == 2 and custommap:
		filename = ("./maps/" + x)
	elif x == "-h":
		human = True
		slowmode = False
	elif (x == "-s" or x == "-ss") and not human:
		slowmode = True
		if x == "-ss":
			slowmodewait *=2
	argi += 1

# Which map we are going to be opening
try:
	currentMap = open(filename, 'r')
except IOError:
	currentMap = open(filename, 'r')


# Information about the map we are creating
MAPWIDTH = 0
MAPHEIGHT = 0
cnt = 0
for line in currentMap:
	if cnt == 0:
		MAPHEIGHT = int(line)
	elif cnt == 1:
		MAPWIDTH = int(line)
		break
	cnt += 1

TILESIZE = 30

#Setting up numbers to keep track
WALL = 0
TILE = 1
PLAYER = 2
PORTAL = 3

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
	WALL: pygame.transform.scale(pygame.image.load('./textures/wall.png'),
                                 [TILESIZE, TILESIZE]),
	TILE: pygame.transform.scale(pygame.image.load('./textures/tile.png'),
                                 [TILESIZE, TILESIZE]),
	PLAYER: pygame.transform.scale(pygame.image.load('./textures/player.png'),
                               [TILESIZE, TILESIZE]),
	PORTAL: pygame.transform.scale(pygame.image.load('./textures/portal.png'),
                                   [TILESIZE, TILESIZE]),
}

def updateclock(FPS, slowmode_enabled):
	fpsClock.tick(FPS)
	if slowmode_enabled == True: pygame.time.wait(slowmodewait)

# GFX
def tile(tileX, tileY):
	display.blit(textures[TILE], (tileX*TILESIZE, tileY*TILESIZE))
def wall(wallX, wallY):
	display.blit(textures[WALL], (wallX*TILESIZE, wallY*TILESIZE))
def portal(portalX, portalY):
	display.blit(textures[PORTAL], (portalX*TILESIZE, portalY*TILESIZE))
def player(pX, pY):
	display.blit(textures[PLAYER], (pX*TILESIZE, pY*TILESIZE))

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
	#	tile(playerX, playerY)
	return results
def down(playerX, playerY):
	results = attemptDown(playerX, playerY)
	#if results:
	#	tile(playerX, playerY)
	return results
def left(playerX, playerY):
	results = attemptleft(playerX, playerY)
	#if results:
	#	tile(playerX, playerY)
	return results
def right(playerX, playerY):
	results = attemptright(playerX, playerY)
	#if results:
	#	tile(playerX, playerY)
	return results

# Initializing pygame and creating the map
pygame.init()
FPS = 24
fpsClock = pygame.time.Clock()  # type: None
display = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))  # type: None


# Map creation
tilemap = numpy.zeros(shape=(MAPHEIGHT, MAPWIDTH), dtype=numpy.int16)
row = 0
#lines = 0
for line in currentMap:
	column = 0
#	if lines >= 2:
	for ch in line:
		if ch == '1':
			tilemap[row, column] = 1
			wall(column, row)
		elif ch == '.':
			tile(column, row)
		elif ch == '0':
			tile(column, row)
			playerX = column
			playerY = row
		elif ch == '2':
			tile(column, row)
			portal(column, row)
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

moved = False
while True:

	tile(playerX, playerY)

	if moved:
		moved = False
	# Get all the user events
	direction = 'wait'
	for event in pygame.event.get():
		keys=pygame.key.get_pressed()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif human == True:
			if event.type == pygame.KEYDOWN:
				if keys[pygame.K_LEFT] == 1:
					direction = 'left'
					moved = True
				elif keys[pygame.K_UP] == 1:
					direction = 'up'
					moved = True
				elif keys[pygame.K_RIGHT] == 1:
					direction = 'right'
					moved = True
				elif keys[pygame.K_DOWN] == 1:
					direction = 'down'
					moved = True
				else:
					moved = False
				AI.last_direction = direction
			else:
				moved = False

	# End Condition for ending the "game"
	if playerX == portalX:
		if playerY == portalY:
			print("Portal was found in : " + str(steps) + " steps.")
			print("Failed steps: " + str(fail) + " steps. ")
			print("Succesful steps: " + str(success) + " steps.")
			AI.mind.normalExit = True
			pygame.quit()
			sys.exit()

	if not human:
		direction = AI.get_decision()

	if direction != 'wait':
		print('Player Loc: (' + str(playerX) + ", " + str(playerY) + ')')
		print('Rel Player Loc: (' + str(AI.mind.relX) + ", " + str(AI.mind.relY) + ')')

	if direction == 'up':
		results = up(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerY -= 1
			AI.put_result('success')
			success += 1
		steps += 1
	if direction == 'down':
		results = down(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerY += 1
			AI.put_result('success')
			success += 1
		steps += 1
	if direction == 'left':
		results = left(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerX -= 1
			AI.put_result('success')
			success += 1
		steps += 1
	if direction == 'right':
		results = right(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerX += 1
			AI.put_result('success')
			success += 1
		steps += 1

	player(playerX, playerY)
	pygame.display.update()
	updateclock(FPS, slowmode)
	if not human or (human and moved):
		print("\n")
