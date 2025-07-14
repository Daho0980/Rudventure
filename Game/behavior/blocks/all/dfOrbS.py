from ..base        import BlockBehavior
from ..orbStandard import interactSound

from Game.entities.player.event import sayCmt
from Game.utils.system.sound    import play

from Assets.data import(
    totalGameStatus as s,
    comments        as c
)


class DfOrbS(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['S']['df']

        if s.df == s.Mdf:
            target = c.getOrb['df']['dfTooOver']
            sayCmt(target['cmt']['S'], target['prob'])

            return data['ty'], data['tx'], interactSound()
        
        if (s.df+point) > s.Mdf:
            s.df = s.Mdf

            target = c.getOrb['df']['dfOver']
            sayCmt(target['cmt']['S'], target['prob'])

            return data['ty'], data['tx'], interactSound()
        
        s.df += point

        if s.df == s.Mdf:
            play("system", "perfectLvlUp")
            s.exaltation += 10

            target = c.getOrb['df']['dfFull']
            sayCmt(target['cmt']['S'], target['prob'])

        elif s.df == point:
            target = c.getOrb['df']['restorationed']
            sayCmt(target['cmt']['S'], target['prob'])

        return data['ty'], data['tx'], interactSound()