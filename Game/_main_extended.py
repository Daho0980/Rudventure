from random import choice

from .entities              import entity
from .entities.player.event import say
from Assets.data.color      import cColors as cc

from Assets.data import (
    totalGameStatus as s,
    comments        as c,
    flags           as f
)


funcData = {}

# region Decorator
def _ephemera(func):
    def wrapper(*args):
        func(*args)
        func.__code__ = (_:=lambda*_:None).__code__
    
    return wrapper


# region Function
@_ephemera
def spawnCompanion() -> None:
    if  not s.stage\
    and not f.isLoadfromBody\
    and s.name.lower() in ["업로드", "upload"]:
        entity.addAnimal(
            'cat', 10, 1, 3, 6,

            name     ="구름이",
            color    =[cc['fg']['W'],'W'],
            friendly =True,
            MCBF     =True,
            SICR     =True,
            extraData={ "loyalty":10 }
        )
    elif f.isLoadfromBody and not f.loadLock:
        f.loadLock = 0b1
        entity.loadEntities()

@_ephemera
def startComment() -> None:
    say(
        choice(
            c.loadsaveStart\
                if  s.bodyPreservationMode
                and f.isLoadfromBody\
            else c.startWithCowardmode\
                if s.cowardMode\
            else c.start
        )
    )