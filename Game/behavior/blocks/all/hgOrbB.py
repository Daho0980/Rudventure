from ..base        import BlockBehavior
from ..orbStandard import interactSound

from random import choice

from Game.entities.player.event import say

from Assets.data import(
    totalGameStatus as s,
    comments        as c
)


class HgOrbB(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['B']['hg']

        if (s.hgr+point) > s.Mhgr:
            say(choice(c.getOrb['hgr']['over']['B']))

            s.hgr = s.Mhgr

            return data['ty'], data['tx'], interactSound()
        
        s.hgr += point

        return data['ty'], data['tx'], interactSound()