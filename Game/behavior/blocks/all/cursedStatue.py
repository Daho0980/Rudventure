from ..base import BlockBehavior

from Assets.data.color import cColors as cc

from Game.core.system.io.logger import (
    addLog
)


class CursedStatue(BlockBehavior):
    def interact(self, **data):
        addLog(
            f"이 {cc['fg']['A']}신상{cc['end']}은 이미 {cc['fg']['F']}저주{cc['end']}에 물들었습니다...",
            colorKey='F'
        )

        return data['ty'], data['tx'], ("player", "hit")