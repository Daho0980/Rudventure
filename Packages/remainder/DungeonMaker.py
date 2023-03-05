import random
import time
import os

Map       = []
progress  = [[4, 4]]
direction = {
    'U' : 1,
    'R' : 2,
    'D' : 3,
    'L' : 4
}

def clear():
    if os.name == 'posix': os.system("clear")
    else                 : os.system("cls")

def GraphicMaker(MapData):
    grid = []
    for i in range(len(MapData)):
        grid.append([])
        for j in range(len(MapData[i])): grid[i].append(MapData[i][j][0])

    return grid

for i in range(9):
    Map.append([])
    for j in range(9): Map[i].append([' ', 0, 0, 0, 0])

x, y         = 4, 4
rooms        = ['\033[31m§\033[0m', '•', '\033[32m*\033[0m', '\033[33m!\033[0m', '\033[34m/\033[0m']
Map[y][x][0] = rooms[0]

def gridPrint(grid):
    for i in grid: print(' '.join(map(str, i)))

def checkOpenDoor(grid):
    global rooms

    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if 1 in grid[row][column]:
                Door          = ['', 'up', 'right', 'down', 'left']
                OpenDoorIndex = [i for i in range(len(grid[row][column])) if grid[row][column][i]==1]
                OpenDoor      = []
                RoomKind      = ["(Start)           ",
                                 "(Basic room)      ",
                                 "(Event room)      ",
                                 "(TreasureBox room)",
                                 "(Exit)            "
                                ]
                while len(OpenDoorIndex) > 0:
                    for j in range(len(Door)):
                        if Door[j] == Door[OpenDoorIndex[0]]:
                            OpenDoor.append(Door[OpenDoorIndex[0]])
                            OpenDoorIndex.remove(OpenDoorIndex[0])
                            break
                print(f"The door located at \033[31my : {row}, x : {column} {RoomKind[rooms.index(grid[row][column][0])]}\033[0m is open to the \033[32m{' and '.join(map(str, OpenDoor))}\033[0m")

def showProgress():
    global progress
    global Map
    global rooms

    MfS = Map[:]
    savedRoomGraphic = ''
    for i in range(len(progress)):
        clear()
        if i > 0:
            MfS[progress[i-1][0]][progress[i-1][1]][0] = savedRoomGraphic
            savedRoomGraphic                           = MfS[progress[i][0]][progress[i][1]][0]
            MfS[4][4][0]                               = rooms[0]
        print(progress[i])
        print(f"Data : {Map[progress[i][0]][progress[i][1]]}")
        MfS[progress[i][0]][progress[i][1]][0]         = f"\033[45m{MfS[progress[i][0]][progress[i][1]][0]}\033[0m"
        gridPrint(GraphicMaker(MfS))
        time.sleep(1)


def initBranch(Map):
    global x, y
    global rooms
    global direction
    global progress

    nowLength                                        = 0
    maxBranchLength                                  = random.randrange(9, 17)
    maxEventRoomCount, nowEventRoomCount             = random.randrange(1, 3), 0
    maxTreasureBoxRoomCount, nowTreasureBoxRoomCount = 1, 0
    bfx, bfy = 0, 0

    def getBack(e, bfx, bfy):
        global x, y
        e -= 1
        x, y = bfx, bfy

    while nowLength < maxBranchLength:    
        bfx, bfy = x, y
#                        | 0 | 1 | 2 |
#         locationData = ['', 0, '']
#          └─ 0:axis, 1:movement, 2:direction
        possibility         = [['y', 1, 'U', 'D'], ['y', -1, 'D', 'U'], ['x', 1, 'L', 'R'], ['x', -1, 'R', 'L']]
        locationData        = possibility[random.randrange(0,4)]
        coordinateNamespace = {'x':x, 'y':y}
        exec(f"{locationData[0]}+={locationData[1]}", coordinateNamespace)
        x, y                = coordinateNamespace['x'], coordinateNamespace['y']

        if y > len(Map)-1 or y < 0 or x > len(Map[0])-1 or x < 0:
            getBack(nowLength, bfx, bfy)
            continue
        elif Map[y][x][0] in rooms:
            getBack(nowLength, bfx, bfy)
            continue
        
        selectRoomKind = random.randrange(1, 4) # 방 종류 설정
        if selectRoomKind == 2: # 이벤트 방
            if nowEventRoomCount >= maxEventRoomCount:
                selectRoomKind = 1
                print(f"\033[32mEventroom\033[0m was changed in \033[31mnowLength:{nowLength} [{y}, {x}]\033[0m")
            else: nowEventRoomCount += 1
        elif selectRoomKind in [3, 4]: # 보물 방
            if nowTreasureBoxRoomCount >= maxTreasureBoxRoomCount:
                selectRoomKind = 1
                print(f"\033[33mTreasureBoxroom\033[0m was changed in \033[31mnowLength:{nowLength} [{y}, {x}]\033[0m")
            else: nowTreasureBoxRoomCount += 1
        else: selectRoomKind = 1
        if maxBranchLength - nowLength == 1: selectRoomKind = 4 # 출구 & 보스방
        Map[y][x][0]                              = rooms[selectRoomKind]
        nowLength                                += 1
        Map[y][x][direction[locationData[2]]]     = 1
        Map[bfy][bfx][direction[locationData[3]]] = 1
        progress.append([y, x])
    return GraphicMaker(Map)

# gridPrint(initBranch(Map))
# print(f"{rooms[0]} = start\n{rooms[1]} = basic room\n{rooms[2]} = event room\n{rooms[3]} = treasurebox room\n{rooms[4]} = exit\n")
# checkOpenDoor(Map)

# input("\nSee progress__")
# showProgress()