from .effects.all      import effectMap
from Assets.data       import totalGameStatus as s
from Assets.data.color import cColors         as cc

from Game.core.system.io.logger import (
    addLog
)


def main(effect, sequence):
    if effect['seq'] != sequence: return

    if effect['id'] in effectMap:
        effectMap[effect['id']].tick(effect)
    else:
        if s.debug:
            addLog(
                f"{cc['fg']['R']}'{effect['id']}'라는 스텝 이펙트가 존재하지 않습니다!{cc['end']}",
                colorKey='R'
            )