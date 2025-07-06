from ..base        import BlockBehavior
from ..orbStandard import interactSound

from random import randrange, choice

from Game.entities.player.event import say
from Game.utils.system.sound    import play

from Assets.data import(
    totalGameStatus as s  ,
    percentage      as per,
    comments        as c
)


class DfOrbS(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['S']['df']

        if s.df == s.Mdf:
            say(choice(c.getOrb['df']['dfTooOver']['S']))

            return data['ty'], data['tx'], interactSound()
        
        if (s.df+point) > s.Mdf:
            s.df = s.Mdf
            say(choice(c.getOrb['df']['dfOver']['S']))

            return data['ty'], data['tx'], interactSound()
        
        s.df += point

        if s.df == s.Mdf:
            play("system", "perfectLvlUp")
            s.exaltation += 10

        if randrange(1, 101) <= per.getOrb:
            if s.df == s.Mdf:
                say(choice(c.getOrb['df']['dfFull']['S']))

            elif s.df == point:
                say(choice(c.getOrb['df']['restorationed']['S']))

        return data['ty'], data['tx'], interactSound()