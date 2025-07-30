from ..base import BlockBehavior

from Assets.data import totalGameStatus as s

from Game.entities.player.event import (
    getRoomData,
    damagedByBlock
)


class Door(BlockBehavior):
    def interact(self, **data):
        if data['block']['nbt']['lock']:
            return data['bfy'], data['bfx'], damagedByBlock(data['block']['block'])

        else:
            s.Dy, s.Dx, data['ty'], data['tx'] = data['block']['nbt']['wp']

            s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2

            for i, (DyOffset, DxOffset) in enumerate(((-1, 0), (0, 1), (1, 0), (0, -1))):
                Ny = s.Dy+DyOffset
                Nx = s.Dx+DxOffset

                if  0<=Ny<len(s.Dungeon)\
                and 0<=Nx<len(s.Dungeon[0]):
                    neighbor = s.Dungeon[Ny][Nx]

                    if  neighbor\
                    and neighbor['isPlayerVisited']                      ==0\
                    and list(s.Dungeon[s.Dy][s.Dx]['doors'].values())[i]==1:
                        neighbor['isPlayerVisited'] = 1

            s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

            getRoomData()

        return data['ty'], data['tx'], ("object", "door", "open")