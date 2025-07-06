from ..base import BlockBehavior

from random import choices

from Assets.data             import totalGameStatus as s
from Game.utils.system.block import iset

from Game.core.system.data.dataLoader import (
    obj
)


class OrbBox(BlockBehavior):
    def interact(self, **data):
        orbBoxEvent(
            data['ty'],
            data['tx'],
            data['block']['nbt']['face']
        )

        return data['ty'], data['tx'], ("object", "itemBox", "open")


def orbBoxEvent(y:int, x:int, face:str) -> None:
    orbId = f"{choices(
        ('hg', 'hp', 'df', 'atk', 'cs'),
        weights=(45, 15, 10, 5, 15),
        k      =1
    )[0]}Orb{choices(
        ('S', 'B'),
        weights=(60, 40),
        k      =1
    )[0]}"

    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = obj(
        '-bb', orbId,
        block=iset(s.bids[orbId], Type=face)
    )