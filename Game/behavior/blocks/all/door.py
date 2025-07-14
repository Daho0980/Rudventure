from ..base import BlockBehavior

from Assets.data                import totalGameStatus as s
from Game.entities.player.event import getRoomData
from Game.tools                 import block


class Door(BlockBehavior):
    def interact(self, **data):
        ty, tx = data['ty'], data['tx']

        s.Dungeon[s.Dy][s.Dx]['room'][ty][tx] = block.get('door')

        # ┏>|y, x| : U->D D->U L->R R->L
        pos     = [data['bfy']-ty, data['bfx']-tx]
        wayType = 0

        if   pos[0] ==  1: s.Dy -= 1; wayType = 0
        elif pos[0] == -1: s.Dy += 1; wayType = 1
        elif pos[1] ==  1: s.Dx -= 1; wayType = 2
        elif pos[1] == -1: s.Dx += 1; wayType = 3

        DWPD = {
            'y'  : len(s.Dungeon[s.Dy][s.Dx]['room']   )//2,
            'my' : len(s.Dungeon[s.Dy][s.Dx]['room']   ) -2,
            'x'  : len(s.Dungeon[s.Dy][s.Dx]['room'][0])//2,
            'mx' : len(s.Dungeon[s.Dy][s.Dx]['room'][0]) -2
        }
        wayPoint:list[list[int]] = [
            [DWPD['my'], DWPD['x']],
            [1,          DWPD['x']],
            [DWPD['y'], DWPD['mx']],
            [DWPD['y'],          1]
        ]
        ty, tx = wayPoint[wayType]

        s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2
        roomPos = (
            (s.Dy-1 if s.Dy>0 else s.Dy,                   s.Dx),
            (s.Dy, s.Dx+1 if s.Dx<len(s.Dungeon[0])-1 else s.Dx),
            (s.Dy+1 if s.Dy<len(s.Dungeon)-1 else s.Dy,    s.Dx),
            (s.Dy,                   s.Dx-1 if s.Dx>0 else s.Dx)
        )
            
        for i in range(len(roomPos)):
            if  len(s.Dungeon[roomPos[i][0]][roomPos[i][1]])               >0\
            and s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited']==0\
            and list(s.Dungeon[s.Dy][s.Dx]['doors'].values())[i]          ==1:
                s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] = 1
        s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

        getRoomData()

        return ty, tx, ("object", "door", "open")