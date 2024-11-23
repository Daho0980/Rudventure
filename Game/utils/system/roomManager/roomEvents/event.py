from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from Game.core.system.logger import addLog
from Game.utils.system.sound import play

from Game.utils.system.roomManager.interactions import changeDoor


def event0(data) -> None:
    if data['summonCount']==0 and s.enemyCount:
        data['summonCount'] = -1
        s.roomLock          = True
        changeDoor(1, data)
        play("object", "door", "close")
    if not s.enemyCount and s.roomLock:
        s.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        changeDoor(2, data)
        play("object", "door", "open")

def event1() -> None:
    addLog(f"{cc['fg']['A']}신상{cc['end']} 주변으로부터 약한 순풍이 {cc['fg']['L']}당신{cc['end']}에게 불어옵니다...", colorKey='A')
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True
def event2() -> None: ...
def event3() -> None: ...
def event4() -> None: ...
def event5() -> None: ...