import numpy
from Enums import *

class MemoryMap:
    def __init__(self, name = 'Joe'):#, sizeX = 10, sizeY = 10):
        self.name = name
        self.sizeX = 10
        self.sizeY = 10

        #FORMAT: self.map[mapX][mapY][0] = The the type of tile located at (mapX, mapY)
        #        self.map[mapX][mapY][1][direction] = A remembered result of attempting to move from the tile at (mapX, mapY) into the tile in the direction
        #
        #        direction:
        #           0 = Left
        #           1 = Up
        #           2 = Right
        #           3 = Down
        self.newtile = [TileType(0), [Result(0), Result(0), Result(0), Result(0)]]
        self.map = [[self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile], [self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile, self.newtile]]

    #WIP: VERY Broken
    def expandMap(self):
        a = 0
        newhalfrow = []
        while a < self.sizeX:
            newhalfrow.append(self.newtile)
            a += 1

        a = 0
        while a < self.sizeY:
            self.map[a].append(newhalfrow)
            a += 1

        newwholerow = []
        newwholerow.append(newhalfrow)
        newwholerow.append(newhalfrow)

        a = 0
        while a < self.sizeY*2:
            self.map.append(newwholerow)
            a += 1

        self.sizeX *= 2
        self.sizeY *= 2

    def print_tilemap(self):
        for y in self.map:
            row = ""
            for x in y:
                row += (str(x[0].value) + "  ")
            print(row)

    def memorize(self, x, y, direction, result):
        if result != Result(0):
            self.map[x][y][1][direction.value] = result
            if direction == Direction(0):
                if result == Result(1):
                    self.map[x-1][y][0] = TileType(1)
                    self.map[x-1][y][1][(direction.value+2)%2] = result
                if result == Direction(1):
                    self.map[x][y-1][0] = TileType(1);
                    self.map[x][y-1][1][(direction.value+2)%2] = result
                if result == Direction(2):
                    self.map[x+1][y][0] = TileType(1):
                    self.map[x+1][y][1][(direction.value+2)%2] = result
                if result == Direction(3):
                    self.map[x][y+1][0] = TileType(1):
                    self.map[x][y+1][1][(direction.value+2)%2] = result

    def remember(self, x, y, direction):
        if self.map[x][y][1][direction.value] != Result(-1):
            return True
