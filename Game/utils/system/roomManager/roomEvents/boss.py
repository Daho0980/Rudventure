from random import randrange, choice

from Game.entities.player        import say
from Game.core.system.dataLoader import obj
from Game.utils.system.sound     import play

from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    comments        as c
)
from Game.utils.system.roomManager.interactions import (
    summonMonster,
    randPlaceOrb,
    changeDoor,
)


def event(data) -> None:
    if data['summonCount'] > 0:
        if randrange(1,101) <= p.enterinBattle:
            say(choice(c.enterinBattle[0]))
        play("object", "door", "close")
        summonMonster(data, 3, 2, 10, boss=True)

        s.Dungeon[s.Dy][s.Dx]['room'][11][11] = obj('-bb', '0')
        changeDoor(1, data)
    elif not s.enemyCount and s.roomLock:
        s.roomLock                             = False
        s.Dungeon[s.Dy][s.Dx]['room'][11][11]  = obj('-bb', '5')
        s.Dungeon[s.Dy][s.Dx]['interaction']   = True
        randPlaceOrb(2)
        changeDoor(2, data)
        play("object", "door", "open")