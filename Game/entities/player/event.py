import time
import threading

from Assets.data              import status    as s
from Assets.data.color        import cColors   as cc
from Assets.data              import lockers   as l
from Game.core.system         import logger
from Game.entities            import player    as p
from Game.utils.system.tts    import TTS
from Game.utils.graphics      import escapeAnsi


def hitted() -> None:
    def event() -> None:
        if s.ids[300] != f"{cc['fg']['R']}{escapeAnsi(s.ids[300])}{cc['end']}":
            icon:str      = s.ids[300][:]
            character:str = escapeAnsi(icon)

            s.ids[300] = f"{cc['fg']['R']}{character}{cc['end']}"
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

        p.say("크아아아아아아악!!!!!!", TextColor='F')
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

def readSign(texts, delay, voice) -> None:
    def target() -> None:
        nonlocal texts, delay

        for line in texts:
            if isinstance(line, list):
                exec(line[1])
                logger.addLog(line[0])
                TTS(line[0], voicePath=("object", "clayModel", "voice", voice))
            else:
                logger.addLog(line)
                TTS(line, voicePath=("object", "clayModel", "voice", voice))
            time.sleep(delay)
    
    threading.Thread(target=target, daemon=True).start()
