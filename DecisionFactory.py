import random
import numpy

from enum import Enum

class TileType(Enum):
    white = 0
    gray = 1
    black = 2
    wall = 3

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

class MemoryMap:
    def __init__(self, name = 'Joe'):#, sizeX = 10, sizeY = 10):
        self.name = name
        self.sizeX = 10
        self.sizeY = 10

        self.map = []
        a = 0
        while a < 10:
            self.map.append([])
            b = 0
            while b < 10:
                self.map[a].append(TileType.white)
                b += 1
            a += 1
        self.map[1][1] = TileType.gray

    def expandMap(self, var = 0):
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
        while (y + 1) >= self.sizeY or (x + 1) >= self.sizeX:
            print("Map too Small. Expanding...")
            self.doubleMap()
            print("New Size: " + str(self.sizeX) + "x" + str(self.sizeY))

    def print_tilemap(self):
        for y in self.map:
            row = ""
            for x in y:
                row += (str(x.value) + "  ")
            print row

    def auditTile(self, x, y):
        adjacents = {self.map[x-1][y], self.map[x][y-1], self.map[x+1][y], self.map[x][y+1]}
        if self.map[x][y] == TileType.gray:
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
                    self.map[x][y] = TileType.black
                x += 1
            y += 1

    def memorize(self, x, y, direction, result):
        self.expand_if_needed(x, y)
        if direction == 'left':
            if result == True:
                self.map[x-1][y] = TileType.gray
            elif result == False:
                self.map[x-1][y] = TileType.wall
        elif direction == 'up':
            if result == True:
                self.map[x][y-1] = TileType.gray
            elif result == False:
                self.map[x][y-1] = TileType.wall
        elif direction == 'right':
            if result == True:
                self.map[x+1][y] = TileType.gray
            elif result == False:
                self.map[x+1][y] = TileType.wall
        elif direction == 'down':
            if result == True:
                self.map[x][y+1] = TileType.gray
            elif result == False:
                self.map[x][y+1] = TileType.wall

    def rememberWalls(self, x, y, direction):
        self.expand_if_needed(x, y)
        if direction == 'left':
            if self.map[x-1][y] == TileType.wall:
                return False
            else:
                return True
        elif direction == 'up':
            if self.map[x][y-1] == TileType.wall:
                return False
            else:
                return True
        elif direction == 'right':
            if self.map[x+1][y] == TileType.wall:
                return False
            else:
                return True
        elif direction == 'down':
            if self.map[x][y+1] == TileType.wall:
                return False
            else:
                return True
        return True

    def rememberBadTiles(self, x, y, direction):
        self.expand_if_needed(x, y)
        if direction == 'left':
            if self.map[x-1][y] == TileType.black or self.map[x-1][y] == TileType.gray:
                return False
            else:
                return True
        elif direction == 'up':
            if self.map[x][y-1] == TileType.black or self.map[x][y-1] == TileType.gray:
                return False
            else:
                return True
        elif direction == 'right':
            if self.map[x+1][y] == TileType.black or self.map[x+1][y] == TileType.gray:
                return False
            else:
                return True
        elif direction == 'down':
            if self.map[x][y+1] == TileType.black or self.map[x][y+1] == TileType.gray:
                return False
            else:
                return True
        return True

    def remove_bad_choices(self, x, y, directions):
        self.expand_if_needed(x, y)
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
        self.expand_if_needed(x, y)
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

class DecisionFactory:
    def __init__(self, name = 'Joe'):
        self.name = name
        self.directions = [ 'wait', 'left', 'up', 'right', 'down']#'up', 'down', 'right', 'left']
        self.last_result = 'success'
        self.last_direction = 'wait'
        self.memory = MemoryMap()
        self.path = TravelPath()
        self.backtravelling = False
        # Note: we have relativisitic coordinates recorded here, since the map
        # is relative to the players first known recorded position:
        # self.state.pos = (0, 0)
        random.seed(random.randint(1, 5000))

    def get_decision(self, x, y, verbose = True):
        return self.smart_direction(x, y) #self.random_direction()

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

    def smart_direction(self, x, y):
        options = list(self.directions)
        print("Available Decisions " + str(options))
        self.memory.remove_bad_choices(x, y, options)
        print("Moveable Decisions " + str(options))
        self.memory.remove_grayblack_choices(x, y, options)
        print("Smart Decisions " + str(options))
        print("Travel Path: " + str(self.path.path))
        size = len(options)
        if size == 1:
            self.backtravelling = True
            print("No White Spaces. Back-travelling...")
            dir = self.path.pop()
            print("Last Direction: " + dir)
            if dir == 'left':
                dir = 'right'
            elif dir == 'up':
                dir = 'down'
            elif dir == 'right':
                dir = 'left'
            elif dir == 'down':
                dir = 'up'
            self.last_direction = dir
        else:
            r = random.randint(1, size-1)
            dir = options[r]
            while self.check_decision(r) is False:
                r = random.randint(1, size-1)

            self.last_direction = dir

        print("Direction: " + dir + "\n")
        return dir

    def put_result(self, x, y, result):
        self.last_result = result
        self.memory.memorize(x, y, self.last_direction, self.last_result)
        if self.last_result is True and self.backtravelling is False:
            self.path.push(self.last_direction)
        elif self.backtravelling is True:
            self.backtravelling = False
