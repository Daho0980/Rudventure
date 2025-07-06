from ..base import BlockBehavior

from Assets.data       import totalGameStatus as s
from Assets.data.color import cColors as cc

from Game.core.system.io.logger import (
    addLog
)
from Game.entities.player.checkStatus import (
    ashChipCheck
)


class AshChip(BlockBehavior):
    def interact(self, **data):
        count = data['block']['nbt']['count']
        if count:
            s.ashChip += count
            addLog(
                f"{cc['fg']['G1']}잿조각{cc['end']}을 {cc['fg']['G1']}{count}{cc['end']}개 얻었습니다.",
                colorKey='G1'
            )
            ashChipCheck()

        return data['ty'], data['tx'], ("object", "ashChip", "get")