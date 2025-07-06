from ..base        import BlockBehavior
from ..orbStandard import interactSound

from Assets.data       import totalGameStatus as s
from Game.utils.system import xpSystem



class CsOrbS(BlockBehavior):
    def interact(self, **data):
        xpSystem.getXP(s.orbData['S']['cs'])

        return data['ty'], data['tx'], interactSound()