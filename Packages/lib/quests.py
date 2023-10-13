from Packages.lib.data import status

s = status


def quest():
    output = 0
    if s.roomLock == False and s.Dungeon[s.Dy][s.Dx]['roomType'] == 4 and s.Dungeon[s.Dy][s.Dx]['room'][6][6] in [s.p1, s.p2]: output = 1
    return output
