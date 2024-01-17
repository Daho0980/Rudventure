from Assets.data import status as s


quest = lambda: 1 if not s.entities and s.Dungeon[s.Dy][s.Dx]['roomType'] == 4 and s.Dungeon[s.Dy][s.Dx]['room'][6][6]["id"] in [300, 301] else 0
