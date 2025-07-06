import time
import curses
from   random import randrange, choice

from .                        import statusEffect
from Assets.data              import totalGameStatus as s
from Assets.data.permissions  import Player          as perm
from Assets.data.color        import cColors         as cc
from Game.behavior.blocks.all import behaviorMap
from Game.core.system.io      import infoWindow as iWin
from Game.entities.player     import event
from Game.utils.system.block  import iset
from Game.utils.system.sound  import play

from Game.core.system.io.logger import (
    addLog
)
from Game.core.system.data.dataLoader import (
    obj
)


def _setPlayerStatus(hp, df, atk, hgr, critRate, critDMG, Mxp, Mlvl, evasionRate=0) -> None:
    s.hp  = hp
    s.df  = df
    s.atk = atk
    s.hgr = hgr

    s.critRate = critRate
    s.critDMG  = critDMG

    s.Mhp  = hp
    s.Mdf  = df
    s.Mhgr = hgr
    s.Mxp  = Mxp
    s.Mlvl = Mlvl

    s.evasionRate = evasionRate

def set() -> None:
    if s.name.lower() in ("레포", "repo"):
        _setPlayerStatus(8, 1, 1, 2500, 4, 32, 4, 32)

    elif s.name.lower() in ("업로드", "upload"):
        _setPlayerStatus(5, 2, 3, 1000, 75, 0, 6, 12, 90)
        
    else: _setPlayerStatus(10, 5, 1, 2000, 10, 10, 10, 20)

def start() -> None:
    event.getRoomData()
    s.y, s.x = map(
        lambda n: int(n/2),
        [
            len(s.Dungeon[s.Dy][s.Dx]['room']   ),
            len(s.Dungeon[s.Dy][s.Dx]['room'][0])
        ]
    )
    s.face         = 'n'
    s.steppedBlock = s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]
    s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = obj('-be', 'player1', block=iset(s.eids['player1']))

def attack(ty, tx, attackSound:tuple=("player", "slash")) -> None:
    s.hitPos['pos'] .append([ty, tx])
    s.hitPos['data'].append(["player", s.atk, attackSound])
    time.sleep(0.001)
    s.hitPos['pos'] .remove([ty, tx])
    s.hitPos['data'].remove(["player", s.atk, attackSound])

# region main
def move(direction) -> None:
    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']

    bfy, bfx   = s.y, s.x
    ty, tx     = s.y, s.x
    bfDy, bfDx = s.Dy, s.Dx

    match direction:
        case curses.KEY_UP   : ty -= 1
        case curses.KEY_DOWN : ty += 1
        case curses.KEY_LEFT :
            tx    -= 1
            s.face = 'r'

        case curses.KEY_RIGHT:
            tx    += 1
            s.face = 'l'

    s.hgr -= 1

    sound = ("player", "move")
    
    # accessibility
    if not perm.data[roomGrid[ty][tx]['id']] & (perm.STEP|perm.INTERACTION|perm.ENTITY):
        ty  , tx   = bfy , bfx
        s.Dy, s.Dx = bfDy, bfDx

    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
    block    = roomGrid[ty][tx]
    blockID  = block['id']

    # entity action
    if perm.data[blockID] & perm.ENTITY:

        if  block.get('tag', False)\
        and block['tag'] in s.friendlyEntity:
            sound = ("player", "hit")

            addLog(
                f"{cc['fg']['L']}우호적인 엔티티{cc['end']}는 {cc['fg']['R']}공격{cc['end']}할 수 없습니다!",
                colorKey='L'
            )

        else:
            sound = None

            if block.get('tag', False):
                s.target['tag'] = block['tag']

            attack(ty, tx)

    # block interaction
    else:
        if blockID in behaviorMap:
            ty, tx, sound = behaviorMap[blockID].interact(
                block=block,
                sound=sound,
                ty   =ty,
                tx   =tx,
                bfy  =bfy,
                bfx  =bfx
            )

        else:
            if s.debug:
                addLog(
                    f"{cc['fg']['R']}'{blockID}'에 대한 행동 클래스가 존재하지 않습니다!{cc['end']}",
                    colorKey='R'
                )

    if not perm.data[blockID] & perm.STEP:
        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    statusEffect.tickProgress("fore")

    s.y, s.x = ty, tx

    s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = s.steppedBlock

    block          = s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]
    if perm.data[block['id']] & perm.STEP:
        s.steppedBlock = block\
                if perm.data[blockID]&perm.MAINTAIN\
            else block['blockData']\
                if block.get('blockData', False)\
            else obj('-bb', 'floor')
    
    s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = obj('-be', 'player1', block=iset(s.eids['player1']))

    if sound: play(*sound)

    statusEffect.tickProgress("back")


# region extended
def observe(direction) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    ty, tx = s.y, s.x
    match direction:
        case curses.KEY_UP   : ty -= 1
        case curses.KEY_DOWN : ty += 1
        case curses.KEY_LEFT : tx -= 1
        case curses.KEY_RIGHT: tx += 1

    titleOnly    = False
    block = roomGrid[ty][tx]
    
    match block['id']:
        case 'cat':
            if block['tag'] in s.friendlyEntity:
                block['nbt'] = { "link" : True }

    data = iWin.dataExtraction(block['id'], block['type'], **block)

    if not data:
        titleOnly  = True
        targetType = {
            "block"  : "블록",
            "entity" : "엔티티",
            "item"   : "아이템"
        }[block['type']]

        data = {
            "icon"        : f"{cc['fg']['R']}X{cc['end']}",
            "blockName"   : f"{cc['fg']['R']}해당 {targetType}의 정보가{cc['end']}\n      {cc['fg']['R']}존재하지 않습니다!{cc['end']}",
            "status"      : "",
            "explanation" : ""
            ""
        }

    iWin.add(
        data['icon'],
        data['blockName'],
        data['status'],
        data['explanation'],

        titleOnly=titleOnly
    )

    s.playerMode = "normal"

def whistle() -> None:
    play("player", "whistle", "wa"if not randrange(0,915) else str(choice([1,2,3,4])))
    if s.target['tag'] and s.enemyCount:
        s.target['attackable'] = True
        s.target['command']    = True
        addLog(
            f"{cc['fg']['L']}집중 공격 대상{cc['end']}이 설정되었습니다!",
            colorKey='L'
        )
        
    else: addLog("아무런 일도 일어나지 않았습니다...", colorKey='L')