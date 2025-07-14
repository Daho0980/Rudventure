from ..base        import BlockBehavior
from ..orbStandard import interactSound

from Game.entities.player.event import sayCmt

from Assets.data import(
    totalGameStatus as s,
    comments        as c
)


class HgOrbS(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['S']['hg']

        if (s.hgr+point) > s.Mhgr:
            s.hgr = s.Mhgr

            target = c.getOrb['hgr']['over']
            sayCmt(target['cmt']['S'], target['prob'])

            return data['ty'], data['tx'], interactSound()
        
        s.hgr += point

        return data['ty'], data['tx'], interactSound()