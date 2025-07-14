from ..base import BlockBehavior

from Assets.data.color import cColors as cc
from Game.tools        import block

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)
from Game.core.system.io.logger import (
    addLog
)
from Game.core.system.data.dataLoader import (
    obj
)
from Game.entities.player.event import (
    linkedInteraction,
    sayCmt
)


class NormalStatue(BlockBehavior):
    def interact(self, **data):
        ty, tx = data['ty'], data['tx']

        if s.lvl < 5:
            data['sound'] = ("player", "hit")

            addLog(
                f"{s.playerColor[0]}당신{cc['end']}은 아직 {cc['fg']['F']}자격{cc['end']}이 주어지지 않았습니다.",
                colorKey='A'
            )

        else:
            data['sound'] = ("player", "interaction", "activate")

            s.DungeonMap[s.Dy][s.Dx] = ('Y', 'F')

            commentType = []
            if s.lvl > (s.Mlvl/2): commentType.append("middle")

            s.lvl -= 5
            s.Mxp -= 15
            s.xp   = 0

            s.exaltation += 20

            commentType.append("Over" if s.lvl>(s.Mlvl/2) else "Under")

            if data['block']['nbt']['linkedInteraction']:
                linkedInteraction(
                    ty, tx, 'normalStatue',
                    {
                        "block" : "_same",
                        "id"    : 'cursedStatue',
                        "type"  : 'block',
                        "nbt"   : { "link" : True }
                    },
                    cc['fg']['F'],
                    delay=0.1
                )

            else: block.place(block.get('cursedStatue', nbt={ "link" : True }), ty, tx)

            addLog(
                f"{s.playerColor[0]}당신{cc['end']}의 몸에서 {cc['fg']['F']}저주{cc['end']}가 빠져나가는 것이 느껴집니다...",
                colorKey='A'
            )
            sayCmt(
                c.curseDecrease['cmt'][''.join(commentType)],
                c.curseDecrease['prob']
            )

        return ty, tx, data['sound']