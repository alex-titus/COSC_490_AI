import pygame, numpy, time, sys
import MemoryMap
from pygame.locals import *

test = MemoryMap.MemoryMap()
test.print_tilemap()
print()
test.expandMap()
test.print_tilemap()
print()
test.expandMap()
test.print_tilemap()
print()
sys.exit()
