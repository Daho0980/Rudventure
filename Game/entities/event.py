import time

from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from Game.utils.graphics     import escapeAnsi
from Game.utils.system.block import iset
from Game.utils.system.sound import play

from Game.core.system.data.dataLoader import (
    obj
)


def hitted(y:int, x:int, icon:str, ID:str, tag:str) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    roomGrid[y][x] = obj(
        '-bb', 'invincibleBlock',
        block=iset(
            f"{cc['fg']['R']}{escapeAnsi(icon)}{cc['end']}"
        ),
        tag=tag
    )
    time.sleep(0.03)

    roomGrid[y][x] = obj(
        '-be', ID,
        block=iset(icon),
        tag  =tag
    )
    
def spawn(y:int, x:int, icon:str) -> None:
    roomGrid:dict = s.Dungeon[s.Dy][s.Dx]['room']

    play("entity", "enemy", "charge")
    for i in ['.', 'x', 'X']:
        roomGrid[y][x] = obj(
            '-bb', 'invincibleBlock',
            block=iset(f"{cc['fg']['A']}{i}{cc['end']}")
        ); time.sleep(0.08)

        roomGrid[y][x] = obj(
            '-bb', 'invincibleBlock',
            block=iset(f"{cc['fg']['W']}{i}{cc['end']}")
        ); time.sleep(0.08)

    play("entity", "enemy", "shoot")
    roomGrid[y][x] = obj(
        '-bb', 'invincibleBlock',
        block=f"{cc['fg']['W']}{escapeAnsi(icon)}{cc['end']}"
    ); time.sleep(0.05)
    
    roomGrid[y][x] = obj('-be', 'invincibleEntity', block=icon)
