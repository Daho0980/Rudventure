from Assets.data.color          import cColors as cc
from Game.core.system.io.logger import addLog
from Game.utils.system.sound    import play

from Assets.data import (
    totalGameStatus as s,
    flags           as f
)
from Game.utils.system.roomManager.interactions import (
    changeDoor
)


def event0(data) -> None:
    if not data['summonData'] and s.enemyCount:
        data['summonData'] = ['command.roomEnd']
        f.roomLock = True

        changeDoor('close', data['name'], data['doors'], "░░")
        play("object", "door", "close")

    if not s.enemyCount and f.roomLock:
        f.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True

        s.exaltation += 5
        
        changeDoor('open', data['name'], data['doors'], ". ")
        play("object", "door", "open")

def event1() -> None:
    addLog(f"{cc['fg']['A']}신상{cc['end']} 주변으로부터 약한 순풍이 {s.playerColor[0]}당신{cc['end']}에게 불어옵니다...", colorKey='A')
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True
def event2() -> None: ...
def event3() -> None: ...
def event4() -> None: ...
def event5() -> None: ...