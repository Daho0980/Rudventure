import time
import threading

from Assets.data        import status    as s
from Assets.data.color  import cColors   as cc
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