import sys
import DecisionFactory
from pygame.locals import *

AI = DecisionFactory.DecisionFactory()

direction = AI.random_direction()
print(direction)

    direction = AI.random_direction()
    if direction == 'up' and playerY >= 0:
        playerY += 1
        print("step up")
    if direction == 'down' and playerY <= 10:
        playerY -= 1
        print("step down")
    if direction == 'left' and playerX >= 0:
        playerX -= 1
        print("step left")
    if direction == 'right'and playerX <= 10 :
        playerX += 1
        print("step right")
