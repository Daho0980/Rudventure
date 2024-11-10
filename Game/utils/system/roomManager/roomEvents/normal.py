from random import randrange, choice

from Game.entities.player    import say
from Game.utils.system.sound import play

from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    comments        as c
)
from Game.utils.system.roomManager.interactions import (
    placeRandomOrbs,
    summonMonster,
    changeDoor,
)


roomData:dict[tuple, str] = {
    (1,1,0,0) : "╚",
    (1,0,1,0) : "║",
    (1,1,1,0) : "╠",
    (1,0,0,1) : "╝",
    (1,1,0,1) : "╩",
    (1,0,1,1) : "╣",
    (0,1,1,0) : "╔",
    (0,1,0,1) : "═",
    (0,1,1,1) : "╦",
    (0,0,1,1) : "╗",
    (1,1,1,1) : "╬",
}

def event(data) -> None:
    if data['summonCount'] > 0:
        doorData = tuple(data['doors'].values())
        if sum(doorData) > 1:
            data['roomIcon'] = [
                roomData[doorData],
                ""
            ]

        play("object", "door", "close")
        if randrange(1, 101) <= p.enterinBattleComment:
            say(choice(
                c.enterinBattleComments[5]\
                if   data['summonCount'] >= 5\
                else c.enterinBattleComments[0]
            ))
        summonMonster(data)

        changeDoor(1, data)
    elif not s.enemyCount and s.roomLock:
        s.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        if randrange(0, 101) > p.clearedRoomLoot: placeRandomOrbs()
        changeDoor(2, data)