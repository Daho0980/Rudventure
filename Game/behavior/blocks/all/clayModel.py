from ..base import BlockBehavior

from Assets.data                import totalGameStatus as s
from Game.entities.player.event import readSign

from Game.core.system.data.dataLoader import (
    obj
)


class ClayModel(BlockBehavior):
    def interact(self, **data):
        nbt = data['block']['nbt']

        s.DungeonMap[s.Dy][s.Dx] = ('☷', 'O')
        readSign(
            nbt['texts'],
            nbt['delay'],
            nbt['voice'],
            nbt['command']
        )

        s.Dungeon[s.Dy][s.Dx]['room'][data['ty']][data['tx']] = obj(
            '-bb', 'deadClayModel',
            nbt={ 'link' : True }
        )

        return data['ty'], data['tx'], data['sound']