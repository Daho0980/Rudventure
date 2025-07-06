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

def getMap(grid:list, blank:int=0) -> str:
    blanks = " "*blank
    output = []

    DisplayMap    = []
    subDisplayMap = []

    for _ in range(9):
        DisplayMap   .append([' ']*9)
        subDisplayMap.append([' ']*8)

    toolY, toolX = 4-s.Dy, 4-s.Dx
    rowLength    = len(DisplayMap)

    for row in range(rowLength):
        for column in range(len(DisplayMap[row])):
            currRoom = grid[row][column]
            CRIS     = s.DungeonMap[row][column]

            FixY, FixX = row+toolY, column+toolX

            if  0 <= FixY <= rowLength-1\
            and 0 <= FixX <= len(DisplayMap[row])-1\
            and len(currRoom) > 0:      
                if  FixX  <len(DisplayMap[row])-1\
                and column<len(DisplayMap[row])-1:
                    if grid[row][column+1]:
                        if (
                            currRoom['doors']['R']\
                            and currRoom['isPlayerVisited']==2
                        ) or (
                            grid[row][column+1]['doors']['L']\
                            and grid[row][column+1]['isPlayerVisited']==2
                        ):
                            subDisplayMap[FixY][FixX] = '═'

                if row==s.Dy and column==s.Dx:
                    DisplayMap[FixY][FixX] = f"{cc['bg']['F']}{s.DungeonMap[s.Dy][s.Dx][0]}{cc['end']}"
                else:
                    match currRoom['isPlayerVisited']:
                        case 0: DisplayMap[FixY][FixX] = ' '
                        case 1: DisplayMap[FixY][FixX] = f"{cc['fg']['F']}?{cc['end']}"
                        case 2:
                            DisplayMap[FixY][FixX] = f"{''
                                    if not CRIS[1]
                                else cc['fg'][CRIS[1]]
                            }{CRIS[0]}{cc['end']}"
        
    for index, mainline in enumerate(DisplayMap):
        output.append(blanks+joineach(mainline,subDisplayMap[index])+blanks+('\n'if index!=rowLength-1 else""))

    return ''.join(output)

def DungeonMaker(showAll=False) -> list:
    output = []

    s.DungeonMap = []

    while 1:
        output = []
        for r in range(9):
            output.append([])
            s.DungeonMap.append([])
            for _ in range(9):
                output[r].append({
                    "name"            : None                        ,
                    "room"            : []                          ,
                    "doors"           : {'U':0, 'R':0, 'D':0, 'L':0},
                    "roomType"        : None                        ,
                    "isPlayerHere"    : False                       ,
                    "isPlayerVisited" : 0                           ,
                    "summonData"      : []                          ,
                    "interaction"     : False
                    })
                
                s.DungeonMap[r].append((" ", ""))

        output[4][4]['roomType']        = "startPoint"
        output[4][4]['isPlayerVisited'] = 2
        output[4][4]['isPlayerHere']    = True
        output[4][4]['interaction']     = True

        s.DungeonMap[4][4] = rData[0]

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
        elif "endPoint" in (
            "startPoint" if s.Dy==0 or not output[s.Dy-1][s.Dx] else output[3][4]['roomType'],
            "startPoint" if s.Dx==8 or not output[s.Dy][s.Dx+1] else output[4][5]['roomType'],
            "startPoint" if s.Dy==8 or not output[s.Dy+1][s.Dx] else output[5][4]['roomType'],
            "startPoint" if s.Dx==0 or not output[s.Dy][s.Dx-1] else output[4][3]['roomType']
        ): continue

        break


    for roomPos, doorDirection in zip(
        [[4-1, 4], [4, 4+1], [4+1, 4], [4, 4-1]],
        list(output[4][4]["doors"].values())
    ):
        if doorDirection: output[roomPos[0]][roomPos[1]]["isPlayerVisited"] = 1

    return output
