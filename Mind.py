import numpy
from Enums import *
import MemoryMap
import PathMemory
import TravelPath

class Mind:
    def __init__(self, name = 'Joe'):
        self.name = name
        self.map = MemoryMap.MemoryMap()
        self.relX = 1#(self.map.sizeX + 1)/2
        self.relY = 1#(self.map.sizeY + 1)/2
        self.map.memorize(self.relX, self.relY, 'wait', True)
        self.path = TravelPath.TravelPath()
        self.pathMem = PathMemory.PathMemory()
        self.recentWhiteAdjacents = TravelPath.TravelPath()

    def __del__(self):
        self.pathMem.update(self.path)

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
        self.map.memorize(self.relX, self.relY, direction, result)
        if result == True:
            self.move(direction)

    def remove_bad_choices(self, directions):
        return self.map.remove_bad_choices(self.relX, self.relY, directions)

    def remove_grayblack_choices(self, directions):
        return self.map.remove_grayblack_choices(self.relX, self.relY, directions)
