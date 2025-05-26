from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from Game.utils.CExt.libtext import joineach

from .roomData   import data as rData
from .algorithms import snake

from .tools import (
    deleteBlankData,
    makeRoom
)


Map = []

def centerGridMapReturn(grid:list, blank:int=0):
    """
    `GraphicMaker`함수로 그래픽만 남은 맵이나 맵 데이터로 맵의 세부 데이터를 추가하는 함수
    
        `grid`(list(2d), list(raw)) : `GraphicMaker`함수로 그래픽만 남은 맵이나 맵 데이터가 포함됨, 무조건 기입해야 함
        `blank`(int)                : 맵의 옆으로 추가될 공백칸 길이, 기본적으로 `0`으로 설정되어 있음
    """
    blanks = " "*blank
    output = []

    DisplayMap    = []
    subDisplayMap = []

    for _ in range(9):
        DisplayMap.append([' ']*9)
        subDisplayMap.append([' ']*8)

    toolY, toolX = 4-s.Dy, 4-s.Dx
    rowLength    = len(DisplayMap)

    for row in range(rowLength):
        for column in range(len(DisplayMap[row])):
            FixY, FixX = row+toolY, column+toolX

            if  0 <= FixY <= rowLength-1\
            and 0 <= FixX <= len(DisplayMap[row])-1\
            and len(grid[row][column]) >  0:      
                if  FixX  <len(DisplayMap[row])-1\
                and column<len(DisplayMap[row])-1:
                    if grid[row][column+1]:
                        if  (
                            grid[row][column]['doors']['R']\
                            and grid[row][column]['isPlayerVisited']==2
                        ) or (
                            grid[row][column+1]['doors']['L']\
                            and grid[row][column+1]['isPlayerVisited']==2
                        ):
                            subDisplayMap[FixY][FixX] = '═'

                if row==s.Dy and column==s.Dx:
                    DisplayMap[FixY][FixX] = f"{cc['bg']['F']}{grid[s.Dy][s.Dx]['roomIcon'][0]}{cc['end']}"
                else:
                    match grid[row][column]['isPlayerVisited']:
                        case 0: DisplayMap[FixY][FixX] = ' '
                        case 1: DisplayMap[FixY][FixX] = f"{cc['fg']['F']}?{cc['end']}"
                        case 2:
                            DisplayMap[FixY][FixX] = f"{''
                                    if not grid[row][column]['roomIcon'][1]
                                else cc['fg'][grid[row][column]['roomIcon'][1]]
                            }{grid[row][column]['roomIcon'][0]}{cc['end']}"
        
    for index, mainline in enumerate(DisplayMap):
        output.append(blanks+joineach(mainline,subDisplayMap[index])+blanks+('\n'if index!=rowLength-1 else""))

    return ''.join(output)

def DungeonMaker(showAll=False) -> list:
    output = []

    while 1:
        output = []
        for r in range(9):
            output.append([])
            for _ in range(9):
                output[r].append({
                    "name"            : None                        ,
                    "room"            : []                          ,
                    "roomIcon"        : [" ", ""]                   ,
                    "doors"           : {"U":0, "R":0, "D":0, "L":0},
                    "roomType"        : None                        ,
                    "isPlayerHere"    : False                       ,
                    "isPlayerVisited" : 0                           ,
                    "summonData"      : []                           ,
                    "interaction"     : False
                    })

        output[4][4]['roomIcon']        = rData[0]
        output[4][4]['roomType']        = "startPoint"
        output[4][4]['isPlayerVisited'] = 2
        output[4][4]['isPlayerHere']    = True
        output[4][4]['interaction']     = True

        output = makeRoom(
            deleteBlankData(
                snake.main(
                    output, 4, 4,
                    rawPrint=True,
                    showAll =showAll
                )
            )
        )

        isStartExist = False

        if not output: continue
        for r in range(9):
            for c in range(9):
                if output[r][c] and output[r][c]['roomType'] == "startPoint":
                    isStartExist = True
                    s.Dy, s.Dx   = r, c
                    break

        if   not isStartExist: continue
        elif "endPoint" in [
            "startPoint" if s.Dy==0 or not output[s.Dy-1][s.Dx] else output[3][4]['roomType'],
            "startPoint" if s.Dx==8 or not output[s.Dy][s.Dx+1] else output[4][5]['roomType'],
            "startPoint" if s.Dy==8 or not output[s.Dy+1][s.Dx] else output[5][4]['roomType'],
            "startPoint" if s.Dx==0 or not output[s.Dy][s.Dx-1] else output[4][3]['roomType']
        ]: continue
        break


    for roomPos, doorDirection in zip(
        [[4-1, 4], [4, 4+1], [4+1, 4], [4, 4-1]],
        list(output[4][4]["doors"].values())
    ):
        if doorDirection: output[roomPos[0]][roomPos[1]]["isPlayerVisited"] = 1

    return output
