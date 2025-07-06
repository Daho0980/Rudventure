from ..base import StatusEffect

from Assets.data             import totalGameStatus as s
from Game.utils.system.block import iset

from Game.core.system.data.dataLoader import (
    obj
)


class BloodStomping(StatusEffect):
    def tick(self, effect) -> None:
        s.steppedBlock = obj(
            '-bb', 'blood',
            block=iset(s.bloodIcon[1]),
            nbt  ={
                "link" : False,
                "stack" : 1
            },
            blockData=s.steppedBlock
        )