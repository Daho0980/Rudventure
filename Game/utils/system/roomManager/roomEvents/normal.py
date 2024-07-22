from random import randrange

from Assets.data                     import status     as s
from Assets.data                     import percentage as p
from Game.utils.system.roomManager.interactions import (
    changeDoorPosBlock,
    summonMonster,
    placeRandomOrbs
)

def event(data) -> None:
    if data['summonCount'] > 0:
        summonMonster(data)

        changeDoorPosBlock(1, data)
    elif not s.entityCount and s.roomLock:
        s.roomLock                           = False
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        if randrange(0, 101) > p.clearedRoomLoot: placeRandomOrbs()
        changeDoorPosBlock(2, data)