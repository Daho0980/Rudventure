from Assets.data             import totalGameStatus as s
from Game.utils.system.block import iset

from Game.core.system.data.dataLoader import (
    obj
)


def event() -> None:
    s.Dungeon[s.Dy][s.Dx]['room'][11][11] = obj('-bb', 'exit', block=iset(s.bids['exit']))
    s.Dungeon[s.Dy][s.Dx]['interaction']  = True

    s.exaltation += 5