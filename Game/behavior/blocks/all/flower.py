from ..base import BlockBehavior

from random import randrange, choice

from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from Game.utils.system.block import iset

from Game.core.system.data.dataLoader import (
    obj
)


class Flower(BlockBehavior):
    def interact(self, **data):
        if data['block']['nbt']['step']:
            ty, tx   = data['ty'], data['tx']
            roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
            block    = data['block']

            flowerColor = block['nbt']['color']

            for pos in [
                (ty-1, tx),
                (ty, tx+1),
                (ty+1, tx),
                (ty, tx-1)
            ]:
                if  roomGrid[pos[0]][pos[1]]['id']=='floor' and\
                not randrange(0,3):
                    roomGrid[pos[0]][pos[1]] = obj(
                        '-bb', 'petal',
                        block=f"{cc['fg'][flowerColor]}. {cc['end']}",
                        nbt  ={'link' : True}
                    ) if block['nbt']['step']==1 else obj(
                        '-bb', 'flower',
                        block=f"{cc['fg'][flowerColor]}{iset(choice(['*',',','.','_']), Type='s')}{cc['end']}",
                        nbt  ={
                            "color" : flowerColor,
                            "step"  : block['nbt']['step']-1
                        }
                    )

        return ty, tx, ("player", "interaction", "step", "flower")