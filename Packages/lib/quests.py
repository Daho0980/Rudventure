from Packages.lib.data import status as s

quest = lambda: 1 if s.roomLock == False and s.Dungeon[s.Dy][s.Dx]['roomType'] == 4 and s.Dungeon[s.Dy][s.Dx]['room'][6][6] in [s.p1, s.p2] else 0
