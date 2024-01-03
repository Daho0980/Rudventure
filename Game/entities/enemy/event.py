import time
from   Assets.data        import status     as s
from   Game.utils.graphic import escapeAnsi

cc = s.cColors

def hitted(y:int, x:int, icon:str, ID:int) -> None:

    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = {'block':f"{cc['fg']['R']}{escapeAnsi(icon)}{cc['end']}", 'id':-1}
    time.sleep(0.1)
    s.Dungeon[s.Dy][s.Dx]['room'][y][x] = {'block':icon, 'id':ID}