import time ; import threading
from   copy   import deepcopy
from   random import randrange, shuffle, choice

from Assets.data.color       import cColors as cc
from Assets.data.permissions import Player  as perm
from functions.grammar       import pstpos  as pp
from Game.entities           import player  as p
from Game.core.system.io     import logger
from Game.utils.system.tts   import TTS, TTC
from Game.utils.graphics     import escapeAnsi
from Game.utils.system.block import iset
from Game.utils.system.sound import play # 이거 씀

from Assets.data import (
    totalGameStatus as s,
    comments        as c, # 얘도 쓰는거임
    flags           as f
    )
from Game.core.system.data.dataLoader import (
    obj
)


def hitted() -> None:
    def event() -> None:
        if s.eids['player1'].startswith(cc['fg']['R']):
            s.eids['player1'] = escapeAnsi(s.eids['player1'])
        else:
            icon      = s.eids['player1'][:]
            character = escapeAnsi(choice(s.playerDamageIcon))

            s.eids['player1'] = f"{cc['fg']['R']}{character}{cc['end']}"
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
            time.sleep(0.03)
            s.eids['player1'] = icon[:]
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])

    threading.Thread(target=event, daemon=True).start()

def damagedByBlock(block:str="?", atk:int=1) -> tuple:
    sound = ("player", "hit")
    hitted()
    logger.addLog(
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
            logger.addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!", colorKey='B1')

    else: dmg = atk

    s.hp -= dmg
    bleeding(dmg)

    if s.hp <= 0: s.DROD = [
        f"{cc['fg']['R']}{choice(["과다출혈","피로 과다","졸도","자살","우울증","과로"])}{cc['end']}",
        'R'
    ]

    return sound

def defended() -> None:
    def event() -> None:
        if s.eids['player1'].startswith(cc['fg']['B1']):
            s.eids['player1'] = escapeAnsi(s.eids['player1'])
        else:
            icon      = s.eids['player1'][:]
            character = escapeAnsi(choice(s.playerDamageIcon))

            s.eids['player1']                                = f"{cc['fg']['B1']}{character}{cc['end']}"
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
            time.sleep(0.03)
            s.eids['player1']                                = icon[:]
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])

    threading.Thread(target=event, daemon=True).start()

def cursedDeath() -> None:
    def event() -> None:
        f.killAll = True
        f.isDying = True
        logger.clear()

        s.DROD = [f"{cc['fg']['F']}저주받음{cc['end']}", 'F']

        say("큭..")
        s.eids['player1']                                = f"{cc['fg']['F']}{escapeAnsi(s.eids['player1'])}{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
        time.sleep(1.5)

        s.eids['player1']                                = f"{cc['fg']['F']}a{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
        say(f"크{cc['fg']['F']}으윽...")
        time.sleep(1.7)

        say("크아아아아아아악!!!!!!", TextColor=cc['fg']['F'])
        while s.hp!=1:
            s.hp -= 1
            time.sleep(0.15)
        s.eids['player1']                                = f"{cc['fg']['F']}o{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
        time.sleep(0.1)

        s.eids['player1']                                = f"{cc['fg']['F']}'{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
        time.sleep(0.1)

        s.eids['player1']                                = f"{cc['fg']['F']}.{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
        time.sleep(0.2)

        s.eids['player1']                                = " "
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = iset(s.eids['player1'])
        time.sleep(1)
        s.hp -= 1
    
    threading.Thread(target=event, daemon=True).start()

def _linkedSay(lines:list[str]) -> None:
    def target():
        nonlocal lines
        for line in lines:
            say(line); time.sleep(TTC(line, logTick=False)+1)

    threading.Thread(target=target, daemon=True).start()

def say(text:str, TextColor:str="pc") -> None:
    if isinstance(text, list): _linkedSay(text); return

    logger.addLog(
        f"{s.playerColor[0] if TextColor=='pc'else TextColor}\"{text}\"{cc['end']}",
        duration=max(50, TTC(text)),
        colorKey=s.playerColor[1]
    )
    threading.Thread(
        target=lambda: TTS(text, voicePath=("player", "voice", s.playerVoice)),
        daemon=True
    ).start()

def readSign(texts, delay, voice, command="") -> None:
    def target() -> None:
        nonlocal texts, delay

        for line in texts:
            if isinstance(line, list):
                exec(line[1])
                logger.addLog(line[0], duration=max(50, TTC(line[0])))
                TTS(line[0], voicePath=("object", "clayModel", "voice", voice), useLvl=False)

            else:
                logger.addLog(line, duration=max(50, TTC(line)))
                TTS(line, voicePath=("object", "clayModel", "voice", voice), useLvl=False)
            time.sleep(delay)
        exec(command)
    
    threading.Thread(target=target, daemon=True).start()

def getRoomData() -> None:
    room = s.Dungeon[s.Dy][s.Dx]

    s.roomData['type'] = room['name']
    s.roomData['cell'] = sum(map(lambda l:len(l),room['room']))

    s.roomData['maxHeight'] = len(room['room'])
    s.roomData['maxWidth']  = len(max(room['room'], key=len))

    s.roomData['maxCharWidth'] = s.roomData['maxWidth']*2

def linkedInteraction(y:int, x:int, _id:str, afterData:dict, color:str):
    for r in range(y-1, y+2):
        for c in range(x-1, x+2):
            if s.Dungeon[s.Dy][s.Dx]['room'][r][c]['id'] == _id:
                if afterData['block'] == "_same":
                    CData          = deepcopy(afterData)
                    CData['block'] = f"{color}{escapeAnsi(s.Dungeon[s.Dy][s.Dx]['room'][r][c]['block'])}{cc['end']}" 

                s.Dungeon[s.Dy][s.Dx]['room'][r][c] = CData
                linkedInteraction(r, c, _id, afterData, color)
                        
            else: continue

def _bloodOverflow(y:int, x:int, stack:int, pos=None):
    if pos == None: pos = []

    neighbors = [(y+dy,x+dx)for dy in(-1,0,1)for dx in(-1,0,1)if not(dy==0 and dx==0)]
    shuffle(neighbors)
    
    for row, col in neighbors:
            if (row, col) in pos: continue
            
            target = s.Dungeon[s.Dy][s.Dx]['room'][row][col]
            if perm.data[target['id']] & perm.STEP:
                pos.append((row, col))

                if target['id'] == 'blood':
                    targetStack            = min(stack+target['nbt']['stack'], 5)
                    target['nbt']['stack'] = targetStack
                    target['block']        = iset(s.bloodIcon[targetStack])

                    stack -= 5-targetStack

                else:
                    currStack = min(stack, 5)
                    stack    -= 5

                    s.Dungeon[s.Dy][s.Dx]['room'][row][col] = obj(
                        '-bb', 'blood',
                        block=iset(s.bloodIcon[currStack]),
                        nbt  ={
                            "link"  : True,
                            "stack" : currStack,
                        },
                        blockData = target
                    )

                if stack > 0:
                    stack = _bloodOverflow(row, col, stack, pos)
                    
                if stack <= 0: break

            else: continue
    
    return stack

def bleeding(hp:int, multiply:bool=True) -> None:
    hp      *= randrange(1,3) if multiply else 1
    roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
    qot, rem = divmod(hp, 4)
    stk      = {dirN : qot for dirN in ("U","R","D","L")}

    for Dir, dirN in zip(
        ((s.y-1,s.x),(s.y,s.x+1),(s.y+1,s.x),(s.y,s.x-1)),
        ("U","R","D","L")
    ):
        if not perm.data[roomGrid[Dir[0]][Dir[1]]['id']] & perm.STEP:
            del stk[dirN]

    dirKey = list(stk.keys())
    if not dirKey: return
    
    for _ in range(rem): stk[dirKey[randrange(0,len(dirKey))]] += 1

    pos = {
        "U" : (s.y-1, s.x  ),
        "R" : (s.y  , s.x+1),
        "D" : (s.y+1, s.x  ),
        "L" : (s.y  , s.x-1)
    }
    for dirN in (i for i in dirKey if stk[i]):
        y, x  = pos[dirN]
        stack = stk[dirN]
        
        if roomGrid[y][x]['id'] == 'blood':
            targetStack                    = min(stack+roomGrid[y][x]['nbt']['stack'], 5)
            roomGrid[y][x]['nbt']['stack'] = targetStack
            roomGrid[y][x]['block']        = iset(s.bloodIcon[targetStack])

            stack -= 5-targetStack

            if stack > 0: _bloodOverflow(y, x, stack)
        
        else:
            stack          = min(stack, 5)
            roomGrid[y][x] = obj(
                '-bb', 'blood',
                block=iset(s.bloodIcon[stack]),
                nbt  ={
                    "link"  : True,
                    "stack" : stack,
                },
                blockData=roomGrid[y][x]
            )