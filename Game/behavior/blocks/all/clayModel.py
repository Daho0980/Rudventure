from ..base import BlockBehavior

from Assets.data                import totalGameStatus as s
from Game.entities.player.event import readSign
from Game.tools                 import block


class ClayModel(BlockBehavior):
    def interact(self, **data):
        s.DungeonMap[s.Dy][s.Dx] = ('☷', 'O')
        readSign(**data['block']['nbt'])

        block.place(
            block.get(
                'deadClayModel',
                nbt={ 'link' : True }
            ),
            data['ty'], data['tx']
        )

        return data['ty'], data['tx'], data['sound']