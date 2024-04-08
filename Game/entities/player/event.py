import time
import threading

from Assets.data        import status    as s
from Assets.data.color  import cColors   as cc
from Assets.data        import lockers   as l
from Game.core.system   import logger
from Game.utils.graphic import escapeAnsi


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

        logger.addLog(f"{cc['fg']['L']}\"큭..\"{cc['end']}", 200)
        s.ids[300]                                       = f"{cc['fg']['F']}{escapeAnsi(s.ids[300])}{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        time.sleep(1.5)

        s.ids[300]                                       = f"{cc['fg']['F']}a{cc['end']}"
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]['block'] = s.ids[300]
        logger.addLog(f"{cc['fg']['L']}\"크{cc['fg']['F']}으윽...\"{cc['end']}")
        time.sleep(1.7)

        logger.addLog(f"{cc['fg']['F']}\"크아아아아아아악!!!!!!\"{cc['end']}")
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
