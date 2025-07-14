from Assets.data             import totalGameStatus as s
from Game.utils.system.block import iset

from Game.core.system.data.dataLoader import (
    obj
)
from Game.utils.system.roomManager.interactions import (
    randPlaceOrb
)


def event() -> None:
    s.Dungeon[s.Dy][s.Dx]['room'][11][11] = obj('-bb', 'exit', block=iset(s.bids['exit']))
    s.Dungeon[s.Dy][s.Dx]['interaction']  = True
    randPlaceOrb(2)

    s.exaltation += 5