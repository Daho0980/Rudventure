from ..base import StatusEffect

from Assets.data                import totalGameStatus as s
from Assets.data.color          import cColors         as cc
from Game.core.system.io.logger import addLog
from Game.utils.system.sound    import echo, play


class Kitrima(StatusEffect):
    def tick(self, effect) -> None:
        if not effect['tick']%15 or effect['tick']==1:
            s.hp -= 1
            echo(
                "entity", "enemy", "pain", "growl",
                feedback=50,
                vVolume =65
            )
            play("player", "hit")

            addLog(
                f"{cc['fg']['F']}계속해서 이명이 들려옵니다...{cc['end']}",
                colorKey='F'
            )

            s.DROD = (f"{cc['fg']['F']}비명{cc['end']}", 'F')