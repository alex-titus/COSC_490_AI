import numpy
import DecisionFactory

class Player:
    def __init__(self, name = 'Joe', tilemap, playerX, playerY):
        self.name = name
        self.x = playerX
        self.y = playerY
        self.AI = DecisionFactory.DecisionFactory()
