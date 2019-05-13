import pygame, numpy, time, sys
from DecisionFactory import MemoryMap
from DecisionFactory import TileType
from DecisionFactory import TileType
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
	if slowmode_enabled == True: pygame.time.wait(300)

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

def get3x3(px = playerX, py = playerY):
	arr = []
	a = 0
	while a < 3:
		arr.append(tilemap[(py-1+a)][(px-1):(px+2)])
		a += 1
	#print(arr)
	#print(tilemap[1, 2])
	#print(tilemap[1][2])
	#arr.append(tilemap[1][0:3])
	#print(tilemap[1+a][0:3])
	#arr.append(tilemap[py][px])

	#print(arr)
	return arr
def getSurroundings(px = playerX, py = playerY):
	arr = [tilemap[py][px-1], tilemap[py-1][px], tilemap[py][px+1], tilemap[py+1][px]]
	return arr

def paintmap():
	spots = [[playerX, playerY], [playerX-1, playerY], [playerX, playerY-1], [playerX+1, playerY], [playerX, playerY+1]]
	for spot in spots:
		x = spot[0]
		y = spot[1]
		#if True: #(x >= 0 and x < AI.mind.map.sizeX) and (y >= 0 and y < AI.mind.map.sizeY):
		AI.mind.map.expand_if_needed(x+dx, y+dy)
		#AI.mind.relX += AI.mind.map.sizeX/4
		#AI.mind.relY += AI.mind.map.sizeY/4
		#print(AI.mind.map.get(x+dx, y+dy).value)
		if AI.mind.map.get(x+dx, y+dy) == TileType.white:
			whitetile(x, y)
		elif AI.mind.map.get(x+dx, y+dy) == TileType.gray:
			graytile(x, y)
		elif AI.mind.map.get(x+dx, y+dy) == TileType.black:
			blacktile(x, y)
		elif AI.mind.map.get(x+dx, y+dy) == TileType.wall:
			redtile(x, y)

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
			#tilemap[row, column] = 0
		if ch == '1':
			tilemap[row, column] = 1
		#elif ch == '.':
		#	tile(row, column)
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
	dx = AI.mind.relX - playerX
	dy = AI.mind.relY - playerY
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
			AI.mind.normalExit = True
			pygame.quit()
			sys.exit()

	print('Player Loc: (' + str(playerX) + ", " + str(playerY) + ')')
	print('Rel Player Loc: (' + str(AI.mind.relX) + ", " + str(AI.mind.relY) + ')')
	direction = AI.get_decision()
	if direction == 'up':
		results = up(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerY -= 1
			AI.put_result('success', get3x3(playerX, playerY))
			success += 1
		steps += 1
	if direction == 'down':
		results = down(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerY += 1
			AI.put_result('success', get3x3(playerX, playerY))
			success += 1
		steps += 1
	if direction == 'left':
		results = left(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerX -= 1
			AI.put_result('success', get3x3(playerX, playerY))
			success += 1
		steps += 1
	if direction == 'right':
		results = right(playerX, playerY)
		if results is False:
			AI.put_result('failure')
			fail += 1
		else:
			playerX += 1
			AI.put_result('success', get3x3(playerX, playerY))
			success += 1
		steps += 1

	paintmap()
	player(playerX, playerY)
	pygame.display.update()
	updateclock(FPS, slowmode)
	print("\n")
