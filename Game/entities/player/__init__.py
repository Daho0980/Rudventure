import curses
from   random    import randrange, choice
from   threading import Thread

from .                        import statusEffect
from Assets.data              import totalGameStatus as s
from Assets.data.permissions  import Player          as perm
from Assets.data.color        import cColors         as cc
from functions.grammar        import pstpos          as pp
from Game.behavior.items.all  import behaviorMap     as itemBMap
from Game.behavior.blocks.all import behaviorMap     as blockBMap
from Game.core.system.io      import infoWindow      as iWin
from Game.entities.player     import event
from Game.tools               import inventory, block
from Game.utils.system.block  import iset
from Game.utils.system.sound  import play

from Game.core.system.io.logger import (
    addLog
)
from Game.core.system.data.dataLoader import (
    obj
)


def _setPlayerStatus(hp, df, atk, hgr, critRate, critDMG, missRate, Mxp, Mlvl, evasionRate=0) -> None:
    s.hp  = hp
    s.df  = df
    s.atk = atk
    s.hgr = hgr

    s.critRate = critRate
    s.critDMG  = critDMG
    s.missRate = missRate

    s.Mhp  = hp
    s.Mdf  = df
    s.Mhgr = hgr
    s.Mxp  = Mxp
    s.Mlvl = Mlvl

    s.evasionRate = evasionRate

def set() -> None:
    if s.name.lower() in ("레포", "repo"):
        _setPlayerStatus(8, 1, 1, 2500, 4, 32, 32, 4, 32)

    elif s.name.lower() in ("업로드", "upload"):
        _setPlayerStatus(5, 2, 3, 1000, 75, 0, 5, 6, 12, 25)
        
    else: _setPlayerStatus(10, 5, 1, 2000, 10, 10, 10, 10, 20)

def _changePosWithFace(direction, ty, tx) -> tuple[int, int]:
    match direction:
        case curses.KEY_UP:
            ty    -= 1
            s.face = 'u'
        case curses.KEY_DOWN:
            ty    += 1
            s.face = 'd'
        case curses.KEY_LEFT:
            tx    -= 1
            s.face = 'r'
        case curses.KEY_RIGHT:
            tx    += 1
            s.face = 'l'

    return ty, tx

def start() -> None:
    event.getRoomData()
    s.y, s.x = map(
        lambda n: int(n/2),
        [
            len(s.Dungeon[s.Dy][s.Dx]['room']   ),
            len(s.Dungeon[s.Dy][s.Dx]['room'][0])
        ]
    )
    s.face         = 'u'
    s.steppedBlock = s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]
    block.place(obj('-be', 'player1', block=iset(s.eids['player1'])), s.y, s.x)

def attack(entityData:dict, sound:tuple=("player", "slash")) -> None:
    def target():
        nonlocal entityData, sound

        if not entityData.get('tag'):
            return

        if not (target:=s.entityMap.get(entityData['tag'])):
            return
        
        atk = s.atk
        if (data:=inventory.get()): atk += data['status']['atk']

        isHit    = True
        crit     = None
        dmgSound = None

        rate = randrange(1,101)
        if rate <= s.missRate:
            dmgSound = "miss"
            atk      = 0
            isHit    = False

        elif rate <= s.critRate:
            dmgSound = "critical"
            crit     = True
            atk      = int((atk+(s.critDMG*0.1))+(atk*(s.critDMG*0.01)))

        if target.hp-atk > 0:
            msg = f"{cc['fg']['R']}{target.name}{cc['end']}{pp(target.name,'sub',True)} {cc['fg']['L']}{atk}{cc['end']}만큼의 피해를 입었습니다!"
            if crit: msg += f" {cc['fg']['L']}치명타!{cc['end']}"

            if isHit:
                target.hitted()
                addLog(msg)

            else:
                addLog(f"{cc['fg']['L']}공격{cc['end']}이 빗나갔습니다!")

            if isHit   : play(*sound)
            if dmgSound: play("entity", "enemy", "damage", dmgSound)

        target.hp -= atk

        inventory.durabilityDecrease()
        if data: itemBMap[data['type']][data['id']].attack()

    Thread(
        target=target,
        name  ="playerAttack",
        daemon=True
    ).start()

# region main
def move(direction) -> None:
    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']

    ty, tx     = _changePosWithFace(direction, s.y, s.x)
    bfy, bfx   = s.y, s.x
    bfDy, bfDx = s.Dy, s.Dx

    s.hgr -= 1

    sound = ("player", "move")
    
    # accessibility
    if not perm.data[roomGrid[ty][tx]['id']]\
           & (perm.STEP|perm.INTERACTION|perm.ENTITY):
        ty  , tx   = bfy , bfx
        s.Dy, s.Dx = bfDy, bfDx

    roomGrid  = s.Dungeon[s.Dy][s.Dx]['room']
    blockData = block.take(ty, tx)
    blockID   = blockData['id']

    # entity action
    if perm.data[blockID] & perm.ENTITY:

        if  blockData.get('tag', False)\
        and blockData['tag'] in s.friendlyEntity:
            sound = ("player", "hit")

            addLog(
                f"{cc['fg']['L']}우호적인 엔티티{cc['end']}는 {cc['fg']['R']}공격{cc['end']}할 수 없습니다!",
                colorKey='L'
            )

        else:
            sound = None

            if blockData.get('tag', False):
                s.target['tag'] = blockData['tag']

            if perm.data[blockData['id']]&perm.ATTACK: attack(blockData)

    # block interaction
    else:
        if blockID in blockBMap:
            ty, tx, sound = blockBMap[blockID].interact(
                block=blockData,
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

    blockData = block.take(s.y, s.x)
    if perm.data[blockData['id']] & perm.STEP:
        s.steppedBlock = blockData\
                if perm.data[blockID]&perm.MAINTAIN\
            else blockData['blockData']\
                if blockData.get('blockData', False)\
            else block.get('floor')
    
    block.place(obj('-be', 'player1', block=iset(s.eids['player1'])), s.y, s.x)

    if sound: play(*sound)

    statusEffect.tickProgress("back")


# region extended
def observe(direction) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    ty, tx = _changePosWithFace(direction, s.y, s.x)

    titleOnly = False
    blockData = roomGrid[ty][tx]
    
    match blockData['id']:
        case 'cat':
            if blockData['tag'] in s.friendlyEntity:
                blockData['nbt'] = { "link" : True }

    data = iWin.itemDataExtraction(
        blockData['nbt']['itemData']['id'],
        blockData['nbt']['itemData']['type'],
        **blockData['nbt']['itemData']
    )\
        if blockData['id'] == 'item'\
    else iWin.blockDataExtraction(
        blockData['id'],
        blockData['type'],
        **blockData
    )

    if not data:
        titleOnly  = True
        targetType = {
            "block"  : "블록",
            "entity" : "엔티티",
            "item"   : "아이템"
        }[blockData['type']]

        data = {
            "icon"        : f"{cc['fg']['R']}X{cc['end']}",
            "name"        : f"{cc['fg']['R']}해당 {targetType}의 정보가{cc['end']}\n      {cc['fg']['R']}존재하지 않습니다!{cc['end']}",
            "status"      : "",
            "explanation" : "",
            "subStatus"   : ""
        }

    iWin.add(*data.values(), titleOnly=titleOnly)

    s.playerMode = "normal"

def whistle() -> None:
    play("player", "whistle", "wa"if not randrange(0,915) else str(choice((1,2,3,4))))
    if s.target['tag'] and s.enemyCount:
        s.target['attackable'] = True
        s.target['command']    = True
        addLog(
            f"{cc['fg']['L']}집중 공격 대상{cc['end']}이 설정되었습니다!",
            colorKey='L'
        )
        
    else: addLog("아무런 일도 일어나지 않았습니다...", colorKey='L')