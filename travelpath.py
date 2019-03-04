import numpy
from Enums import*

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
