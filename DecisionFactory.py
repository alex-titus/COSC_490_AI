import random
import numpy

from enum import Enum

class TileType(Enum):
	white = 0
	gray = 1
	black = 2
	wall = 3

class MemoryMap:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.sizeX = 10
		self.sizeY = 10
		self.forX = 0
		self.forY = 0
		self.recentlyExpanded = False
		self.map = []
		a = 0
		while a < self.sizeY:
			self.map.append([])
			b = 0
			while b < self.sizeX:
				self.map[a].append(TileType.white)
				b += 1
			a += 1
		self.print_tilemap()

	def get(self, x, y):
		return self.map[y+self.forY][x+self.forX]

	def set(self, x, y, type):
		self.map[y+self.forY][x+self.forX] = type

	def expandMap(self):# var = 0):
		a = 0
		while a < self.sizeY:
			b = 0
			while b < self.sizeX/2:
				self.map[a].insert(0, TileType.white)
				self.map[a].append(TileType.white)
				b += 1
			a += 1

		a = 0
		while a < self.sizeY/2:
			b = 0
			self.map.insert(0, [])
			self.map.append([])

			while b < self.sizeX*2:
				self.map[0].append(TileType.white)
				self.map[self.sizeX+a*2+1].append(TileType.white)
				b += 1
			a += 1
		self.sizeX *= 2
		self.sizeY *= 2

	def doubleMap(self, var = 0):
		a = 0
		while a < self.sizeY:
			b = 0
			#self.map.append([])
			while b < self.sizeX:
				self.map[a].append(TileType.white)

				b += 1
			a += 1
		self.sizeX *= 2

		a = self.sizeY
		while a < self.sizeY*2:
			b = 0
			self.map.append([])
			while b < self.sizeX:
				self.map[a].append(TileType.white)
				b += 1
			a += 1

		self.sizeY *= 2

	def expand_if_needed(self, x, y):
		expanded = False
		nx = x + self.forX
		ny = y + self.forY
		if ((ny < 1) or (ny + 1 >= self.sizeY)) or ((nx < 1) or (nx + 1 >= self.sizeX)):
			expanded = True
			self.expandMap()
			self.forX += self.sizeX/4
			self.forY += self.sizeY/4
			#self.print_tilemap
			self.expand_if_needed(x, y)
			self.recentlyExpanded = True
		return expanded

	def print_tilemap(self):
		y = 0
		while y < self.sizeY:
			x = 0
			row = ""
			while x < self.sizeX:
				#if x == 3 and y == 2:
				#	print("HELLO")
				row += (str(self.map[y][x].value) + "  ")
				x += 1
			print(row)
			y += 1
		print("")

	def auditTile(self, x, y):
		adjacents = {self.map[y-1][x], self.map[y][x-1], self.map[y+1][x], self.map[y][x+1]}
		if self.map[y][x] == TileType.gray:
			wallblackcount = 0
			for tile in adjacents:
				 if tile == TileType.wall or tile == TileType.black:
					 wallblackcount += 1

		return wallblackcount >= 3

	def audit(self):
		y = 0
		for col in self.map:
			x = 0
			for row in col:
				if auditTile(x, y):
					self.map[y][x] = TileType.black
				x += 1
			y += 1

	def memorize(self, x, y, direction, result):
		print("MEMORIZING: " + str(x) + " " + str(y) + " " + direction + " " + str(result))
		self.expand_if_needed(x, y)
		if direction == 'left':
			if result == True:
				self.map[y+self.forY][x+self.forX-1] = TileType.gray
			elif result == False:
				self.map[y+self.forY][x+self.forX-1] = TileType.wall
			#print("Updated TILE: " + str(self.map[x-1][y]))
		elif direction == 'up':
			if result == True:
				self.map[y+self.forY-1][x+self.forX] = TileType.gray
			elif result == False:
				self.map[y+self.forY-1][x+self.forX] = TileType.wall
			#print("Updated TILE: " + str(self.map[x][y-1]))
		elif direction == 'right':
			if result == True:
				self.map[y+self.forY][x+self.forX+1] = TileType.gray
			elif result == False:
				self.map[y+self.forY][x+self.forX+1] = TileType.wall
			#print("Updated TILE: " + str(self.map[x+1][y]))
		elif direction == 'down':
			if result == True:
				self.map[y+self.forY+1][x+self.forX] = TileType.gray
			elif result == False:
				self.map[y+self.forY+1][x+self.forX] = TileType.wall
			#print("Updated TILE: " + str(self.map[y+1][x]))
		elif direction == 'wait':
			self.map[y+self.forY][x+self.forX] = TileType.gray
			#print("Updated TILE: " + str(self.map[y][x]))
		self.print_tilemap()

	def rememberWalls(self, x, y, direction):
		self.expand_if_needed(x, y)
		if direction == 'left':
			if self.map[y+self.forY][x+self.forX-1] == TileType.wall:
				return False
			else:
				return True
		elif direction == 'up':
			if self.map[y+self.forY-1][x+self.forX] == TileType.wall:
				return False
			else:
				return True
		elif direction == 'right':
			if self.map[y+self.forY][x+self.forX+1] == TileType.wall:
				return False
			else:
				return True
		elif direction == 'down':
			if self.map[y+self.forY+1][x+self.forX] == TileType.wall:
				return False
			else:
				return True
		return True

	def rememberBadTiles(self, x, y, direction):
		self.expand_if_needed(x, y)
		if direction == 'left':
			if self.map[y+self.forY][x+self.forX-1] == TileType.black or self.map[y+self.forY][x+self.forX-1] == TileType.gray:
				return False
			else:
				return True
		elif direction == 'up':
			if self.map[y+self.forY-1][x+self.forX] == TileType.black or self.map[y+self.forY-1][x+self.forX] == TileType.gray:
				return False
			else:
				return True
		elif direction == 'right':
			if self.map[y+self.forY][x+self.forX+1] == TileType.black or self.map[y+self.forY][x+self.forX+1] == TileType.gray:
				return False
			else:
				return True
		elif direction == 'down':
			if self.map[y+self.forY+1][x+self.forX] == TileType.black or self.map[y+self.forY+1][x+self.forX] == TileType.gray:
				return False
			else:
				return True
		return True

	def remove_bad_choices(self, x, y, directions):
		#self.expand_if_needed(x, y)
		copy = list(directions)
		for d in copy:
			if d == 'left':
				if self.rememberWalls(x, y, d) is False:
					directions.remove('left')
			elif d == 'up':
				if self.rememberWalls(x, y, d) is False:
					directions.remove('up')
			elif d == 'right':
				if self.rememberWalls(x, y, d) is False:
					directions.remove('right')
			elif d == 'down':
				if self.rememberWalls(x, y, d) is False:
					directions.remove('down')
		return directions

	def remove_grayblack_choices(self, x, y, directions):
		#self.expand_if_needed(x, y)
		copy = list(directions)
		for d in copy:
			if d == 'left':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('left')
			elif d == 'up':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('up')
			elif d == 'right':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('right')
			elif d == 'down':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('down')
		if len(directions) - 1 == 0:
			directions = list(copy)
		return directions

class TravelPath:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.path = []
		self.pathlength = 0
		self.adjacents = []

	def push(self, direction):
		self.path.append(direction)
		self.pathlength += 1

	def pop(self):
		if self.pathlength >= 1:
			self.pathlength -= 1
			return self.path.pop()

class Mind:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.map = MemoryMap()
		self.relX = (self.map.sizeX + 1)/2
		self.relY = (self.map.sizeY + 1)/2
		self.map.memorize(self.relX, self.relY, 'wait', True)
		self.path = TravelPath()

	def move(self, direction):
		if direction == 'left':
			self.relX -= 1
		elif direction == 'up':
			self.relY -= 1
		elif direction == 'right':
			self.relX += 1
		elif direction == 'down':
			self.relY += 1

	def learn(self, direction, result):
		#if self.map.expand_if_needed(self.relX, self.relY):
		#	self.relX += self.map.sizeX/4
		#	self.relY += self.map.sizeY/4
		self.map.memorize(self.relX, self.relY, direction, result)
		if result == True:
			self.move(direction)

	def remove_bad_choices(self, directions):
		#if self.map.expand_if_needed(self.relX, self.relY):
		#	self.relX += self.map.sizeX/4
		#	self.relY += self.map.sizeY/4
		return self.map.remove_bad_choices(self.relX, self.relY, directions)

	def remove_grayblack_choices(self, directions):
		#if self.map.expand_if_needed(self.relX, self.relY):
		#	self.relX += self.map.sizeX/4
		#	self.relY += self.map.sizeY/4
		return self.map.remove_grayblack_choices(self.relX, self.relY, directions)

class DecisionFactory:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.directions = [ 'wait', 'left', 'up', 'right', 'down']#'up', 'down', 'right', 'left']
		self.last_result = 'success'
		self.last_direction = 'wait'
		self.mind = Mind()
		self.backtravelling = False
		# Note: we have relativisitic coordinates recorded here, since the map
		# is relative to the players first known recorded position:
		# self.state.pos = (0, 0)
		random.seed(random.randint(1, 5000))

	def get_decision(self, verbose = True):
		return self.smart_direction() #self.random_direction()

	def check_decision(self, dir):
		if dir == self.last_direction:
			if self.last_result is False:
				return False
		return True

	def random_direction(self):
		r = random.randint(1, 4)
		dir = self.directions[r]
		self.last_direction = dir
		return dir

	def smart_direction(self):
		options = list(self.directions)
		print("Available Decisions " + str(options))
		self.mind.remove_bad_choices(options)
		print("Moveable Decisions " + str(options))
		self.mind.remove_grayblack_choices(options)
		print("Smart Decisions " + str(options))
		print("Travel Path: " + str(self.mind.path.path))
		size = len(options)
		if size == 1:
			if len(self.mind.path.path) > 0:
				self.backtravelling = True
				print("No White Spaces. Back-travelling...")
				dir = self.mind.path.pop()
				print("Last Direction: " + dir)
				if dir == 'left':
					dir = 'right'
				elif dir == 'up':
					dir = 'down'
				elif dir == 'right':
					dir = 'left'
				elif dir == 'down':
					dir = 'up'
			else:
				dir = self.random_direction()
		else:
			r = random.randint(1, size-1)
			dir = options[r]
			while self.check_decision(r) is False:
				r = random.randint(1, size-1)

		self.last_direction = dir

		print("Direction: " + dir)
		return dir

	def put_result(self, result):
		if result == 'success':
			self.last_result = True
		else:
			self.last_result = False
		self.mind.learn(self.last_direction, self.last_result)
		if self.last_result is True:
			if self.backtravelling is False:
				self.mind.path.push(self.last_direction)
			else:
				self.backtravelling = False
