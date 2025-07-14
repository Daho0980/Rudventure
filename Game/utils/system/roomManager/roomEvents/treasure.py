from Game.entities.player.event import sayCmt

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


def event() -> None:
    sayCmt(
        c.treasureRoom['cmt'][s.Dungeon[s.Dy][s.Dx]['treasureRarity']],
        c.treasureRoom['prob']
    )
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True