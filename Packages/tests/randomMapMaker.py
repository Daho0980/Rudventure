import random

Map   = []
rooms = ['^', '\033[31m^\033[0m']
x, y  = 4, 4
for i in range(9): Map.append(['.', '.', '.', '.', '.', '.', '.', '.', '.'])

def fieldPrint(Map):
    for i in range(len(Map)): print(' '.join(map(str, Map[i])))

def randomPlace(Map):
    global x, y
    global rooms

    Map[y][x]     = '\033[31m^\033[0m'
    numberOfRooms = random.randrange(3, 20)
    for i in range(numberOfRooms):
        bfx, bfy = x, y
        x, y     = x + random.randrange(-1,2), y + random.randrange(-1,2)
        if y > len(Map)-1 or y < 0 or x > len(Map[0])-1 or x < 0:
            x, y = bfx, bfy
            numberOfRooms += 1
            continue
        if Map[y][x] != '.':
            x, y = bfx, bfy
            numberOfRooms += 1
            continue
        # if x <= len(Map[0])-2 and x > 1 and y <= len(Map)-2 and y > 1:
        somethin = ["[y+1][x]", "[y-1][x]", "[y][x+1]", "[y][x-1]"]
        if y == len(Map)-1: somethin.remove(somethin[0])
        if y == 0: somethin.remove(somethin[1])
        if x == len(Map[0])-1: somethin.remove(somethin[2])
        if x == 0: somethin.remove(somethin[3])

        for j in somethin:
            exec(f"if Map{j} not in rooms: x, y = bfx, bfy; numberOfRooms += 1")
        # if Map[y+1][x] not in rooms and Map[y-1][x] not in rooms and Map[y][x+1] not in rooms and Map[y][x-1] not in rooms:
        #     x, y = bfx, bfy
        #     numberOfRooms += 1
        #     continue
        print(f"{i} : y : {y}, x : {x}")
        Map[y][x] = '^'

    return Map

fieldPrint(randomPlace(Map))
