from random import choice

from Assets.data                import totalGameStatus   as s
from Assets.data.color          import cColors           as cc
from Game.entities.player.event import bleeding, readSign
from Game.tools.block           import place, get
from Game.utils.system.block    import iset
from Game.utils.system.sound    import play


def giveLoot(ty:int, tx:int, face:str) -> None:
    play("object", "squishy", "open")
    kind = choice(("aorta", "venaCava"))
    place(
        get(
            kind,
            block=iset(s.bids[kind], Type=face)
        ),
        ty, tx,
        stack=False
    )

def explosion(ty:int, tx:int, face:str) -> None:
    play("object", "squishy", "explosion")
    
    s.hp -= 5; bleeding(5)

    s.DROD = (f"{cc['fg']['B1']}말랑이{cc['end']}", 'B1')

    place(
        get('floor',
            block=iset(
                f'{cc['fg']['B1']}x{cc['end']}',
                Type=face
            )
        ),
        ty, tx
    )

    readSign(
        [f"{cc['fg']['B1']}'하하하, 터어어어얼렸구나!!'{cc['end']}"],
        0.07,
        "clayModel"
    )