from Assets.data                               import status  as s
from Assets.data.color                         import cColors as cc
from Game.utils.advanced.DungeonMaker.roomData import data    as rData

from Assets.data import (
    percentage,
    status
    )
from Game.utils.advanced.DungeonMaker.algorithms import (
    snake
)
from Game.utils.advanced.DungeonMaker.tools import (
    deleteBlankData,
    graphicMaker,
    makeRoom
)


s   = status
per = percentage

Map = []

def gridMapReturn(grid:list, blank:int=0, center:bool=False):
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
                    if row == s.Dy and column == s.Dx: DisplayMap[FixY][FixX] = f"{cc['bg']['F']}{grid[s.Dy][s.Dx]['roomIcon'][0]}{cc['end']}"
                    else:
                        match grid[row][column]['isPlayerVisited']:
                            case 0: DisplayMap[FixY][FixX] = ' '
                            case 1: DisplayMap[FixY][FixX] = f"{cc['fg']['F']}?{cc['end']}"
                            case 2: DisplayMap[FixY][FixX] = f"{'' if not grid[row][column]['roomIcon'][1] else cc['fg'][grid[row][column]['roomIcon'][1]]}{grid[row][column]['roomIcon'][0]}{cc['end']}"

    elif center == False:
        DisplayMap = graphicMaker(grid)

        DisplayMap[s.Dy][s.Dx] = f"{cc['bg']['F']}{DisplayMap[s.Dy][s.Dx]}{cc['end']}"
        for row in range(len(DisplayMap)):
            for column in range(len(DisplayMap[row])):
                if len(grid[row][column]) > 0:
                    match grid[row][column]['isPlayerVisited']:
                        case 0: DisplayMap[row][column] = ' '
                        case 1: DisplayMap[row][column] = f"{cc['fg']['F']}?{cc['end']}"

    for i in range(len(DisplayMap)):
        output += (blanks+' '.join(map(str, DisplayMap[i]))+blanks+"\n" if i != len(DisplayMap)-1 else blanks+' '.join(map(str, DisplayMap[i]))+blanks)

    return output

def DungeonMaker(showAll=False) -> list:
    output = []

    while 1:
        output = []
        for r in range(9):
            output.append([])
            for _ in range(9):
                output[r].append({
                    "room"            : [],
                    "roomIcon"        : [" ", ""],
                    "doorPos"         : {"U":0, "R":0, "D":0, "L":0},
                    "roomType"        : None,
                    "isPlayerHere"    : False,
                    "isPlayerVisited" : 0,
                    "summonCount"     : 0,
                    "interaction"     : False
                    })

        output[4][4]['roomIcon']        = rData[0]
        output[4][4]['roomType']        = 0
        output[4][4]['isPlayerVisited'] = 2
        output[4][4]['isPlayerHere']    = True
        output[4][4]['interaction']     = True

        output = makeRoom(deleteBlankData(snake.main(output, 4, 4, rawPrint=True, showAll=showAll)))

        isStartExist = False

        if not output: continue
        for r in range(9):
            for c in range(9):
                if output[r][c] and output[r][c]['roomType'] == 0:
                    isStartExist = True
                    s.Dy, s.Dx   = r, c
                    break

        if   not isStartExist: continue
        elif 4 in [
            0 if s.Dy == 0 or not output[s.Dy-1][s.Dx] else output[3][4]['roomType'],
            0 if s.Dx == 8 or not output[s.Dy][s.Dx+1] else output[4][5]['roomType'],
            0 if s.Dy == 8 or not output[s.Dy+1][s.Dx] else output[5][4]['roomType'],
            0 if s.Dx == 0 or not output[s.Dy][s.Dx-1] else output[4][3]['roomType']
        ]: continue
        break


    for roomPos, doorDirection in zip([[4-1, 4], [4, 4+1], [4+1, 4], [4, 4-1]], list(output[4][4]["doorPos"].values())):
        if doorDirection: output[roomPos[0]][roomPos[1]]["isPlayerVisited"] = 1

    return output
