import numpy
import os
import TravelPath
from Enums import*

class PathMemory:
    def __init__(self, name = 'Joe', fp = 'paths', mem = 'last.txt'):
        self.name = name
        self.folder = fp
        self.file = mem
        self.dir = self.folder + "/" + self.file
        self.memoryExists = False
        self.lastPath = TravelPath.TravelPath()

        if not os.path.exists(self.folder):
            print("No memory directory found.")
            try:
                os.mkdir(self.folder)
                print("Directory: " + self.folder + " created")
            except OSError:
                print("Directory: " , self.folder ,  " could not be created. Exitting...")
                sys.exit()
        else:
            print("Memory directory found: " + self.folder)

        if not os.path.exists(self.dir):
            print("No memory file found.")
            try:
                open(self.dir, 'w+')
                print("File: " + self.file + " created")
            except OSError:
                print("File: " + self.file + " could not be created. Exitting...")
                sys.exit()
        else:
            self.memoryExists = True
            print("Memory file found: " + self.dir)
        if self.memoryExists:
            self.read()
            self.shorten()


    def update(self, tpath):
        f = open(self.dir, 'w')
        #f.write(str(x) + "\n")
        #f.write(str(y) + "\n")
        path = tpath.path
        while len(path) > 0:
            f.write(path[0] + "\n")
            path = path[1:]
        f.close()

    def read(self):
        path = TravelPath.TravelPath()
        f = open(self.dir, 'r')
        path.path = f.read().splitlines()
        f.close()

        path.pathlength = len(path.path)
        print(path.path)
        print(path.pathlength)
        path.path = path.path[::-1]
        self.lastPath = path
        if self.lastPath.pathlength == 0:
            self.memoryExists = False

    def shorten(self):
        def shortenable(a, b, c):
            print(a + " " + b + " " + c)
            if a == 'down' and c == 'up' and (b == 'left' or b == 'right'):
                return True
            elif a == 'up' and c == 'down' and (b == 'left' or b == 'right'):
                return True
            elif a == 'left' and c == 'right' and (b == 'up' or b == 'down'):
                return True
            elif a == 'right' and c == 'left' and (b == 'up' or b == 'down'):
                return True
            return False
        shortcut = self.lastPath.path[:]
        a = 0
        while a < len(shortcut) - 2 and len(shortcut) >= 3:
            if shortenable(shortcut[a], shortcut[a+1], shortcut[a+2]):
                print(True)
                shortcut = shortcut[0:a] + shortcut[a+1:a+2] + shortcut[a+3:]
            else:
                a += 1
        print("Pre-shortened Previous Path: " + str(self.lastPath.path))
        self.lastPath.path = shortcut
        self.lastPath.pathlength = len(shortcut)
        print("Shortened: Path: " + str(self.lastPath.path))
