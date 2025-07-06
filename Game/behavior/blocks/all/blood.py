from ..base import BlockBehavior

from random import randrange

from Game.entities.player       import statusEffect
from Game.entities.player.event import bleeding


class Blood(BlockBehavior):
    def interact(self, **data):
        stack = data['block']['nbt']['stack']

        if stack > 2:
            split = randrange(1, 4)
            bleeding(split, False)
            statusEffect.addEffect(
                'bloodStomping',
                stack-split
            )
        
        else:
            statusEffect.addEffect(
                'bloodStomping',
                stack
            )

        return data['ty'], data['tx'], ("player", "interaction", "step", "blood")