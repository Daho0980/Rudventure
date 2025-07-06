from ..base        import BlockBehavior
from ..orbStandard import interactSound

from random import choice

from Game.entities.player.event import say

from Assets.data import(
    totalGameStatus as s,
    comments        as c
)


class HgOrbS(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['S']['hg']

        if (s.hgr+point) > s.Mhgr:
            say(choice(c.getOrb['hgr']['over']['S']))

            s.hgr = s.Mhgr

            return data['ty'], data['tx'], interactSound()
        
        s.hgr += point

        return data['ty'], data['tx'], interactSound()