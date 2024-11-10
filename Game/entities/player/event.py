import time
import threading
from   copy     import deepcopy
from   random   import choice, randrange

from Assets.data.color        import cColors as cc
from Assets.data              import lockers as l
from Game.core.system         import logger
from Game.entities            import player as p
from Game.utils.system.tts    import TTS, TTC
from Game.utils.graphics      import escapeAnsi
from Game.utils.system.sound  import play # 계속 이거 지우는데 지우지마라

from Assets.data import (
    status   as s,
    comments as c # 얘도 쓰는거임
    )


def hitted() -> None:
    def event() -> None:
        if s.ids[300].startswith(cc['fg']['R']):
            s.ids[300] = escapeAnsi(s.ids[300])
        else:
            icon:str      = s.ids[300][:]
            character:str = escapeAnsi(choice(s.playerDamageIcon))

            s.ids[300] = f"{cc['fg']['R']}{character}{cc['end']}"
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
            time.sleep(0.03)
            s.ids[300] = icon[:]
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]

    threading.Thread(target=event, daemon=True).start()

def defended() -> None:
    def event() -> None:
        if s.ids[300].startswith(cc['fg']['B1']):
            s.ids[300] = escapeAnsi(s.ids[300])
        else:
            icon:str      = s.ids[300][:]
            character:str = escapeAnsi(choice(s.playerDamageIcon))

            s.ids[300] = f"{cc['fg']['B1']}{character}{cc['end']}"
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
            time.sleep(0.03)
            s.ids[300] = icon[:]
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]

    threading.Thread(target=event, daemon=True).start()

def cursedDeath() -> None:
    def event() -> None:
        s.killAll = True
        l.isDying = True
        logger.clear()

        s.DROD = [f"{cc['fg']['F']}저주받음{cc['end']}", 'F']

        p.say("큭..")
        s.ids[300]                                       = f"{cc['fg']['F']}{escapeAnsi(s.ids[300])}{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        time.sleep(1.5)

        s.ids[300]                                       = f"{cc['fg']['F']}a{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        p.say(f"크{cc['fg']['F']}으윽...")
        time.sleep(1.7)

        p.say("크아아아아아아악!!!!!!", TextColor=cc['fg']['F'])
        while s.hp!=1:
            s.hp -= 1
            time.sleep(0.15)
        s.ids[300]                                       = f"{cc['fg']['F']}o{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        time.sleep(0.1)

        s.ids[300]                                       = f"{cc['fg']['F']}'{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        time.sleep(0.1)

        s.ids[300]                                       = f"{cc['fg']['F']}.{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        time.sleep(0.2)

        s.ids[300]                                       = " "
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        time.sleep(1)
        s.hp -= 1

    
    threading.Thread(target=event, daemon=True).start()

def readSign(texts, delay, voice, command="") -> None:
    def target() -> None:
        nonlocal texts, delay

        for line in texts:
            if isinstance(line, list):
                exec(line[1])
                logger.addLog(line[0], duration=max(50, TTC(line[0])))
                TTS(line[0], voicePath=("object", "clayModel", "voice", voice))
            else:
                logger.addLog(line, duration=max(50, TTC(line)))
                TTS(line, voicePath=("object", "clayModel", "voice", voice))
            time.sleep(delay)
        exec(command)
    
    threading.Thread(target=target, daemon=True).start()

def linkedInteraction(y:int, x:int, _id:int, afterData:dict, color:str):
    for r in range(y-1, y+2):
        for c in range(x-1, x+2):
                    if s.Dungeon[s.Dy][s.Dx]['room'][r][c]['id'] == _id:
                        if afterData['block'] == "same_":
                            CData = deepcopy(afterData)
                            CData['block'] = f"{color}{escapeAnsi(s.Dungeon[s.Dy][s.Dx]['room'][r][c]['block'])}{cc['end']}" 
                        s.Dungeon[s.Dy][s.Dx]['room'][r][c] = CData
                        linkedInteraction(r, c, _id, afterData, color)
                    else: continue
