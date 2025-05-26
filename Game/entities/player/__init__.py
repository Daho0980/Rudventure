import time    ; import curses; import threading
from   random                   import randrange, choices, choice

from .                           import statusEffect
from Assets.data.permissions     import Player      as perm
from Assets.data.color           import cColors     as cc
from functions.grammar           import pstpos      as pp
from Game.core.system            import infoWindow  as iWin
from Game.core.system.logger     import addLog
from Game.core.system.dataLoader import obj
from Game.utils.system           import xpSystem, tts
from Game.utils.system.block     import iset
from Game.utils.system.sound     import play

from Assets.data import (
    totalGameStatus as s  ,
    percentage      as per,
    comments        as c
)
from Game.entities.player import (
    checkStatus as cs,

    event,
)


def _setPlayerStatus(hp, df, atk, hgr, critRate, critDMG, Mxp, Mlvl, MFW, evasionRate=0) -> None:
    s.hp     = hp
    s.df     = df
    s.atk    = atk
    s.hunger = hgr

    s.critRate = critRate
    s.critDMG  = critDMG

    s.Mhp  = hp
    s.Mdf  = df
    s.Mxp  = Mxp
    s.Mlvl = Mlvl

    s.MFairWind = MFW

    s.evasionRate = evasionRate

def set() -> None:
    if s.name.lower() in ["레포", "repo"]:
        _setPlayerStatus(8, 1, 1, 2500, 4, 32, 4, 32, 90)

    elif s.name.lower() in ["업로드", "upload"]:
        _setPlayerStatus(5, 2, 3, 1000, 75, 0, 6, 12, 90, 45)
        
    else: _setPlayerStatus(10, 5, 1, 2000, 10, 10, 10, 20, 90)

def start() -> None:
    getRoomData()
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

def damage(block:str="?", atk:int=1) -> tuple:
    sound = ("player", "hit")
    event.hitted()
    addLog(
        f"{s.lightName}{pp(s.name,'sub',True)} [ {block} ] 에 의해 상처입었습니다",
        colorKey='R'
    )

    if s.df > 0:
        sound = ("player", "armor", "defended")
        s.df -= 1
        if s.df < 0: dmg = int(atk/2)
        else:        dmg = int(atk/3)
                
        if s.df <= 0 and s.dfCrack <= 0:
            sound     = ("player", "armor", "armorCrack")
            s.dfCrack = 1
            addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!", colorKey='B1')

    else: dmg = atk

    s.hp -= dmg
    event.bleeding(dmg)

    if s.hp <= 0: s.DROD = [
        f"{cc['fg']['R']}{choice(["과다출혈","피로 과다","졸도","자살","우울증","과로"])}{cc['end']}",
        'R'
    ]

    return sound

def attack(ty, tx, attackSound:tuple=("player", "slash")) -> None:
    s.hitPos['pos'] .append([ty, tx])
    s.hitPos['data'].append(["player", s.atk, attackSound])
    time.sleep(0.001)
    s.hitPos['pos'] .remove([ty, tx])
    s.hitPos['data'].remove(["player", s.atk, attackSound])

def orbBoxEvent(y:int, x:int, face:str) -> None:
    orbId = f"{choices(
        ('hg', 'hp', 'df', 'atk', 'cs'),
        weights=(45, 15, 10, 5, 15),
        k      =1
    )[0]}Orb{choices(
        ('S', 'B'),
        weights=(60, 40),
        k      =1
    )[0]}"

    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = obj(
        '-bb', orbId,
        block=iset(s.bids[orbId], Type=face)
    )
        
orbData = {
    "S" : {
        "hp"  : 1,
        "df"  : 1,
        "atk" : 1,
        "hg"  : 50,
        "cs"  : 1
    },
    "B" : {
        "hp"  : 3,
        "df"  : 2,
        "atk" : 2,
        "hg"  : 75,
        "cs"  : 5
    }
}
def orbEvent(ID:str) -> None:
    S, T    = ID[-1], ID[:-4]
    point   = orbData[S][T]
    comment = randrange(1,101) <= per.getOrb
    match T:
        case 'hp':
            if s.hp == s.Mhp:
                say(choice(c.getOrb['hp']['hpTooOver'][S]))

                return
                
            elif s.hp+point > s.Mhp:
                s.hp = s.Mhp
                say(choice(c.getOrb['hp']['hpOver'][S]))

                return
            
            s.hp += point
            if s.hp == s.Mhp: play("system", "perfectLvlUp")
            
            if comment:
                say(choice(
                    c.getOrb['hp']['hpFull'
                            if s.hp == s.Mhp
                        else ['notHpLow','hpLow'][s.hpLow]
                    ][S]
                ))
                
        case 'df':
            if s.df == s.Mdf:
                say(choice(c.getOrb['df']['dfTooOver'][S]))

                return

            if s.df+point > s.Mdf:
                s.df = s.Mdf
                say(choice(c.getOrb['df']['dfOver'][S]))

                return

            s.df += point
            if s.df == s.Mdf: play("system", "perfectLvlUp")

            if comment:
                if s.df == s.Mdf:
                    say(choice(c.getOrb['df']['dfFull'][S]))

                elif s.df == point:
                    say(choice(c.getOrb['df']['restorationed'][S]))

        case 'atk':
            s.atk += point
            if comment:
                say(choice(
                    c.getOrb['atk']['lowAtk'
                            if s.atk < s.stage
                        else 'hiAtk'
                    ][S]
                ))
        case 'hg': s.hunger += point

        case 'cs': xpSystem.getXP(point)


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

    s.hunger -= 1

    sound   = ("player", "move")
    
    # accessibility
    if not perm.data[roomGrid[ty][tx]['id']] & (perm.STEP|perm.INTERACTION|perm.ENTITY):
        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
    block    = roomGrid[ty][tx]
    blockID  = block['id']

    # entity action
    if perm.data[blockID]&perm.ENTITY:

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
    if blockID == 'wall':
        sound = damage(block['block'])

        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    elif blockID == 'orbBox':
        sound = ("object", "itemBox", "open")
        orbBoxEvent(ty, tx, block['nbt']['face'])

    elif "Orb" in blockID:
        sound = ("player", "interaction", "repo", "nom")if s.playerIdentity=='repo'else("player", "getItem")
        orbEvent(blockID)

    elif blockID == 'door':
        sound = ("object", "door", "open")

        s.Dungeon[s.Dy][s.Dx]['room'][ty][tx] = obj('-bb', 'door')

        # ┏>|y, x| : U->D D->U L->R R->L
        pos     = [bfy-ty, bfx-tx]
        wayType = 0

        if   pos[0] ==  1: s.Dy -= 1; wayType = 0
        elif pos[0] == -1: s.Dy += 1; wayType = 1
        elif pos[1] ==  1: s.Dx -= 1; wayType = 2
        elif pos[1] == -1: s.Dx += 1; wayType = 3

        DWPD = {
            'y'  : len(s.Dungeon[s.Dy][s.Dx]['room']   )//2,
            'my' : len(s.Dungeon[s.Dy][s.Dx]['room']   ) -2,
            'x'  : len(s.Dungeon[s.Dy][s.Dx]['room'][0])//2,
            'mx' : len(s.Dungeon[s.Dy][s.Dx]['room'][0]) -2
        }
        wayPoint:list[list[int]] = [
            [DWPD['my'], DWPD['x']],
            [1,          DWPD['x']],
            [DWPD['y'], DWPD['mx']],
            [DWPD['y'],          1]
        ]
        ty, tx = wayPoint[wayType]

        s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2
        roomPos = [
            [s.Dy-1 if s.Dy>0 else s.Dy,                   s.Dx],
            [s.Dy, s.Dx+1 if s.Dx<len(s.Dungeon[0])-1 else s.Dx],
            [s.Dy+1 if s.Dy<len(s.Dungeon)-1 else s.Dy,    s.Dx],
            [s.Dy,                   s.Dx-1 if s.Dx>0 else s.Dx]
        ]
            
        for i in range(len(roomPos)):
            if  len(s.Dungeon[roomPos[i][0]][roomPos[i][1]])               >0\
            and s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited']==0\
            and list(s.Dungeon[s.Dy][s.Dx]['doors'].values())[i]          ==1:
                s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] = 1
        s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

        getRoomData()

    elif blockID in ('squishy0', 'squishy1'):
        sound = ("object", "squishy", "squish")

        face, count, command = list(s.Dungeon[s.Dy][s.Dx]['room'][ty][tx]['nbt'].values())

        if count:
            addLog(
                f"{cc['fg']['B1']}하하, 또 속으셨네요.{cc['end']}"\
                    if count<0\
                else f"{cc['fg']['B1']}{count}{cc['end']}번 남았습니다...",
                colorKey='B1'
            )

            BID = 'squishy0' if blockID=='squishy1' else 'squishy1'
            s.Dungeon[s.Dy][s.Dx]['room'][ty][tx] = obj(
                '-bb', BID,
                block=iset(s.bids[BID], Type=face),
                nbt={
                    "face"    : face,
                    "count"   : count-1,
                    "command" : command
                }
            )
            
        else: exec(command)

        ty, tx = bfy, bfx

    elif blockID == 'clayModel':
        data = block["nbt"]

        s.Dungeon[s.Dy][s.Dx]['roomIcon'] = ['☷', 'O']
        event.readSign(data["texts"], data["delay"], data["voice"], data["command"])
        roomGrid[ty][tx] = obj('-bb', 'deadClayModel', nbt={ 'link' : True })

    elif blockID == 'deadClayModel':
        sound = ("player", "interaction", "open")

        addLog(
            f"당신 앞에는 그저 {cc['fg']['O']}흙더미{cc['end']}가 자리를 지키고 있을 뿐입니다...",
            colorKey='O'
        )

    elif blockID == 'flower':
        if block['nbt']['step']:
            sound       = ("player", "interaction", "step", "flower")
            flowerColor = block['nbt']['color']

            for pos in [[ty-1, tx], [ty, tx+1], [ty+1, tx], [ty, tx-1]]:
                if  roomGrid[pos[0]][pos[1]]["id"]=='floor' and\
                not randrange(0,3):
                    roomGrid[pos[0]][pos[1]] = obj(
                        '-bb', 'petal',
                        block=f"{cc['fg'][flowerColor]}. {cc['end']}",
                        nbt  ={'link' : True}
                    ) if block['nbt']['step'] == 1 else obj(
                        '-bb', 'flower',
                        block=f"{cc['fg'][flowerColor]}{iset(choice(['*',',','.','_']), Type='s')}{cc['end']}",
                        nbt  ={
                            "color" : flowerColor,
                            "step"  : block['nbt']['step']-1
                        }
                    )

    elif blockID == 'blood':
        sound = ("player", "interaction", "step", "blood")

        if block['nbt']['stack'] > 2:
            split = randrange(1, 4)
            event.bleeding(split, False)
            statusEffect.addEffect('bloodStomping', block['nbt']['stack']-split)

        else: statusEffect.addEffect('bloodStomping', block['nbt']['stack'])

    elif blockID == 'normalStatue':
        s.Dy, s.Dx = bfDy, bfDx

        if s.lvl<5:
            sound = ("player", "hit")

            addLog(
                f"{s.playerColor[0]}당신{cc['end']}은 아직 {cc['fg']['F']}자격{cc['end']}이 주어지지 않았습니다.",
                colorKey='A'
            )

        else:
            sound  = ("player", "interaction", "activate")

            s.Dungeon[s.Dy][s.Dx]['roomIcon'] = ['Y', 'F']

            if s.lvl > (s.Mlvl/2): commentType = "middle"

            s.lvl -= 5
            s.Mxp -= 15
            s.xp   = 0
            commentType = "Over" if s.lvl>(s.Mlvl/2) else "Under"

            if block['nbt']['linkedInteraction']:
                event.linkedInteraction(
                    ty, tx, 'normalStatue',
                    {
                        "block" : "_same",
                        "id"    : 'cursedStatue',
                        "type"  : 'block',
                        "nbt"   : { "link" : True }
                    },
                    cc['fg']['F']
                )

            else: roomGrid[ty][tx] = obj('-bb', 'cursedStatue', nbt={ "link" : True })

            addLog(
                f"{s.playerColor[0]}당신{cc['end']}의 몸에서 {cc['fg']['F']}저주{cc['end']}가 빠져나가는 것이 느껴집니다...",
                colorKey='A'
            )
            say(choice(c.curseDecrease[commentType]))

    elif blockID == 'cursedStatue':
        sound = ("player", "hit")

        addLog(
            f"이 {cc['fg']['A']}신상{cc['end']}은 이미 {cc['fg']['F']}저주{cc['end']}에 물들었습니다...",
            colorKey='F'
        )

    elif blockID in ('aorta', 'venaCava'):
        sound = ("player", "getItem")

        # exec(f"{['s.Mhp', 's.Mdf'][blockID-501]}+=3")
        exec(f"{'s.Mhp'\
                if blockID=='aorta'\
            else 's.Mdf'\
                if blockID=='venaCava'\
            else '_'\
        }+=3")

    elif blockID == 'ashChip':
        sound = ("object", "ashChip", "get")

        count = block["nbt"]["count"]
        if count:
            s.ashChip += count
            addLog(f"{cc['fg']['G1']}잿조각{cc['end']}을 {cc['fg']['G1']}{count}{cc['end']}개 얻었습니다.", colorKey='G1')
            cs.ashChipCheck()

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

def _linkedSay(lines:list[str]) -> None:
    def target():
        nonlocal lines
        for line in lines:
            say(line); time.sleep(tts.TTC(line, logTick=False)+1)

    threading.Thread(target=target, daemon=True).start()

def say(text:str, TextColor:str="pc") -> None:
    if isinstance(text, list): _linkedSay(text); return

    addLog(
        f"{s.playerColor[0] if TextColor=='pc'else TextColor}\"{text}\"{cc['end']}",
        duration=max(50, tts.TTC(text)),
        colorKey=s.playerColor[1]
    )
    threading.Thread(
        target=lambda: tts.TTS(text, voicePath=("player", "voice", s.playerVoice)),
        daemon=True
    ).start()

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

def getRoomData() -> None:
    room = s.Dungeon[s.Dy][s.Dx]

    s.roomData['type'] = room['name']
    s.roomData['cell'] = sum(map(lambda l:len(l),room['room']))

    s.roomData['maxHeight'] = len(room['room'])
    s.roomData['maxWidth']  = len(max(room['room'], key=len))

    s.roomData['maxCharWidth'] = s.roomData['maxWidth']*2