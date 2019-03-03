import numpy
from Enums import *

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

    #WIP: VERY Broken
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

    def print_tilemap(self):
        for y in self.map:
            row = ""
            for x in y:
                row += (str(x.value) + "  ")
            print row

    #def auditTile(self, x, y):
    #    return (self.map[x][y] == TileType.gray) and (self.map[x-1][y] == TileType.wall or self.map[]
    #def audit(self):
    #    for y in self.map:

    #        for x in y:
    #            if(self.map[x][y] != TileType.white)
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
