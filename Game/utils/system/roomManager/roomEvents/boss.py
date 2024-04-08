from Assets.data                     import status as s
from Game.utils.system.roomManager.interactions import (
    changeDoorPosBlock,
    summonMonster,
    placeRandomOrbs
)

def event(data) -> None:
    if data['summonCount'] > 0:
        summonMonster(
            data, 3, 2, 10,
            boss=True
            )

        s.Dungeon[s.Dy][s.Dx]['room'][6][6] = {"block" : s.ids[0], "id" : 0}
        changeDoorPosBlock(1, data)
    elif not s.entityCount and s.roomLock:

        s.roomLock = False
        s.Dungeon[s.Dy][s.Dx]['room'][6][6]  = {"block" : s.ids[5], "id" : 5}
        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
        placeRandomOrbs(multiple=2)
        changeDoorPosBlock(2, data)