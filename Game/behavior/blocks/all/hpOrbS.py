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


class HpOrbS(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['S']['hp']

        if s.hp == s.Mhp:
            say(choice(c.getOrb['hp']['hpTooOver']['S']))

            return data['ty'], data['tx'], interactSound()

        if (s.hp+point) > s.Mhp:
            s.hp = s.Mhp
            say(choice(c.getOrb['hp']['hpOver']['S']))

            return data['ty'], data['tx'], interactSound()

        s.hp += point

        if s.hp == s.Mhp:
            play("system", "perfectLvlUp")
            s.exaltation += 10

        if randrange(1, 101) <= per.getOrb:
            if s.hp == s.Mhp:
                say(choice(c.getOrb['hp']['hpFull']['S']))

                return data['ty'], data['tx'], interactSound()

            if s.hpLow:
                say(choice(c.getOrb['hp']['hpLow']['S']))
            else:
                say(choice(c.getOrb['hp']['notHpLow']['S']))

        return data['ty'], data['tx'], interactSound()