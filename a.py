import pygame, sys
from pygame.locals import *

# Which map we are going to be opening
currentMap = open("firstmap.txt", 'r')

for line in currentMap:
    for ch in line:
        print(ch)
