import time    ; import curses; import threading
from   itertools                import chain
from   random                   import randrange, choice

from .                           import statusEffect
from Assets.data.color           import cColors     as cc
from functions.grammar           import pstpos      as pp
from Game.core.system            import infoWindow  as iWin
from Game.core.system.logger     import addLog
from Game.core.system.dataLoader import obj
from Game.utils.system           import xpSystem, tts
from Game.utils.system.block     import iset
from Game.utils.system.sound     import play

from Assets.data import (
    totalGameStatus as s,
    percentage      as per,
    comments        as c
)
from Game.entities.player import (
    checkStatus as cs,

    event,
)


def set() -> None:
    if s.name.lower() in ["레포", "repo"]:
        s.hp     = 8
        s.df     = 1
        s.atk    = 1
        s.hunger = 2500

        s.critRate = 4
        s.critDMG  = 32
        
        s.Mhp  = s.hp
        s.Mdf  = s.df
        s.Mxp  = 4
        s.Mlvl = 32

        s.MFairWind = 90

    elif s.name.lower() in ["업로드", "upload"]:
        s.hp     = 5
        s.df     = 2
        s.atk    = 3
        s.hunger = 1000

        s.critRate    = 75
        s.critDMG     = 0
        s.evasionRate = 45
        
        s.Mhp  = s.hp
        s.Mdf  = s.df
        s.Mxp  = 6
        s.Mlvl = 12

        s.MFairWind = 90
        
    else:
        s.hp     = 3
        s.df     = 5
        s.atk    = 1
        s.hunger = 2000

        s.critRate = 10
        s.critDMG  = 10
        
        s.Mhp  = s.hp
        s.Mdf  = s.df
        s.Mxp  = 10
        s.Mlvl = 20

        s.MFairWind = 90

def start() -> None:
    getRoomData()
    s.y, s.x = map(
        lambda n: int(n/2),
        [
            len(s.Dungeon[s.Dy][s.Dx]['room']   ),
            len(s.Dungeon[s.Dy][s.Dx]['room'][0])
        ]
    )
    s.face   = 'n'
    s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = obj('-bb', '300', block=iset(s.ids[300]))

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
        f"{cc['fg']['R']}{choice(["과다출혈","피로 과다","졸도","자살","우울증"])}{cc['end']}",
        'R'
    ]

    return sound

def attack(ty, tx, attackSound:tuple=("player", "slash")) -> None:
    s.hitPos['pos'].append([ty, tx])
    s.hitPos['data'].append(["player", s.atk, attackSound])
    time.sleep(0.001)
    s.hitPos['pos'].remove([ty, tx])
    s.hitPos['data'].remove(["player", s.atk, attackSound])

def itemEvent(y:int, x:int, face:str) -> None:
    orbPer = randrange(1, 101)

    if   0  < orbPer <= 45: typeIndex = "hunger"
    elif 45 < orbPer <= 70: typeIndex = "hp"
    elif 70 < orbPer <= 80: typeIndex = "def"
    elif 80 < orbPer <= 85: typeIndex = "atk"
    else                  : typeIndex = "exp"

    orbId = s.orbIds["type"][typeIndex][randrange(0, 2)]

    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = obj(
        '-bb', str(orbId),
        block=iset(s.ids[orbId], Type=face)
    )
        
def orbEvent(Size:int, Type:int) -> None:
    orbData = [
    #    s   L
        [1 , 3  ],
        [1 , 2  ],
        [1 , 2  ],
        [50, 100],
        [1 , 5  ]
    ]

    point   = orbData[Type][Size]
    comment = randrange(1,101) <= per.getOrb
    match Type:
        case 0:
            if s.hp == s.Mhp:
                say(choice(c.getOrb['hp']['hpTooOver'][Size]))

                return
                
            elif s.hp+point > s.Mhp:
                s.hp = s.Mhp
                say(choice(c.getOrb['hp']['hpOver'][Size]))

                return
            
            s.hp += point
            if s.hp == s.Mhp: play("system", "perfectLvlUp")
            
            if comment:
                say(choice(
                    c.getOrb['hp']['hpFull'
                            if s.hp == s.Mhp
                        else ['notHpLow','hpLow'][s.hpLow]
                    ][Size]
                ))
                
        case 1:
            if s.df == s.Mdf:
                say(choice(c.getOrb['df']['dfTooOver'][Size]))

                return

            if s.df+point > s.Mdf:
                s.df = s.Mdf
                say(choice(c.getOrb['df']['dfOver'][Size]))

                return

            s.df += point
            if s.df == s.Mdf: play("system", "perfectLvlUp")

            if comment:
                if s.df == s.Mdf:
                    say(choice(c.getOrb['df']['dfFull'][Size]))

                elif s.df == point:
                    say(choice(c.getOrb['df']['restorationed'][Size]))

        case 2:
            s.atk += point
            if comment:
                say(choice(
                    c.getOrb['atk']['lowAtk'
                            if s.atk < s.stage
                        else 'hiAtk'
                    ][Size]
                ))
        case 3: s.hunger += point

        case 4: xpSystem.getXP(point)


def move(Dir, distance:int) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    bfy, bfx   = s.y, s.x
    ty, tx     = s.y, s.x
    bfDy, bfDx = s.Dy, s.Dx

    match Dir:
        case curses.KEY_UP   : ty -= distance
        case curses.KEY_DOWN : ty += distance
        case curses.KEY_LEFT :
            tx    -= distance
            s.face = 'r'

        case curses.KEY_RIGHT:
            tx    += distance
            s.face = 'l'

    s.hunger -= 1

    sound   = ("player", "move")
    block   = roomGrid[ty][tx]
    blockID = block['id']

    if blockID == -1: ty, tx = bfy, bfx

    if blockID in [1, 3]:
        sound = damage(block['block'])

        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    elif blockID in s.enemyIds+s.animalIds:

        if block['hashKey'] in s.friendlyEntity:
            sound = ("player", "hit")
            addLog(
                f"{cc['fg']['L']}우호적인 엔티티{cc['end']}는 {cc['fg']['R']}공격{cc['end']}할 수 없습니다!",
                colorKey='L'
            )

        else:
            sound = None

            s.target['hashKey'] = block['hashKey']
            attack(ty, tx)
        
        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx

    elif blockID == 4:
        sound = ("object", "itemBox", "open")
        itemEvent(ty, tx, block['nbt']['face'])
        ty, tx = bfy, bfx

    elif blockID in chain(s.orbIds["size"]["smallOne"], s.orbIds["size"]["bigOne"]):
        sound = ("player", "interaction", "repo", "nom")if s.name.lower()in("repo","레포")else("player", "getItem")
        orbId = blockID
        orbEvent(
            Size=1 if orbId in s.orbIds['size']['bigOne'] else 0,
            Type=int(list(chain(*s.orbIds['type'].values())).index(orbId)/2)
        )

    elif blockID == 2:
        sound = ("object", "door", "open")

        s.Dungeon[s.Dy][s.Dx]['room'][ty][tx]["id"] = 2

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

    elif blockID == 6:
        sound = ("object", "box", "move")
        cy, cx = 0, 0
        Type   = 1 if Dir in [curses.KEY_LEFT,curses.KEY_RIGHT] else 0

        match Dir:
            case curses.KEY_UP:    cy = ty-distance
            case curses.KEY_DOWN:  cy = ty+distance
            case curses.KEY_LEFT:  cx = tx-distance
            case curses.KEY_RIGHT: cx = tx+distance

        positions = [[cy, tx], [ty, cx]]
        if roomGrid[positions[Type][0]][positions[Type][1]]['id'] in s.interactableBlocks['unsteppable']:
            s.Dy, s.Dx = bfDy, bfDx
            ty, tx     = bfy, bfx

        else: s.Dungeon[s.Dy][s.Dx]['room'][positions[Type][0]][positions[Type][1]] = obj('-bb', '6')

    elif blockID in (8, 9):
        sound = ("object", "squishy", "squish")

        face, count, command = list(s.Dungeon[s.Dy][s.Dx]['room'][ty][tx]['nbt'].values())

        if count:
            addLog(
                f"{cc['fg']['B1']}하하, 또 속으셨네요.{cc['end']}"\
                    if count<0\
                else f"{cc['fg']['B1']}{count}{cc['end']}번 남았습니다...",
                colorKey='B1'
            )

            BID = 8 if blockID==9 else 9
            s.Dungeon[s.Dy][s.Dx]['room'][ty][tx] = obj(
                '-bb', str(BID),
                block=iset(s.ids[BID], Type=face),
                nbt={
                    "face"    : face,
                    "count"   : count-1,
                    "command" : command
                }
            )
            
        else: exec(command)

        ty, tx = bfy, bfx

    elif blockID == 20:
        data = block["nbt"]

        s.Dungeon[s.Dy][s.Dx]['roomIcon'] = ['☷', 'O']
        event.readSign(data["texts"], data["delay"], data["voice"], data["command"])
        roomGrid[ty][tx] = obj('-bb', '21', nbt={'link' : True})

        s.Dy, s.Dx = bfDy, bfDx
        ty, tx     = bfy, bfx

    elif blockID == 21:
        sound      = ("player", "interaction", "open")
        s.Dy, s.Dx = bfDy, bfDx
        ty, tx     = bfy, bfx

        addLog(
            f"당신 앞에는 그저 {cc['fg']['O']}흙더미{cc['end']}가 자리를 지키고 있을 뿐입니다...",
            colorKey='O'
        )

    elif blockID == 22:
        if block['nbt']['step']:
            sound       = ("player", "interaction", "step", "flower")
            flowerColor = block['nbt']['color']

            for pos in [[ty-1, tx], [ty, tx+1], [ty+1, tx], [ty, tx-1]]:
                if  not roomGrid[pos[0]][pos[1]]["id"] and\
                not randrange(0,3):
                    roomGrid[pos[0]][pos[1]] = obj(
                        '-bb', '23',
                        block=f"{cc['fg'][flowerColor]}. {cc['end']}",
                        nbt  ={'link' : True}
                    ) if block['nbt']['step'] == 1 else obj(
                        '-bb', '22',
                        block=f"{cc['fg'][flowerColor]}{iset(choice(['*',',','.','_']), Type='s')}{cc['end']}",
                        nbt  ={
                            "color" : flowerColor,
                            "step"  : block['nbt']['step']-1
                        }
                    )

    elif blockID == 27:
        sound = ("player", "interaction", "step", "blood")

        s.steppedBlock = block['nbt']['blockData']

        if block['nbt']['stack'] > 2:
            split = randrange(1, 4)
            event.bleeding(split, False)
            statusEffect.addEffect('1', block['nbt']['stack']-split)

        else: statusEffect.addEffect('1', block['nbt']['stack'])

    elif blockID == 400:
        s.Dy, s.Dx = bfDy, bfDx

        if s.lvl<5:
            sound  = ("player", "hit")
            ty, tx = bfy, bfx
            addLog(f"{s.playerColor[0]}당신{cc['end']}은 아직 {cc['fg']['F']}자격{cc['end']}이 주어지지 않았습니다.", colorKey='A')

        else:
            sound  = ("player", "interaction", "activate")

            s.Dungeon[s.Dy][s.Dx]['roomIcon'] = ['Y', 'F']

            if s.lvl>(s.Mlvl/2): commentType = "middle"

            s.lvl -= 5
            s.Mxp -= 15
            s.xp   = 0
            commentType = "Over" if s.lvl>(s.Mlvl/2) else "Under"

            if block['nbt']['linkedInteraction']:
                event.linkedInteraction(ty, tx, 400, {"block" : "same_", "id" : 401, "type" : 0, "nbt":{"link" : True}}, cc['fg']['F'])
            else: roomGrid[ty][tx] = obj('-bb', '401', nbt={'link':True})
            ty, tx = bfy, bfx

            addLog(
                f"{s.playerColor[0]}당신{cc['end']}의 몸에서 {cc['fg']['F']}저주{cc['end']}가 빠져나가는 것이 느껴집니다...",
                colorKey='A'
            )
            say(choice(c.curseDecrease[commentType]))

    elif blockID == 401:
        sound      = ("player", "hit")
        ty, tx     = bfy, bfx
        s.Dy, s.Dx = bfDy, bfDx
        addLog(f"이 {cc['fg']['A']}신상{cc['end']}은 이미 {cc['fg']['F']}저주{cc['end']}에 물들었습니다...", colorKey='F')

    elif blockID in [501, 502]:
        sound = ("player", "getItem")
        exec(f"{['s.Mhp', 's.Mdf'][blockID-501]}+=3")

    elif blockID == 900:
        sound = ("object", "ashChip", "get")
        count = block["nbt"]["count"]
        if count:
            s.ashChip += count
            addLog(f"{cc['fg']['G1']}잿조각{cc['end']}을 {cc['fg']['G1']}{count}{cc['end']}개 얻었습니다.", colorKey='G1')
            cs.ashChipCheck()

    statusEffect.tickProgress("fore")

    s.y, s.x                                = ty, tx
    s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = s.steppedBlock
    s.steppedBlock = s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]\
            if s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['id'] in s.interactableBlocks['steppable']['maintainable']\
        else obj('-bb', '0')
    s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = obj('-bb', '300', block=iset(s.ids[300]))
    if sound: play(*sound)

    statusEffect.tickProgress("back")

def observe(Dir) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    ty, tx = s.y, s.x
    match Dir:
        case curses.KEY_UP   : ty -= 1
        case curses.KEY_DOWN : ty += 1
        case curses.KEY_LEFT : tx -= 1
        case curses.KEY_RIGHT: tx += 1

    titleOnly    = False
    block = roomGrid[ty][tx]
    
    match block['id']:
        case 200:
            if block['hashKey'] in s.friendlyEntity:
                block['nbt'] = {"link" : True}

    data = iWin.dataRegistration(
        block['id'],
        s.types[block['type']],
        block
    )

    if not data:
        titleOnly  = True
        targetType = {
            0 : "블록",
            1 : "엔티티",
            2 : "아이템"
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
    if s.target['hashKey']:
        s.target['attackable'] = True
        s.target['command']    = True
        addLog(
            f"{cc['fg']['L']}타겟{cc['end']}을 {cc['fg']['R']}집중 공격 대상{cc['end']}으로 설정합니다!",
            colorKey='L'
        )
        
    else: addLog("아무런 일도 일어나지 않았습니다...", colorKey='L')

def getRoomData() -> None:
    room    = s.Dungeon[s.Dy][s.Dx]
    lineLen = map(lambda l: len(l), room['room'])

    s.roomData['type'] = room['name']
    s.roomData['cell'] = sum(lineLen)

    s.roomData['maxHeight'] = len(room['room'])
    s.roomData['maxWidth']  = len(max(room['room'], key=len))

    s.roomData['maxCharWidth'] = s.roomData['maxWidth']*2