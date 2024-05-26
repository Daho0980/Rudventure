from random import randrange, choice

from Assets.data             import comments, status
from Assets.data.color       import cColors         as cc
from Game.core.system.logger import addLog
from Game.entities.player    import say


c, s = comments, status

def event(cmt) -> None:
    rewardP = randrange(1, 101)
    comment = ""

    if rewardP > 30:
        s.Dungeon[s.Dy][s.Dx]['room'][6][6] = {"block" : s.ids[4], "id" : 4}
        if cmt: comment = choice(c.treasureRoomComment[0])
    elif 10 <= rewardP < 30:
        for i in range(5, 8): s.Dungeon[s.Dy][s.Dx]['room'][i][i] = {"block" : s.ids[4], "id" : 4}
        if cmt: comment = choice(c.treasureRoomComment[1])
    else:
        for i in range(5, 8): s.Dungeon[s.Dy][s.Dx]['room'][i][i] = {"block" : s.ids[4], "id" : 4}
        s.Dungeon[s.Dy][s.Dx]['room'][5][7] = {"block" : s.ids[4], "id" : 4}
        s.Dungeon[s.Dy][s.Dx]['room'][7][5] = {"block" : s.ids[4], "id" : 4}
        if cmt: comment = choice(c.treasureRoomComment[2])
    if cmt:
        # addLog(f"{cc['fg']['L']}\"{comment}\"{cc['end']}")
        say(comment)
    s.Dungeon[s.Dy][s.Dx]['interaction'] = True