from random import choice

from Game.entities.player import say

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


def event(cmt) -> None:
    if cmt: say(choice(c.treasureRoomComments[s.Dungeon[s.Dy][s.Dx]['treasureRarity']]))
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True