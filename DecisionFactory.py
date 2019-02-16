import random
import numpy
#import numpy as np

class DecisionFactory:
    def __init__(self, name = 'Joe'):
        self.name = name
        self.directions = [ 'wait', 'up', 'down', 'right', 'left']
        self.last_result = 'success'
        self.last_direction = 'wait'

        # Note: we have relativisitic coordinates recorded here, since the map
        # is relative to the players first known recorded position:
        # self.state.pos = (0, 0)

    def get_decision(self, verbose = True):
        return self.random_direction()

    def check_decision(self, dir):
        if dir == self.last_direction:
            if self.last_result is False:
                return False
        return True

    def random_direction(self):
        #r = random.randint(0, 4)
        r = random.randint(1, 4)
        dir = self.directions[r]
        while self.check_decision(r) is False:
            r = random.randint(1, 4)

        self.last_direction = self.directions[r]

        return self.directions[r]

    def put_result(self, result):
        self.last_result = result
