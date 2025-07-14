from ..base import BlockBehavior

from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from Game.tools              import block
from Game.utils.system.block import iset

from Game.core.system.io.logger import (
    addLog
)


class Squishy0(BlockBehavior):
    def interact(self, **data):
        ty, tx = data['ty'], data['tx']

        face, count, command = list(s.Dungeon[s.Dy][s.Dx]['room'][ty][tx]['nbt'].values())

        if count:
            addLog(
                f"{cc['fg']['B1']}하하, 또 속으셨네요.{cc['end']}"\
                    if count<0\
                else f"{cc['fg']['B1']}{count}{cc['end']}번 남았습니다...",
                colorKey='B1'
            )

            BID = 'squishy1'
            block.place(
                block.get(
                    BID,
                    block=iset(s.bids[BID], Type=face),
                    nbt={
                        "face"    : face,
                        "count"   : count-1,
                        "command" : command
                    }
                ),
                ty, tx
            )
            
        else: command(data['ty'], data['tx'], face)

        return data['bfy'], data['bfx'], ("object", "squishy", "squish")