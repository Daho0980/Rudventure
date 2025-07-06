from ..base        import BlockBehavior
from ..orbStandard import interactSound

from random import randrange, choice

from Game.entities.player.event import say

from Assets.data import(
    totalGameStatus as s  ,
    percentage      as per,
    comments        as c
)


class AtkOrbS(BlockBehavior):
    def interact(self, **data):
        s.atk += s.orbData['S']['atk']

        if randrange(1, 101) <= per.getOrb:
            if s.atk > s.stage:
                say(choice(c.getOrb['atk']['hiAtk']['S']))
            else:
                say(choice(c.getOrb['atk']['lowAtk']['S']))

        return data['ty'], data['tx'], interactSound()