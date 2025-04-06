from Assets.data import totalGameStatus as s


quest = lambda: 1\
        if  not s.enemyCount\
        and s.Dungeon[s.Dy][s.Dx]['roomType']=="endPoint"\
        and s.Dungeon[s.Dy][s.Dx]['room'][11][11]['id']in('player1', 'player2')\
	else 0
