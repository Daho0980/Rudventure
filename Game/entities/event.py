import time

from Assets.data.color       import cColors as cc
from Game.tools              import block
from Game.utils.graphics     import escapeAnsi
from Game.utils.system.block import iset
from Game.utils.system.sound import play

from Game.core.system.data.dataLoader import (
    obj
)

    
def spawn(y:int, x:int, icon:str) -> None:
    play("entity", "enemy", "charge")
    for i in ('.', 'x', 'X'):
        block.place(
            block.get('invincibleBlock',
                block=iset(f"{cc['fg']['A']}{i}{cc['end']}")
            ),
            y, x
        ); time.sleep(0.08)

        block.place(
            block.get('invincibleBlock',
                block=iset(f"{cc['fg']['W']}{i}{cc['end']}")
            ),
            y, x
        ); time.sleep(0.08)

    play("entity", "enemy", "shoot")
    block.place(
        block.get('invicnibleBlock',
            block=f"{cc['fg']['W']}{escapeAnsi(icon)}{cc['end']}"
        ),
        y, x
    ); time.sleep(0.05)
    
    block.place(obj('-be', 'invincibleEntity', block=icon), y, x)
