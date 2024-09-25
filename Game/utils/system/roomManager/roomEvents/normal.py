from random import randrange, choice

from Assets.data             import percentage, comments, status
from Game.entities.player    import say
from Game.utils.system.sound import play

from Game.utils.system.roomManager.interactions import (
    changeDoorPosBlock,
    placeRandomOrbs,
    summonMonster
)


s, p, c = status, percentage, comments

def event(data) -> None:
    if data['summonCount'] > 0:
        play("object", "door", "close")
        if randrange(1, 101) <= p.enterinBattleComment:
            say(choice(
                c.enterinBattleComments[5]\
                if   data['summonCount'] >= 5\
                else c.enterinBattleComments[0]
            ))
        summonMonster(data)

        changeDoorPosBlock(1, data)
    elif not s.enemyCount and s.roomLock:
        s.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        if randrange(0, 101) > p.clearedRoomLoot: placeRandomOrbs()
        changeDoorPosBlock(2, data)