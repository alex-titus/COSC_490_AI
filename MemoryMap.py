import numpy
from Enums import *

class MemoryMap:
    def __init__(self, name = 'Joe'):#, sizeX = 10, sizeY = 10):
        self.name = name
        self.sizeX = 10
        self.sizeY = 10

        #self.map = [[TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)], [TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0), TileType(0)]]
        self.map = []
        a = 0
        while a < 10:
            self.map.append([])
            b = 0
            while b < 10:
                self.map[a].append(TileType(0))
                b += 1
            a += 1

    #WIP: VERY Broken
    def expandMap(self, var = 0):
        a = 0
        while a < self.sizeY:
            b = 0
            while b < self.sizeX/2:
                self.map[a].insert(0, TileType(0))
                self.map[a].append(TileType(0))
                b += 1
            a += 1

        a = 0
        while a < self.sizeY/2:
            b = 0
            self.map.insert(0, [])
            self.map.append([])

            while b < self.sizeX*2:
                self.map[0].append(TileType(0))
                self.map[self.sizeX+a*2+1].append(TileType(0))
                b += 1
            a += 1

        self.sizeX *= 2
        self.sizeY *= 2

    def print_tilemap(self):
        for y in self.map:
            row = ""
            for x in y:
                row += (str(x.value) + "  ")
            print row

    def memorize(self, x, y, direction, result):
        if direction == 'left':
            if result == True:
                self.map[x-1][y] = TileType(1)
            elif result == False:
                self.map[x-1][y] = TileType(3)
        elif direction == 'up':
            if result == True:
                self.map[x][y-1] = TileType(1)
            elif result == False:
                self.map[x][y-1] = TileType(3)
        elif direction == 'right':
            if result == True:
                self.map[x+1][y] = TileType(1)
            elif result == False:
                self.map[x+1][y] = TileType(3)
        elif direction == 'down':
            if result == True:
                self.map[x][y+1] = TileType(1)
            elif result == False:
                self.map[x][y+1] = TileType(3)

    def remember(self, x, y, direction):
        if direction == 'left':
            if self.map[x-1][y] == TileType(3):
                return False
            else:
                return True
        elif direction == 'up':
            if self.map[x][y+1] == TileType(3):
                return False
            else:
                return True
        elif direction == 'right':
            if self.map[x+1][y] == TileType(3):
                return False
            else:
                return True
        elif direction == 'down':
            if self.map[x][y+1] == TileType(3):
                return False
            else:
                return True

    def remove_bad_choices(self, x, y, directions):
        copy = list(directions)
        print("Available Decisions " + str(directions))
        for d in copy:
            if d == 'left':
                if self.remember(x, y, d) is False:
                    directions.remove('left')
            elif d == 'up':
                if self.remember(x, y, d) is False:
                    directions.remove('up')
            elif d == 'right':
                if self.remember(x, y, d) is False:
                    directions.remove('right')
            elif d == 'down':
                if self.remember(x, y, d) is False:
                    directions.remove('down')
        print("Good Decisions " + str(directions))
        return directions
