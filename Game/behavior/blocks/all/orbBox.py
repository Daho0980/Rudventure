from ..base import BlockBehavior

from random import choices

from Assets.data             import totalGameStatus as s
from Game.tools              import block
from Game.utils.system.block import iset


class OrbBox(BlockBehavior):
    def interact(self, **data):
        orbId = f"{choices(
            ('hg', 'hp', 'df', 'atk', 'cs'),
            weights=(45, 15, 10, 5, 15),
            k      =1
        )[0]}Orb{choices(
            ('S', 'B'),
            weights=(60, 40),
            k      =1
        )[0]}"

        block.place(
            block.get(
                orbId,
                block=iset(s.bids[orbId], Type=data['block']['nbt']['face'])
            ),
            data['ty'], data['tx']
        )

        return data['ty'], data['tx'], ("object", "itemBox", "open")