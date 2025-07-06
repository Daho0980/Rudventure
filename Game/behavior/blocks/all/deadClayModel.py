from ..base import BlockBehavior

from Assets.data.color          import cColors as cc
from Game.core.system.io.logger import addLog


class DeadClayModel(BlockBehavior):
    def interact(self, **data):
        addLog(
            f"당신 앞에는 그저 {cc['fg']['O']}흙더미{cc['end']}가 자리를 지키고 있을 뿐입니다...",
            colorKey='O'
        )

        return data['ty'], data['tx'], ("player", "interaction", "open")