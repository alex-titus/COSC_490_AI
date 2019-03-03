import numpy
from Enums import*

class TravelPath:
    def __init__(self, name = 'Joe'):
        self.name = name
        self.path = []
        self.pathlength = 0
        self.adjacents = []

    def addtoPath(self, dx, dy):
        self.path.append([dx, dy])
        self.pathlength += 1

    def pop(self):
        if self.pathlength >= 1:
            self.pathlength -= 1
            return self.path.pop()
