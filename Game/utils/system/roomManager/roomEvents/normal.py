from random import randrange

from Assets.data.probs          import dungeon as per
from Game.entities.player.event import sayCmt
from Game.utils.system.sound    import play

from Assets.data import (
    totalGameStatus as s,
    comments        as c,
    flags           as f
)
from Game.utils.system.roomManager.interactions import (
    randPlaceOrb,
    summonEnemy,
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
    if data['summonData']:
        doorData = tuple(data['doors'].values())
        if sum(doorData) > 1:
            s.DungeonMap[s.Dy][s.Dx] = (roomData[doorData], "")

        summonEnemy(data['summonData'])

        sayCmt(
            c.enterinBattle['cmt'][5]\
                if len(data['summonData']) >= 5\
            else c.enterinBattle['cmt'][0],

            c.enterinBattle['prob']
        )

        changeDoor('close', data['name'], data['doors'], "░░")
        play("object", "door", "close")

    elif not s.enemyCount and f.roomLock:
        f.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        if randrange(0, 101) > per.clearedRoomLoot: randPlaceOrb()

        s.exaltation += 5

        changeDoor('open', data['name'], data['doors'], ". ")
        play("object", "door", "open")