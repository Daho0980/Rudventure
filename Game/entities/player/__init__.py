import random, time
import curses
from   itertools import chain

from Assets.data          import rooms, status
from Assets.data.color    import cColors      as cc
from Game.core.system     import logger
from Game.entities.player import event
from Game.utils.system    import xpSystem


s, r = status, rooms

def set() -> None:
    s.hp       = 10
    s.df       = 5
    s.atk      = 1
    s.hunger   = 1000

    s.critRate = 10
    s.critDMG  = 10
    
    s.Mhp      = s.hp
    s.Mdf      = s.df
    s.Mxp      = 10

def start(Dy:int, Dx:int, y:int, x:int) -> None:
    s.Dungeon[Dy][Dx]['room'][y][x] = {"block":s.ids[300], "id":300}
    s.Dy, s.Dx, s.y, s.x            = Dy, Dx, y, x

def damage(block:str="?") -> None:
    event.hitted()
    if s.df > 0: s.df -= 1
    else       : s.hp -= 1

    if s.hp <= 0 and s.df <= 0:
        s.DROD = [f"{cc['fg']['R']}{random.choice(['과다출혈', '피로 과다', '졸도', '자살', '우울증'])}{cc['end']}", 'R']
    logger.addLog(f"{s.lightName}이(가) [ {block} ] 에 의해 상처입었습니다")

def itemEvent(y:int, x:int) -> None:
    percent   = random.randrange(1, 101)

    if   percent > 0  and percent <= 45: typeIndex = "hunger"
    elif percent > 45 and percent <= 70: typeIndex = "hp"
    elif percent > 70 and percent <= 80: typeIndex = "def"
    elif percent > 80 and percent <= 85: typeIndex = "atk"
    else: typeIndex = "exp"

    orbId = s.orbIds["type"][typeIndex][random.randrange(0, 2)]

    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = {"block" : s.ids[orbId], "id" : orbId}
        
def orbEvent(Size:int, Type:int) -> None:
    orbData   = [
        [3,   1],
        [3,   1],
        [2,   1],
        [50, 25],
        [5,   1]
    ]

    point:int = orbData[Type][Size]
    match Type:
        case 0: s.hp = s.Mhp if s.hp+point > s.Mhp else s.hp+point
        case 1: s.df = s.Mdf if s.df+point > s.Mdf else s.df+point

        case 2: s.atk    += point
        case 3: s.hunger += point

        case 4: xpSystem.getXP(point)


def move(Dir, Int:int) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    if s.df > 0: s.dfCrack = 0
    bfy, bfx   = s.y, s.x
    ty, tx     = s.y, s.x
    bfDy, bfDx = s.Dy, s.Dx

    match Dir:
        case curses.KEY_UP   : ty -= Int
        case curses.KEY_DOWN : ty += Int
        case curses.KEY_LEFT : tx -= Int
        case curses.KEY_RIGHT: tx += Int

    s.hunger -= 1

    if roomGrid[ty][tx]["id"] == -1: ty, tx = bfy, bfx

    if roomGrid[ty][tx]["id"] in [1, 3]:
        damage(roomGrid[ty][tx]["block"])

        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

        if s.df <= 0 and s.dfCrack <= 0:
            s.dfCrack = 1
            logger.addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")

    elif roomGrid[ty][tx]["id"] in s.enemyIds:

        s.hitPos.append([ty, tx])
        time.sleep(0.001)
        s.hitPos.remove([ty, tx])

        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    elif roomGrid[ty][tx]["id"] == 4:
        itemEvent(ty, tx)
        ty, tx = bfy, bfx

    elif roomGrid[ty][tx]["id"] in chain(s.orbIds["size"]["smallOne"], s.orbIds["size"]["bigOne"]):
        orbId = roomGrid[ty][tx]["id"]
        orbEvent(
            Size=0 if orbId in s.orbIds["size"]["bigOne"] else 1,
            Type=int(
                list(
                    chain(
                        s.orbIds["type"]["hp"],
                        s.orbIds["type"]["def"],
                        s.orbIds["type"]["atk"],
                        s.orbIds["type"]["hunger"],
                        s.orbIds["type"]["exp"]
                        )
                    ).index(orbId)/2
                )
            )

    elif roomGrid[ty][tx]["id"] == 2:
        s.Dungeon[s.Dy][s.Dx]['room'][ty][tx]["id"] = 2
        pos = [bfy-ty, bfx-tx]
        # ┏>|y, x| : U to D   D to U  L to R   R to L
        resetYX:list[list[int]] = [[11, 6], [1, 6], [6, 11], [6, 1]]
        resetType:int = 0

        if pos[0] == 1   : s.Dy -= 1; resetType = 0
        elif pos[0] == -1: s.Dy += 1; resetType = 1
        elif pos[1] == 1 : s.Dx -= 1; resetType = 2
        elif pos[1] == -1: s.Dx += 1; resetType = 3
        ty, tx = resetYX[resetType][0], resetYX[resetType][1]

        s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2
        roomPos = [
            [s.Dy-1 if s.Dy>0 else s.Dy, s.Dx],
            [s.Dy, s.Dx+1 if s.Dx<len(s.Dungeon[0])-1 else s.Dx],
            [s.Dy+1 if s.Dy<len(s.Dungeon)-1 else s.Dy, s.Dx],
            [s.Dy, s.Dx-1 if s.Dx>0 else s.Dx]
            ]
            
        for i in range(len(roomPos)):
            if len(s.Dungeon[roomPos[i][0]][roomPos[i][1]]) > 0 and s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] == 0 and list(s.Dungeon[s.Dy][s.Dx]['doorPos'].values())[i] == 1:
                s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] = 1
        s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

    elif roomGrid[ty][tx]["id"] == 6:
        cx, cy = 0, 0
        Type   = 1 if Dir in [curses.KEY_LEFT, curses.KEY_RIGHT] else 0
        match Dir:
            case curses.KEY_UP:    cy = ty - Int
            case curses.KEY_DOWN:  cy = ty + Int
            case curses.KEY_LEFT:  cx = tx - Int
            case curses.KEY_RIGHT: cx = tx + Int

        positions = [[cy, tx], [ty, cx]]
        if roomGrid[positions[Type][0]][positions[Type][1]]["id"] in s.interactableBlocks["cannotStepOn"]:
            ty, tx     = bfy, bfx
            s.Dy, s.Dx = bfDy, bfDx
        else: s.Dungeon[s.Dy][s.Dx]['room'][positions[Type][0]][positions[Type][1]] = {"block" : s.ids[6], "id" : 6}

    s.y, s.x                                = ty, tx
    s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = {"block" : s.ids[0], "id" : 0}
    s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = {"block":s.ids[300], "id":300}