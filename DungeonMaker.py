import random
import time
import copy
import os
from Packages.lib.data import status, rooms

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
        for j in range(len(MapData[i])):
            if len(MapData[i][j]) > 0: grid[i].append(MapData[i][j]["roomIcon"])
            else                     : grid[i].append(' ')

    return grid

for i in range(9):
    Map.append([])
    for j in range(9): Map[i].append({"room":[], "roomIcon":' ', "doorPos":{"U":0, "R":0, "D":0, "L":0}, "roomType":None, "isPlayerHere":False, "isPlayerVisited":False})

x, y                  = 4, 4
roomIcons             = ['\033[31m§\033[0m', '•', '\033[32m*\033[0m', '\033[33m!\033[0m', '\033[34m/\033[0m']
Map[y][x]["roomIcon"] = roomIcons[0]
Map[y][x]["roomType"] = 0

def gridPrint(grid):
    for i in grid: print(' '.join(map(str, i)))

def returnBlankDataInRawMap(grid):
    for row in range(len(grid)):
        for column in range(len(grid[row])): grid[row][column] = {} if grid[row][column]['roomType'] == None else grid[row][column]

    return grid

def checkOpenDoor(grid):
    global roomIcons

    print("code running")

    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column]["roomType"] != None:
                Door          = ['up', 'right', 'down', 'left']
                DoorIndexChar, DoorIndex = ['U', 'R', 'D', 'L'], [0, 1, 2, 3]
                OpenDoorIndex = []
                OpenDoor      = []
                RoomKind      = ["(Start)           ",
                                 "(Basic room)      ",
                                 "(Event room)      ",
                                 "(TreasureBox room)",
                                 "(Exit)            "
                                ]
                for i in range(len(grid[row][column]["doorPos"])):
                    if grid[row][column]["doorPos"][DoorIndexChar[i]] == 1: OpenDoorIndex.append(DoorIndex[i])

                while len(OpenDoorIndex) > 0:
                    for j in range(len(Door)):
                        if Door[j] == Door[OpenDoorIndex[0]]:
                            OpenDoor.append(Door[OpenDoorIndex[0]])
                            OpenDoorIndex.remove(OpenDoorIndex[0])
                            break
                print(f"The door located at \033[31my : {row}, x : {column} {RoomKind[grid[row][column]['roomType']]}\033[0m is open to the \033[32m{' and '.join(map(str, OpenDoor))}\033[0m")

def showProgress():
    global progress
    global Map
    global roomIcons

    MfS = copy.deepcopy(Map)
    savedRoomGraphic = ''
    for i in range(len(progress)):
        clear()
        if i > 0:
            MfS[progress[i-1][0]][progress[i-1][1]]["roomIcon"] = savedRoomGraphic
            savedRoomGraphic                                = MfS[progress[i][0]][progress[i][1]]["roomIcon"]
            MfS[4][4]["roomIcon"]                               = roomIcons[0]
        print(progress[i])
        print(f"Data : {Map[progress[i][0]][progress[i][1]]}")
        MfS[progress[i][0]][progress[i][1]]["roomIcon"]         = f'\033[45m{MfS[progress[i][0]][progress[i][1]]["roomIcon"]}\033[0m'
        gridPrint(GraphicMaker(MfS))
        time.sleep(1)

def makeRoom(Map):
    output = copy.deepcopy(Map)

    for row in range(len(output)):
        for column in range(len(output[row])):
            if len(output[row][column]) > 0:
                baseMap   = copy.deepcopy(rooms.Room)
                RDP = list(output[row][column]["doorPos"].values())
                GRDP   = [[0, 7], [7, 14], [14, 7], [7, 0]]

                for DIE in range(len(RDP)):
                    baseMap[GRDP[DIE][0]][GRDP[DIE][1]] = status.R if RDP[DIE] == 1 else status.wall
                
                output[row][column]["room"] = baseMap
    return output

def initBranch(Map, rawPrint=False):
    global y, x
    global roomIcons
    global direction
    global progress

    nowLength                                        = 0
    maxBranchLength                                  = random.randrange(9, 17)
    maxEventRoomCount, nowEventRoomCount             = random.randrange(1, 3), 0
    maxTreasureBoxRoomCount, nowTreasureBoxRoomCount = 1, 0
    bfx, bfy = 0, 0

    def getBack(bfx, bfy):
        global x, y
        x, y       = bfx, bfy

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

        if y > len(Map)-1 or y < 0 or x > len(Map[0])-1 or x < 0: # 맵 탈출(outOfRangeError) 방지
            getBack(bfx, bfy)
            continue
        if Map[y][x]["roomIcon"] in roomIcons: # 방 덮어쓰기 방지
            p = [[y-1 if y>0 else y, x], [y+1 if y<len(Map)-1 else y, x], [y, x-1 if x>0 else x], [y, x+1 if x<len(Map[0])-1 else x]]
            if None not in [Map[p[0][0]][p[0][1]]['roomType'], Map[p[1][0]][p[1][1]]['roomType'], Map[p[2][0]][p[2][1]]['roomType'], Map[p[3][0]][p[3][1]]['roomType']]:
                Map[y][x] = {"roomIcon":roomIcons[4], "doorPos":Map[y][x]['doorPos'], "roomType":4, "isPlayerHere":False, "isPlayerVisited":False}
                break
            getBack(bfx, bfy)
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
        Map[y][x]["roomIcon"]                         = roomIcons[selectRoomKind]
        Map[y][x]["roomType"]                     = selectRoomKind
        Map[y][x]["doorPos"][locationData[2]]     = 1
        Map[bfy][bfx]["doorPos"][locationData[3]] = 1
        nowLength                                += 1
        progress.append([y, x])

    if rawPrint == False: return GraphicMaker(Map)
    else                : return Map

# a = initBranch(Map, rawPrint=True)
# gridPrint(GraphicMaker(a))
# print(f"{roomIcons[0]} = start\n{roomIcons[1]} = basic room\n{roomIcons[2]} = event room\n{roomIcons[3]} = treasurebox room\n{roomIcons[4]} = exit\n")
# checkOpenDoor(Map)

# input("\nSee progress__")
# showProgress()

# input("\nSee raw map data__")
# print(returnBlankDataInRawMap(a))

# input("\nSee all Map Rooms__")
# testVar = makeRoom(Map)
# for i in range(len(testVar)):
#     for j in range(len(testVar[i])):
#         clear()
#         if len(testVar[i][j]) > 0: print(f"\n\ny : {i}, x : {j}\ndoors : {Map[i][j]['doorPos']}\nType : {Map[i][j]['roomIcon']}, {Map[i][j]['roomType']}\n\n"); gridPrint(testVar[i][j]["room"]); input("check__")