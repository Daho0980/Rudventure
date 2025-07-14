from ..base        import BlockBehavior
from ..orbStandard import interactSound

from Game.entities.player.event import sayCmt

from Assets.data import(
    totalGameStatus as s,
    comments        as c
)


class AtkOrbB(BlockBehavior):
    def interact(self, **data):
        s.atk += s.orbData['B']['atk']

        if s.atk > s.stage:
            target = c.getOrb['atk']['hiAtk']
        else:
            target = c.getOrb['atk']['lowAtk']

        sayCmt(target['cmt']['B'], target['prob'])

        return data['ty'], data['tx'], interactSound()