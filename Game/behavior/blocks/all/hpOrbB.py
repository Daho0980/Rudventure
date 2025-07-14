from ..base        import BlockBehavior
from ..orbStandard import interactSound

from Game.entities.player.event import sayCmt
from Game.utils.system.sound    import play

from Assets.data import(
    totalGameStatus as s,
    comments        as c
)


class HpOrbB(BlockBehavior):
    def interact(self, **data):
        point = s.orbData['B']['hp']

        if s.hp == s.Mhp:
            target = c.getOrb['hp']['hpTooOver']
            sayCmt(target['cmt']['B'], target['prob'])

            return data['ty'], data['tx'], interactSound()

        if (s.hp+point) > s.Mhp:
            s.hp = s.Mhp

            target = c.getOrb['hp']['hpOver']
            sayCmt(target['cmt']['B'], target['prob'])

            return data['ty'], data['tx'], interactSound()

        s.hp += point

        if s.hp == s.Mhp:
            play("system", "perfectLvlUp")
            s.exaltation += 10

            target = c.getOrb['hp']['hpFull']
            sayCmt(target['cmt']['B'], target['prob'])

            return data['ty'], data['tx'], interactSound()

        if s.hpLow: target = c.getOrb['hp']['hpLow']
        else      : target = c.getOrb['hp']['notHpLow']

        sayCmt(target['cmt']['B'], target['prob'])

        return data['ty'], data['tx'], interactSound()