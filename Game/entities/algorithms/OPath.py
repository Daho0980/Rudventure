import os
import math
import time


def main(radius, center):
    path = []
    diameter = 2*radius+1

    for y in range(diameter):
        for x in range(diameter):
            dist = math.sqrt((x-radius)**2 + (y-radius)**2)
            
            if radius-0.5 < dist < radius+0.5:
                path.append((
                    y+center[0]-radius,
                    x+center[1]-radius
                    ))
    
    return organizePath(path)

def organizePath(path):
    pathDrawer = {}
    newPath    = []

    for y, x in path:
        if not pathDrawer.get(y):
            pathDrawer[y] = []
        pathDrawer[y].append((y, x))

    mn, mx = min(pathDrawer.keys()), max(pathDrawer.keys())

    for down in range(mn, mx+1, 1):
        if down <= int(len(pathDrawer)/2)+mn:
            newPath += pathDrawer[down][int(len(pathDrawer[down])/2):]
        else:
            if down == mx:
                newPath += pathDrawer[down][::-1]
            else:
                newPath += pathDrawer[down][int(len(pathDrawer[down])/2):][::-1]

    for up in range(mx-1, mn-1, -1):
        if up >= int(len(pathDrawer)/2)+mn:
            newPath += pathDrawer[up][:int(len(pathDrawer[up])/2)][::-1]
        else:
            newPath += pathDrawer[up][:int(len(pathDrawer[up])/2)]

    return newPath

def pathToGrid(path):
    global center

    grid = [['0' for _ in range(30)] for _ in range(30)]
    if 0<=center[0]<30 or 0<=center[1]<30:
        grid[center[0]][center[1]] = '\033[31m2\033[0m'

    for (y, x) in path:
        os.system("clear")
        if False in map(lambda i: False if i<0 or i>29 else True, [y, x]):
            pass
        else: grid[y][x] = '\033[32m1\033[0m'
        for row in grid:
            print(' '.join(row))
        time.sleep(0.03/radius)


if __name__ == '__main__':
    from random import randrange

    while 1:
        radius = 3
        center = (
            randrange(10, 20),
            randrange(10, 20)
            )
        os.system("clear")
        path = main(radius, center)
        pathToGrid(path)
        print(f"path : {path}")
        time.sleep(0.3)
