from ..base import BlockBehavior

from random import randrange, choice

from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from Game.tools              import block
from Game.utils.system.block import iset


class Flower(BlockBehavior):
    def interact(self, **data):
        if data['block']['nbt']['step']:
            ty, tx    = data['ty'], data['tx']
            roomGrid  = s.Dungeon[s.Dy][s.Dx]['room']
            blockData = data['block']

            flowerColor = blockData['nbt']['color']

            for pos in (
                (ty-1, tx),
                (ty, tx+1),
                (ty+1, tx),
                (ty, tx-1)
            ):
                if  roomGrid[pos[0]][pos[1]]['id']=='floor' and\
                not randrange(0,3):
                    block.place(
                        block.get(
                            'petal',
                            block=f"{cc['fg'][flowerColor]}. {cc['end']}",
                            nbt  ={'link' : True}
                        ) if blockData['nbt']['step']==1 else block.get(
                            'flower',
                            block=f"{cc['fg'][flowerColor]}{iset(choice(['*',',','.','_']), Type='s')}{cc['end']}",
                            nbt  ={
                                "color" : flowerColor,
                                "step"  : blockData['nbt']['step']-1
                            }
                        ),
                        *pos
                    )

        return ty, tx, ("player", "interaction", "step", "flower")