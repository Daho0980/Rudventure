from random import randrange, choice

from Game.entities.player.event import say
from Game.utils.system.block    import iset
from Game.utils.system.sound    import play

from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    comments        as c,
    flags           as f
)
from Game.core.system.data.dataLoader import (
    obj
)
from Game.utils.system.roomManager.interactions import (
    randPlaceOrb,
    summonEnemy,
    changeDoor
)


def event(data) -> None:
    if data['summonData']:
        if randrange(1,101) <= p.enterinBattle:
            say(choice(c.enterinBattle[0]))

        s.Dungeon[s.Dy][s.Dx]['room'][11][11] = obj('-bb', 'floor')
        changeDoor('wall', data, "░░")
        play("object", "door", "close")

        summonEnemy(data['summonData'], 3, 2, randrange(5, 11))

    elif not s.enemyCount and f.roomLock:
        f.roomLock                            = False
        s.Dungeon[s.Dy][s.Dx]['room'][11][11] = obj('-bb', 'exit', block=iset(s.bids['exit']))
        s.Dungeon[s.Dy][s.Dx]['interaction']  = True
        randPlaceOrb(2)

        s.exaltation += 5

        changeDoor('door', data)
        play("object", "door", "open")