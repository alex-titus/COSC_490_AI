import random
import numpy
import MemoryMap

#import numpy as np

class DecisionFactory:
    def __init__(self, name = 'Joe'):
        self.name = name
        self.directions = [ 'wait', 'left', 'up', 'right', 'down']#'up', 'down', 'right', 'left']
        self.last_result = 'success'
        self.last_direction = 'wait'
        self.memory = MemoryMap.MemoryMap()

        # Note: we have relativisitic coordinates recorded here, since the map
        # is relative to the players first known recorded position:
        # self.state.pos = (0, 0)

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
        self.memory.remove_bad_choices(x, y, options)
        size = len(options)-1
        if size == 1:
            dir = self.random_direction()
            self.last_direction = dir
            return dir
        else:
            r = random.randint(1, size)
            dir = options[r]
            while self.check_decision(r) is False:
                r = random.randint(1, size)

            self.last_direction = dir

            return dir

    def put_result(self, x, y, result):
        self.last_result = result
        self.memory.memorize(x, y, self.last_direction, self.last_result)
