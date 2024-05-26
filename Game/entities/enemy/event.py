import time

from Assets.data             import status    as s
from Assets.data.color       import cColors   as cc
from Game.utils.graphic      import escapeAnsi
from Game.utils.system.sound import play


def hitted(y:int, x:int, icon:str, ID:int) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    roomGrid[y][x] = {'block':f"{cc['fg']['R']}{escapeAnsi(icon)}{cc['end']}", 'id':-1}; time.sleep(0.03)
    roomGrid[y][x] = {'block':icon, 'id':ID}

def spawn(y:int, x:int, icon:str) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    play("enemy", "charge")
    for i in ['.', 'x', 'X']:
        roomGrid[y][x] = {'block':f"{cc['fg']['R']}{i}{cc['end']}", 'id':-1}; time.sleep(0.08)
        roomGrid[y][x] = {'block':f"{cc['fg']['W']}{i}{cc['end']}", 'id':-1}; time.sleep(0.08)

    play("enemy", "shoot")
    roomGrid[y][x] = {'block':f"{cc['fg']['W']}{escapeAnsi(icon)}{cc['end']}", 'id':-1}; time.sleep(0.05)
    roomGrid[y][x] = {'block':icon, 'id':-1}
