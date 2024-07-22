import random, time
import curses
import threading
from   itertools   import chain

from Assets.data             import rooms, status
from Assets.data.color       import cColors                 as cc
from Game.core.system        import logger, blockDescription
from Game.entities.player    import event, checkStatus
from Game.utils.system       import xpSystem, tts
from Game.utils.system.sound import play


s, r = status, rooms
cs   = checkStatus
bd   = blockDescription

def set() -> None:
    s.hp       = 10
    s.df       = 5
    s.atk      = 1
    s.hunger   = 2000

    s.critRate = 10
    s.critDMG  = 10
    
    s.Mhp       = s.hp
    s.Mdf       = s.df
    s.Mxp       = 10
    s.Mlvl      = 25
    s.MFairWind = 90

def start(Dy:int, Dx:int, y:int, x:int) -> None:
    s.Dungeon[Dy][Dx]['room'][y][x] = {"block":s.ids[300], "id":300, "type" : 1}
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

    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = {"block" : s.ids[orbId], "id" : orbId, "type" : 0}
        
def orbEvent(Size:int, Type:int) -> None:
    orbData   = [
        [3,    1],
        [3,    1],
        [2,    1],
        [100, 50],
        [5,    1]
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
    sound     = ("player", "move")
    blockID   = roomGrid[ty][tx]["id"]

    if blockID == -1: ty, tx = bfy, bfx

    if blockID in [1, 3]:
        damage(roomGrid[ty][tx]["block"])

        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

        if s.df <= 0 and s.dfCrack <= 0:
            sound     = ("player", "armor", "crack")
            s.dfCrack = 1
            logger.addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")
        else: sound = ("player", "hit")

    elif blockID in s.enemyIds:
        sound = None
        s.hitPos.append([ty, tx])
        time.sleep(0.001)
        s.hitPos.remove([ty, tx])

        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    elif blockID == 4:
        sound = ("object", "itemBox", "open")
        itemEvent(ty, tx)
        ty, tx = bfy, bfx

    elif blockID in chain(s.orbIds["size"]["smallOne"], s.orbIds["size"]["bigOne"]):
        sound = ("player", "getItem")
        orbId = blockID
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

    elif blockID == 2:
        sound = ("object", "door", "open")
        s.Dungeon[s.Dy][s.Dx]['room'][ty][tx]["id"] = 2
        pos = [bfy-ty, bfx-tx]
        # ┏>|y, x| : U to D   D to U  L to R   R to L
        wayType:int = 0
        if pos[0] == 1   : s.Dy -= 1; wayType = 0
        elif pos[0] == -1: s.Dy += 1; wayType = 1
        elif pos[1] == 1 : s.Dx -= 1; wayType = 2
        elif pos[1] == -1: s.Dx += 1; wayType = 3

        DWPD = {
            'y'  : int(len(s.Dungeon[s.Dy][s.Dx]['room'])/2),
            'my' : len(s.Dungeon[s.Dy][s.Dx]['room'])-2,
            'x'  : int(len(s.Dungeon[s.Dy][s.Dx]['room'][0])/2),
            'mx' : len(s.Dungeon[s.Dy][s.Dx]['room'][0])-2
        }
        wayPoint:list[list[int]] = [
            [DWPD['my'], DWPD['x']],
            [1,          DWPD['x']],
            [DWPD['y'], DWPD['mx']],
            [DWPD['y'],          1]
            ]
        ty, tx = wayPoint[wayType][0], wayPoint[wayType][1]

        s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2
        roomPos = [
            [s.Dy-1 if s.Dy>0 else s.Dy, s.Dx],
            [s.Dy, s.Dx+1 if s.Dx<len(s.Dungeon[0])-1 else s.Dx],
            [s.Dy+1 if s.Dy<len(s.Dungeon)-1 else s.Dy, s.Dx],
            [s.Dy, s.Dx-1 if s.Dx>0 else s.Dx]
            ]
            
        for i in range(len(roomPos)):
            if len(s.Dungeon[roomPos[i][0]][roomPos[i][1]])                > 0 and\
               s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] == 0 and\
               list(s.Dungeon[s.Dy][s.Dx]['doorPos'].values())[i]         == 1:
                s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] = 1
        s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

    elif blockID == 6:
        sound = ("object", "box", "move")
        cx, cy = 0, 0
        Type   = 1 if Dir in [curses.KEY_LEFT, curses.KEY_RIGHT] else 0
        match Dir:
            case curses.KEY_UP:    cy = ty - Int
            case curses.KEY_DOWN:  cy = ty + Int
            case curses.KEY_LEFT:  cx = tx - Int
            case curses.KEY_RIGHT: cx = tx + Int

        positions = [[cy, tx], [ty, cx]]
        if roomGrid[positions[Type][0]][positions[Type][1]]["id"] in s.interactableBlocks["cannotStepOn"]:
            s.Dy, s.Dx = bfDy, bfDx
            ty, tx     = bfy, bfx
        else: s.Dungeon[s.Dy][s.Dx]['room'][positions[Type][0]][positions[Type][1]] = {"block" : s.ids[6], "id" : 6}

    elif blockID == 20:
        data = roomGrid[ty][tx]["nbt"]
        event.readSign(data["texts"], data["delay"], data["voice"])
        roomGrid[ty][tx] = {
            "block" : s.ids[21],
            "id"    : 21,
            "type"  : 0,
            "nbt"   : {
                "link" : True
            }
            }

        s.Dy, s.Dx = bfDy, bfDx
        ty, tx     = bfy, bfx

    elif blockID == 21:
        sound      = ("player", "interaction", "open")
        s.Dy, s.Dx = bfDy, bfDx
        ty, tx     = bfy, bfx

        logger.addLog(f"당신 앞에는 그저 {cc['fg']['O']}흙더미{cc['end']}가 자리를 지키고 있을 뿐입니다...")

    elif blockID == 22:
        if roomGrid[ty][tx]["nbt"]["step"]:
            for pos in [[ty-1, tx], [ty, tx+1], [ty+1, tx], [ty, tx-1]]:
                if not roomGrid[pos[0]][pos[1]]["id"] and not random.randrange(0,3):
                    roomGrid[pos[0]][pos[1]] = {
                        "block" : f"{cc['fg'][roomGrid[ty][tx]['nbt']['color']]}.{cc['end']}",
                        "id"    : 23,
                        "type"  : 0,
                        "nbt"   : {
                            "step" : 0,
                            "link" : True
                        }
                    }
            sound = ("player", "interaction", "stepFlower")

    elif blockID == 400:
        s.Dy, s.Dx = bfDy, bfDx

        if s.lvl<5:
            sound  = ("player", "hit")
            ty, tx = bfy, bfx
            logger.addLog(f"{cc['fg']['L']}당신{cc['end']}은 아직 {cc['fg']['F']}자격{cc['end']}이 주어지지 않았습니다.")
        else:
            sound            = ("player", "interaction", "activate")
            s.lvl           -= 5
            s.Mxp           -= 15
            s.xp             = 0
            if roomGrid[ty][tx]['nbt']['linkedInteraction']:
                event.linkedInteraction(ty, tx, 400, {"block" : "same_", "id" : 401, "type" : 0, "nbt":{"link" : True}}, cc['fg']['F'])
            else:
                roomGrid[ty][tx] = {
                    "block" : s.ids[401],
                    "id"    : 401,
                    "type"  : 0,
                    "nbt"   : {
                        "link" : True
                    }
                    }
            ty, tx = bfy, bfx

            logger.addLog(f"{cc['fg']['L']}당신{cc['end']}의 몸에서 {cc['fg']['F']}저주{cc['end']}가 빠져나가는 것이 느껴집니다...")

    elif blockID == 401:
        sound      = ("player", "hit")
        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx
        logger.addLog(f"이 {cc['fg']['A']}신상{cc['end']}은 이미 {cc['fg']['F']}저주{cc['end']}에 물들었습니다...")

    elif blockID == 900:
        sound = ("object", "ashChip", "get")
        s.ashChip += roomGrid[ty][tx]["nbt"]["count"]
        logger.addLog(f"{cc['fg']['G1']}잿조각{cc['end']}을 {cc['fg']['G1']}{roomGrid[ty][tx]['nbt']['count']}{cc['end']}개 얻었습니다.")
        cs.ashChipCheck()

    s.y, s.x                                = ty, tx
    s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = {"block" : s.ids[0],   "id" : 0,   "type" : 0}
    s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = {"block" : s.ids[300], "id" : 300, "type" : 1}
    if sound: play(*sound)

def observe(Dir) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    ty, tx = s.y, s.x
    match Dir:
        case curses.KEY_UP   : ty -= 1
        case curses.KEY_DOWN : ty += 1
        case curses.KEY_LEFT : tx -= 1
        case curses.KEY_RIGHT: tx += 1

    titleOnly = False
    data = bd.dataLoader(roomGrid[ty][tx]['id'], s.types[roomGrid[ty][tx]['type']], roomGrid[ty][tx])
    if not data:
        titleOnly = True
        targetType = {
            0 : "블록",
            1 : "엔티티",
            2 : "아이템"
        }[roomGrid[ty][tx]['type']]
        data = {
        "icon"        : f"{cc['fg']['R']}X{cc['end']}",
        "blockName"   : f"{cc['fg']['R']}해당 {targetType}의 정보가{cc['end']}\n      {cc['fg']['R']}존재하지 않습니다!{cc['end']}",
        "status"      : "",
        "explanation" : ""
        ""
        }
    bd.add(
        data['icon'],
        data['blockName'],
        data['status'],
        data['explanation'],
        titleOnly=titleOnly
    )

    s.playerMode = "normal"

def say(text, TextColor:str='L') -> None:
    logger.addLog(f"{cc['fg'][TextColor]}\"{text}\"{cc['end']}")
    threading.Thread(
        target=lambda: tts.TTS(text),
        daemon=True
    ).start()