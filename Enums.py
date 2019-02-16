# Used in MemoryMap.py
from enum import Enum

class Direction(Enum):
    left = 0
    up = 1
    right = 2
    down = 3

class Result(Enum):
    failure = -1
    unknown = 0
    success = 1

class TileType(Enum):
    unknown = 0
    tile = 1
    portal = 2
    wall = 3
