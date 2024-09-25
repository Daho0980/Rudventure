from random import randrange

from Assets.data                               import percentage  as per
from Game.utils.advanced.DungeonMaker.tools    import graphicMaker
from Game.utils.advanced.DungeonMaker.roomData import data        as rData


direction = {
    'U' : 1,
    'R' : 2,
    'D' : 3,
    'L' : 4
}

def main(Map:list,
         y:int,
         x:int,
         rawPrint:bool=False,
         showAll:bool =False ):
    """
    처음으로 맵 데이터를 작성하고 기초를 다지는 함수, 이 프로그램의 핵심 알고리즘이 포함됨
    
        `Map`(list(frame)) : 맵 데이터 작성 전 먼저 제작된 맵 데이터 틀이 포함됨, 무조건 기입해야 함
        `y`(int)           : 최초로 선언될 y값, 보통 맵의 중심인 4로 시작함
        `x`(int)           : 최초로 선언될 x값, 보통 맵의 중심인 4로 시작함
        `rawPrint`(bool)   : 맵 데이터를 그대로 보낼지에 대한 여부, 기본적으로 `False`로 설정되어 있음
    """
    global roomIcons
    global direction

    nowLength                                     = 0
    maxBranchLength                               = randrange(9, 17)
    maxEventRoomCount, eventRoomCount             = randrange(1, 3), 0
    maxTreasureBoxRoomCount, treasureBoxRoomCount = randrange(1, 3), 0
    bfx, bfy                                      = 0, 0
    possibility                                   = [['y', 1, 'U', 'D'], ['y', -1, 'D', 'U'], ['x', 1, 'L', 'R'], ['x', -1, 'R', 'L']]

    def getBack(bfx:int, bfy:int):
        nonlocal y, x
        y, x = bfy, bfx

    endCount = 0
    while nowLength < maxBranchLength:
        bfy, bfx = y, x
#         locationData = ['', 0, '']
#                        └─> 0:axis, 1:movement, 2:direction
        locationData        = possibility[randrange(0,4)]
        coordinateNamespace = {'x':x, 'y':y}
        roomKind            = 0
        
        exec(f"{locationData[0]}+={locationData[1]}", coordinateNamespace)
        x, y = coordinateNamespace['x'], coordinateNamespace['y']

        if y>len(Map)-1 or y<0 or x>len(Map[0])-1 or x<0: # 맵 탈출(outOfRangeError) 방지
            getBack(bfx, bfy)
            continue
        if Map[y][x]["roomIcon"] in rData: # 방 덮어쓰기 방지
            p = [
                [y-1    if y>0             else y, x],
                [y+1    if y<len(Map)-1    else y, x],
                [y, x-1 if x>0             else x   ],
                [y, x+1 if x<len(Map[0])-1 else x   ]
                ]
            if None not in [
                Map[p[0][0]][p[0][1]]['roomType'],
                Map[p[1][0]][p[1][1]]['roomType'],
                Map[p[2][0]][p[2][1]]['roomType'],
                Map[p[3][0]][p[3][1]]['roomType']] or\
                [y, x] in p:
                Map[y][x] = {
                    "roomIcon"        : rData[4],
                    "doorPos"         : Map[y][x]['doorPos'],
                    "roomType"        : 4,
                    "isPlayerHere"    : False,
                    "isPlayerVisited" : 2,
                    "summonCount"     : 1,
                    "interaction"     : False
                    }
                break
            elif endCount >= 8: Map = []; break
            
            getBack(bfx, bfy)
            endCount += 1
            continue
        endCount = 0

        match randrange(0, 2): # 방 종류 설정
            case 0: roomKind = randrange(1, 4)
            case 1: roomKind = randrange(5, 7)

        if maxBranchLength - nowLength == 1: roomKind = 4 # 출구 & 보스방

        if roomKind == 2: # 이벤트 방
            if eventRoomCount >= maxEventRoomCount: roomKind = 1
            else:
                eventRoomCount        += 1
                Map[y][x]['eventType'] = randrange(0, 6)

        elif roomKind in [3, 5]: # 보물 방
            roomKind = 3
            if treasureBoxRoomCount >= maxTreasureBoxRoomCount: roomKind = 1
            else:
                treasureBoxRoomCount += 1
                rewardP               = randrange(1, 101)

                if rewardP<=per.treasureBox['small']:                              rarity = 0
                elif per.treasureBox['small']<rewardP<=per.treasureBox['medium'] : rarity = 1
                else:                                                              rarity = 2

                Map[y][x]['treasureRarity'] = rarity

        elif roomKind != 4: roomKind = 1

        # 몬스터 summonCount 설정
        SCP  = randrange(1,101)
        size = randrange(1, 6)\
            if SCP<=per.monsterSpawnSize['small']\
            else randrange(6, 8) if SCP> per.monsterSpawnSize["small"]\
                 and SCP<=per.monsterSpawnSize['medium']\
            else 8

        # 방 데이터 정리
        nowLength                                += 1
        Map[y][x]['roomIcon']                     = rData[roomKind]
        Map[y][x]['roomType']                     = roomKind
        Map[y][x]['isPlayerVisited']              = 2 if roomKind == 4 or showAll == True else 0
        Map[y][x]['doorPos'][locationData[2]]     = 1
        Map[bfy][bfx]['doorPos'][locationData[3]] = 1
        Map[y][x]['summonCount']                  = 1 if roomKind == 4 else 0 if roomKind in [2, 3] else size

    if rawPrint == False and Map: return graphicMaker(Map)
    else:                         return Map