import time

from Assets.data                 import totalGameStatus as s
from Assets.data.color           import cColors         as cc
from Game.core.system.dataLoader import obj
from Game.utils.graphics         import escapeAnsi
from Game.utils.system.sound     import play


def hitted(y:int, x:int, icon:str, ID:int, hashKey:str) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    roomGrid[y][x] = {'block':f"{cc['fg']['R']}{escapeAnsi(icon)}{cc['end']}", 'id':-1, "type" : 1, "hashKey" : hashKey}
    time.sleep(0.03)
    roomGrid[y][x] = {'block':icon, 'id':ID, "type" : 1, "hashKey" : hashKey}

def spawn(y:int, x:int, icon:str) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    play("entity", "enemy", "charge")
    for i in ['. ', 'x ', 'X ']:
        roomGrid[y][x] = obj('-bb', '-1', block=f"{cc['fg']['R']}{i}{cc['end']}"); time.sleep(0.08)
        roomGrid[y][x] = obj('-bb', '-1', block=f"{cc['fg']['W']}{i}{cc['end']}"); time.sleep(0.08)

    play("entity", "enemy", "shoot")
    roomGrid[y][x] = obj('-bb', '-1', block=f"{cc['fg']['W']}{escapeAnsi(icon)}{cc['end']}"); time.sleep(0.05)
    roomGrid[y][x] = obj('-bb', '-1', block=icon)
