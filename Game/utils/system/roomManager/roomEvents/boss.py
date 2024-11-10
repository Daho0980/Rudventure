from random import randrange, choice

from Game.entities.player    import say
from Game.utils.system.sound import play

from Assets.data import (
    percentage as p,
    comments   as c,
    status     as s
)
from Game.utils.system.roomManager.interactions import (
    placeRandomOrbs,
    summonMonster,
    changeDoor,
)


def event(data) -> None:
    if data['summonCount'] > 0:
        play("object", "door", "close")
        if randrange(1,101) <= p.enterinBattleComment:
            say(choice(c.enterinBattleComments[0]))
        summonMonster(
            data, 3, 2, 10,
            boss=True
            )

        s.Dungeon[s.Dy][s.Dx]['room'][11][11] = {"block" : s.ids[0], "id" : 0, "type" : 0}
        changeDoor(1, data)
    elif not s.enemyCount and s.roomLock:
        s.roomLock                             = False
        s.Dungeon[s.Dy][s.Dx]['room'][11][11]  = {"block" : s.ids[5], "id" : 5, "type" : 0}
        s.Dungeon[s.Dy][s.Dx]['interaction']   = True
        placeRandomOrbs(multiple=2)
        changeDoor(2, data)