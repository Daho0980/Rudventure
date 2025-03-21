from random import randrange, choice

from Game.entities.player    import say
from Game.utils.system.sound import play

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
            data['roomIcon'] = [roomData[doorData], ""]

        summonMonster(data['summonCount'])

        if randrange(1, 101) <= p.enterinBattle:
            say(choice(
                c.enterinBattle[5]\
                if   data['summonCount'] >= 5\
                else c.enterinBattle[0]
            ))

        changeDoor(1, data, "░░")
        play      ("object", "door", "close")

    elif not s.enemyCount and s.roomLock:
        s.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        if randrange(0, 101) > p.clearedRoomLoot: randPlaceOrb()

        changeDoor(2, data)
        play      ("object", "door", "open")