"""
던전 랜덤 생성 모듈

    그래픽 관련:
        ``GraphicMaker``        : 맵의 데이터에서 방 아이콘만 빼내 그래픽을 출력하기 쉽게 하기 위해 만든 함수
        ``gridMapReturn``       : `GraphicMaker`함수로 그래픽만 남은 맵이나 맵 데이터로 맵의 세부 데이터를 추가하는 함수

        사용하지 않는 것들:
            ``checkOpenDoor``(dead) : 맵 데이터를 탐색해 각 방 당 열린 문의 위치를 출력하는 함수, 현재는 사용하지 않음
            ``showProgreess``(dead) : global 리스트인 `progress`를 이용해 `GraphicMaker`함수로 그래픽만 남은 맵에서 진행 경로를 출력하는 함수, 현재는 문이 여러 개가 될 확률이 생겼고, 별로 쓸 이유가 없으므로 현재는 사용하지 않음

    맵 툴 관련:
        ``initBranch``         : 처음으로 맵 데이터를 작성하고 기초를 다지는 함수, 이 프로그램의 핵심 알고리즘이 포함됨
        ``deleteBlankData``    : 맵의 데이터 중 쓸데없이 메모리만 차지하는 공백 데이터를 제거하는 함수
        ``makeRoom``           : `deleteBlankData`함수로 수정된 맵 데이터 중 "room" 데이터를 추가하는 함수, 맵 데이터 중 "doors"도 활용함
        ``DungeonMaker``       : `initBranch.Map`의 기본 틀을 제공하고, `deleteBlankData`, `makeRoom`함수를 사용해 완벽하게 편집된 맵 데이터를 반환하는 함수
"""

import re
import copy
import random
from   Assets.data import rooms,  status
from   Game.utils  import graphic

grp = graphic
s   = status
cc  = s.cColors

Map       = []
direction = {
    'U' : 1,
    'R' : 2,
    'D' : 3,
    'L' : 4
}
roomIcons = [
    f"{cc['fg']['R']}§{cc['end']}",
    "•",
    f"{cc['fg']['L']}*{cc['end']}",
    f"{cc['fg']['Y']}!{cc['end']}",
    f"{cc['fg']['B1']}/{cc['end']}"
    ]

# ---------- Graphic section ----------
escapeAnsi = lambda line: re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('', line)

def GraphicMaker(MapData:list):
    """
    맵의 데이터에서 방 아이콘만 빼내 그래픽을 출력하기 쉽게 하기 위해 만든 함수

        `MapData`(list(2d)) : `deleteBlankData`함수로 공백칸을 제거한 맵이 포함됨, 무조건 기입해야 함
    """
    grid = []
    for i in range(len(MapData)):
        grid.append([])
        for j in range(len(MapData[i])):
            if len(MapData[i][j]) > 0: grid[i].append(MapData[i][j]["roomIcon"])
            else                     : grid[i].append(' ')

    return grid

def gridMapReturn(grid:list, blank=0, center=False):
    """
    `GraphicMaker`함수로 그래픽만 남은 맵이나 맵 데이터로 맵의 세부 데이터를 추가하는 함수
    
        `grid`(list(2d), list(raw)) : `GraphicMaker`함수로 그래픽만 남은 맵이나 맵 데이터가 포함됨, 무조건 기입해야 함
        `blank`(int)                : 맵의 옆으로 추가될 공백칸 길이, 기본적으로 `0`으로 설정되어 있음
        `center`(bool)              : 현재 플레이어가 위치한 방을 중간으로 설정할지에 대한 여부, 기본적으로 `False`로 설정되어 있음
    """
    blanks = " "*blank
    output = ""

    if center == True:
        DisplayMap = []
        for row in range(9):
            DisplayMap.append([" "]*9)
        toolY, toolX = 4-s.Dy, 4-s.Dx

        for row in range(len(DisplayMap)):
            for column in range(len(DisplayMap[row])):
                FixY, FixX = row+toolY, column+toolX
                if FixY >= 0 and FixY <= len(DisplayMap)-1 and FixX >= 0 and FixX <= len(DisplayMap[row])-1 and len(grid[row][column]) > 0:
                    if row == s.Dy and column == s.Dx: DisplayMap[FixY][FixX] = f"{cc['bg']['F']}{escapeAnsi(grid[s.Dy][s.Dx]['roomIcon'])}{cc['end']}"
                    else:
                        match grid[row][column]["isPlayerVisited"]:
                            case 0: DisplayMap[FixY][FixX] = ' '
                            case 1: DisplayMap[FixY][FixX] = f"{cc['fg']['F']}?{cc['end']}"
                            case 2: DisplayMap[FixY][FixX] = grid[row][column]["roomIcon"]

    elif center == False:
        DisplayMap = GraphicMaker(grid)

        DisplayMap[s.Dy][s.Dx] = f"{cc['bg']['F']}{DisplayMap[s.Dy][s.Dx]}{cc['end']}"
        for row in range(len(DisplayMap)):
            for column in range(len(DisplayMap[row])):
                if len(grid[row][column]) > 0:
                    match grid[row][column]["isPlayerVisited"]:
                        case 0: DisplayMap[row][column] = ' '
                        case 1: DisplayMap[row][column] = f"{cc['fg']['F']}?{cc['end']}"

    for i in range(len(DisplayMap)): output += blanks+' '.join(map(str, DisplayMap[i]))+blanks+"\n" if i != len(DisplayMap)-1 else blanks+' '.join(map(str, DisplayMap[i]))+blanks

    return output

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 이거 안씀 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# def checkOpenDoor(grid:list):
#     """
#     맵 데이터를 탐색해 각 방 당 열린 문의 위치를 출력하는 함수, 현재는 사용하지 않음
    
#         `grid`(list(raw)) : 맵 데이터가 포함됨, 무조건 기입해야 함
#     """
#     global roomIcons

#     print("code running")

#     for row in range(len(grid)):
#         for column in range(len(grid[row])):
#             if grid[row][column]["roomType"] != None:
#                 Door                     = ['up', 'right', 'down', 'left']
#                 DoorIndexChar, DoorIndex = ['U', 'R', 'D', 'L'], [0, 1, 2, 3]
#                 OpenDoorIndex            = []
#                 OpenDoor                 = []
#                 RoomKind                 = ["(Start)           ",
#                                             "(Basic room)      ",
#                                             "(Event room)      ",
#                                             "(TreasureBox room)",
#                                             "(Exit)            "
#                                            ]
#                 for i in range(len(grid[row][column]["doorPos"])):
#                     if grid[row][column]["doorPos"][DoorIndexChar[i]] == 1: OpenDoorIndex.append(DoorIndex[i])

#                 while len(OpenDoorIndex) > 0:
#                     for j in range(len(Door)):
#                         if Door[j] == Door[OpenDoorIndex[0]]:
#                             OpenDoor.append(Door[OpenDoorIndex[0]])
#                             OpenDoorIndex.remove(OpenDoorIndex[0])
#                             break
#                 print(f"The door located at \033[31my : {row}, x : {column} {RoomKind[grid[row][column]['roomType']]}\033[0m is open to the \033[32m{' and '.join(map(str, OpenDoor))}\033[0m")

# def showProgress(Data:list):
#     """
#     global 리스트인 `progress`를 이용해 `GraphicMaker`함수로 그래픽만 남은 맵에서 진행 경로를 출력하는 함수, 현재는 문이 여러 개가 될 확률이 생겼고, 별로 쓸 이유가 없으므로 현재는 사용하지 않음
    
#         `Data`(list(2d)) : `GraphicMaker`함수로 그래픽만 남은 맵이 포함됨, 무조건 기입해야 함
#     """
#     global roomIcons

#     Map, progress    = Data[0], Data[1]
#     MfS              = copy.deepcopy(Map)
#     savedRoomGraphic = ''
#     for i in range(len(progress)):
#         from Packages.lib.system import globalFunctions as gbf
#         gbf.clear()
#         if i > 0:
#             MfS[progress[i-1][0]][progress[i-1][1]]["roomIcon"] = savedRoomGraphic
#             savedRoomGraphic                                = MfS[progress[i][0]][progress[i][1]]["roomIcon"]
#             MfS[4][4]["roomIcon"]                               = roomIcons[0]

#         print(progress[i])
#         print(f"Data : {Map[progress[i][0]][progress[i][1]]}")
#         MfS[progress[i][0]][progress[i][1]]["roomIcon"]         = f'\033[45m{MfS[progress[i][0]][progress[i][1]]["roomIcon"]}\033[0m'
#         gridMapReturn(MfS)
#         time.sleep(1)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 이거 안씀 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ---------- Init section ----------
def makeRoom(Map:list):
    """
    `deleteBlankData`함수로 수정된 맵 데이터 중 "room" 데이터를 추가하는 함수, 맵 데이터 중 "doors"도 활용함

        `Map`(list(raw)) : `deleteBlankData`함수로 수정된 맵이 포함됨, 무조건 기입해야 함
    """
    if not Map: return Map

    output = copy.deepcopy(Map)

    # 방 생성
    for row in range(len(output)):
        for column in range(len(output[row])):
            if len(output[row][column]) > 0:
                baseMap = copy.deepcopy(rooms.Room1)
                RDP     = list(output[row][column]["doorPos"].values())
                GRDP    = [[0, 6], [6, 12], [12, 6], [6, 0]]

                for DIE in range(len(RDP)):
                    if RDP[DIE] == 1:
                        baseMap[GRDP[DIE][0]][GRDP[DIE][1]] = {"block":s.ids[2], "id":2}
                        if DIE in [0, 2]:
                            baseMap[GRDP[DIE][0]][GRDP[DIE][1]-1], baseMap[GRDP[DIE][0]][GRDP[DIE][1]+1] = {"block":s.ids[2], "id":2}, {"block":s.ids[2], "id":2}
                        elif DIE in [1, 3]:
                            baseMap[GRDP[DIE][0]-1][GRDP[DIE][1]], baseMap[GRDP[DIE][0]+1][GRDP[DIE][1]] = {"block":s.ids[2], "id":2}, {"block":s.ids[2], "id":2}

                output[row][column]["room"] = baseMap

    for row in range(len(output)):
        for column in range(len(output[row])):
            if len(output[row][column]) > 0:
                if output[row][column] and output[row][column]["roomType"] == 4: continue

                DPG        = {'U':[0, 6], 'R':[6, 12], 'D':[12, 6], 'L':[6, 0]}
                p          = [[row-1 if row>0 else row, column], [row+1 if row<len(output)-1 else row, column], [row, column-1 if column>0 else column], [row, column+1 if column<len(output[0])-1 else column]]
                dp         = [['U', 'D'], ['D', 'U'], ['L', 'R'], ['R', 'L']]
                doorValues = list(output[row][column]['doorPos'].values())
                grd        = [[DPG['U'], DPG['D']], [DPG['D'], DPG['U']], [DPG['L'], DPG['R']], [DPG['R'], DPG['L']]]

                while [row, column] in p:
                    del dp        [p.index([row, column])]
                    del doorValues[p.index([row, column])]
                    del grd       [p.index([row, column])]
                    del p         [p.index([row, column])]
                while 1 in doorValues:
                    del p         [doorValues.index(1)]
                    del dp        [doorValues.index(1)]
                    del grd       [doorValues.index(1)]
                    del doorValues[doorValues.index(1)]
                
                for i in range(len(p)):
                    if len(output[p[i][0]][p[i][1]]) > 0 and output[p[i][0]][p[i][1]]["roomType"] != 4 and not random.randrange(0, 3):
                        output[row][column]['doorPos'][dp[i][0]]      = 1
                        output[p[i][0]][p[i][1]]['doorPos'][dp[i][1]] = 1

                        output[row][column]['room'][grd[i][0][0]][grd[i][0][1]] = {"block":s.ids[2], "id":2}
                        if dp[i][0] in ['U', 'D']:
                            output[row][column]['room'][grd[i][0][0]][grd[i][0][1]-1], output[row][column]['room'][grd[i][0][0]][grd[i][0][1]+1] = {"block":s.ids[2], "id":2}, {"block":s.ids[2], "id":2}
                        elif dp[i][0] in ['L', 'R']:
                            output[row][column]['room'][grd[i][0][0]-1][grd[i][0][1]], output[row][column]['room'][grd[i][0][0]+1][grd[i][0][1]] = {"block":s.ids[2], "id":2}, {"block":s.ids[2], "id":2}

                        output[p[i][0]][p[i][1]]['room'][grd[i][1][0]][grd[i][1][1]] = {"block":s.ids[2], "id":2}
                        if dp[i][0] in ['U', 'D']:
                            output[p[i][0]][p[i][1]]['room'][grd[i][1][0]][grd[i][1][1]-1], output[p[i][0]][p[i][1]]['room'][grd[i][1][0]][grd[i][1][1]+1] = {"block":s.ids[2], "id":2}, {"block":s.ids[2], "id":2}
                        elif dp[i][0] in ['L', 'R']:
                            output[p[i][0]][p[i][1]]['room'][grd[i][1][0]-1][grd[i][1][1]], output[p[i][0]][p[i][1]]['room'][grd[i][1][0]+1][grd[i][1][1]] = {"block":s.ids[2], "id":2}, {"block":s.ids[2], "id":2}
    return output

def deleteBlankData(grid:list):
    """
    맵의 데이터 중 쓸데없이 메모리만 차지하는 공백 데이터를 제거하는 함수
    
        `grid`(list(raw)) : `initBranch`함수로 생긴 맵 데이터가 포함됨, 무조건 기입해야 함
    """
    if not grid: return grid
    # 비어있는 잉여 데이터 정리
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            grid[row][column] = {} if grid[row][column]['roomType'] == None else grid[row][column]

    return grid

def initBranch(Map:list, y:int, x:int, rawPrint=False, showAll=False):
    """
    처음으로 맵 데이터를 작성하고 기초를 다지는 함수, 이 프로그램의 핵심 알고리즘이 포함됨
    
        `Map`(list(frame)) : 맵 데이터 작성 전 먼저 제작된 맵 데이터 틀이 포함됨, 무조건 기입해야 함
        `y`(int)           : 최초로 선언될 y값, 보통 맵의 중심인 4로 시작함
        `x`(int)           : 최초로 선언될 x값, 보통 맵의 중심인 4로 시작함
        `rawPrint`(bool)   : 맵 데이터를 그대로 보낼지에 대한 여부, 기본적으로 `False`로 설정되어 있음
    """
    global roomIcons
    global direction

    nowLength                                        = 0
    maxBranchLength                                  = random.randrange(9, 17)
    maxEventRoomCount, nowEventRoomCount             = random.randrange(1, 3), 0
    maxTreasureBoxRoomCount, nowTreasureBoxRoomCount = 1, 0
    bfx, bfy                                         = 0, 0
    possibility                                      = [['y', 1, 'U', 'D'], ['y', -1, 'D', 'U'], ['x', 1, 'L', 'R'], ['x', -1, 'R', 'L']]

    def getBack(bfx, bfy):
        nonlocal y, x
        y, x = bfy, bfx

    endCount = 0
    while nowLength < maxBranchLength:
        bfy, bfx = y, x
#         locationData = ['', 0, '']
#                        └─> 0:axis, 1:movement, 2:direction
        locationData        = possibility[random.randrange(0,4)]
        coordinateNamespace = {'x':x, 'y':y}
        
        exec(f"{locationData[0]}+={locationData[1]}", coordinateNamespace)
        x, y = coordinateNamespace['x'], coordinateNamespace['y']

        if y > len(Map)-1 or y < 0 or x > len(Map[0])-1 or x < 0: # 맵 탈출(outOfRangeError) 방지
            getBack(bfx, bfy)
            continue
        if Map[y][x]["roomIcon"] in roomIcons: # 방 덮어쓰기 방지
            p = [
                [y-1    if y>0             else y, x],
                [y+1    if y<len(Map)-1    else y, x],
                [y, x-1 if x>0             else x   ],
                [y, x+1 if x<len(Map[0])-1 else x   ]
                ]
            if None not in [Map[p[0][0]][p[0][1]]['roomType'], Map[p[1][0]][p[1][1]]['roomType'], Map[p[2][0]][p[2][1]]['roomType'], Map[p[3][0]][p[3][1]]['roomType']] or\
                [y, x] in p:
                Map[y][x] = {
                    "roomIcon"       :roomIcons[4],
                    "doorPos"        :Map[y][x]['doorPos'],
                    "roomType"       :4,
                    "isPlayerHere"   :False,
                    "isPlayerVisited":2,
                    "summonCount"    :1,
                    "interaction"    :False
                    }
                break
            elif endCount >= 8:
                Map = False
                break
            getBack(bfx, bfy)
            endCount += 1
            continue
        endCount = 0

        match random.randrange(0, 2): # 방 종류 설정
            case 0: selectRoomKind = random.randrange(1, 4)
            case 1: selectRoomKind = random.randrange(5, 7)
        if maxBranchLength - nowLength == 1: selectRoomKind = 4 # 출구 & 보스방

        if selectRoomKind == 2: # 이벤트 방
            if nowEventRoomCount >= maxEventRoomCount: selectRoomKind = 1
                # f"\033[32mEventroom\033[0m was changed in \033[31mnowLength:{nowLength} [{y}, {x}]\033[0m"
            else: nowEventRoomCount += 1

        elif selectRoomKind in [3, 5]: # 보물 방
            selectRoomKind = 3
            if nowTreasureBoxRoomCount >= maxTreasureBoxRoomCount: selectRoomKind = 1
                # f"\033[33mTreasureBoxroom\033[0m was changed in \033[31mnowLength:{nowLength} [{y}, {x}]\033[0m"
            else: nowTreasureBoxRoomCount += 1

        elif selectRoomKind != 4: selectRoomKind = 1

        # 몬스터 summonCount 설정
        size    = 0
        percent = random.randrange(1,101)

        if percent <= 50                   : size = random.randrange(1, 5)
        elif percent > 50 and percent <= 95: size = random.randrange(5, 7)
        elif percent > 95                  : size = 7

        # 방 데이터 정리
        nowLength                                += 1
        Map[y][x]["roomIcon"]                     = roomIcons[selectRoomKind]
        Map[y][x]["roomType"]                     = selectRoomKind
        Map[y][x]["isPlayerVisited"]              = 2 if selectRoomKind == 4 or showAll == True else 0
        Map[y][x]["doorPos"][locationData[2]]     = 1
        Map[bfy][bfx]["doorPos"][locationData[3]] = 1
        Map[y][x]["summonCount"]                  = 1 if selectRoomKind == 4 else 0 if selectRoomKind in [2, 3] else size

    if rawPrint == False and Map: return GraphicMaker(Map)
    else:                         return Map

def DungeonMaker(showAll=False):
    """
    `initBranch.Map`의 기본 틀을 제공하고, `initBranch`, `deleteBlankData`, `makeRoom`함수를 사용해 완벽하게 편집된 맵 데이터를 반환하는 함수
    """     
    
    while 1:
        output = []
        # 맵의 기본 틀 생성
        for i in range(9):
            output.append([])
            for j in range(9):
                output[i].append({
                    "room":[],
                    "roomIcon":' ',
                    "doorPos":{"U":0, "R":0, "D":0, "L":0},
                    "roomType":None,
                    "isPlayerHere":False,
                    "isPlayerVisited":0,
                    "summonCount":0,
                    "interaction":False
                    })

        output[4][4]["roomIcon"]        = roomIcons[0]
        output[4][4]["roomType"]        = 0
        output[4][4]["isPlayerVisited"] = 2
        output[4][4]["isPlayerHere"]    = True
        output[4][4]["interaction"]     = True

        output        = makeRoom(deleteBlankData(initBranch(output, 4, 4, rawPrint=True, showAll=showAll)))
        if output: break
    SR            = [[4-1, 4], [4, 4+1], [4+1, 4], [4, 4-1]]
    doorPositions = list(output[4][4]["doorPos"].values())

    for i in range(4):
        if doorPositions[i]: output[SR[i][0]][SR[i][1]]["isPlayerVisited"] = 1

    return output


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
#         gbf.clear()
#         if len(testVar[i][j]) > 0: print(f"\n\ny : {i}, x : {j}\ndoors : {Map[i][j]['doorPos']}\nType : {Map[i][j]['roomIcon']}, {Map[i][j]['roomType']}\n\n"); gridPrint(testVar[i][j]["room"]); input("check__")