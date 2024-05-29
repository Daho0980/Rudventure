from random import choice

from Assets.data          import comments, status
from Game.entities.player import say


c, s = comments, status

def event(cmt) -> None:
    if cmt: say(choice(c.treasureRoomComment[s.Dungeon[s.Dy][s.Dx]['treasureRarity']]))
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True