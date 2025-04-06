from functools import wraps
from random    import choice

from Assets.data.color import cColors       as cc
from .entities         import entity, player

from Assets.data import (
    totalGameStatus as s,
    comments        as c,
    lockers         as l
)


funcData = {}

# region Decorator
def _ephemera(func):
    def wrapper(*args):
        func(*args)
        func.__code__ = (_:=lambda*_:None).__code__
    
    return wrapper

def _blink(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('trigger', False) and func.__name__ in funcData:
            target = funcData.pop(func.__name__)

            func.__code__ = target['code']

            return

        elif func.__name__ not in funcData:
            func(*args, **kwargs)

            funcData[func.__name__] = {
                "code"   : func.__code__,
                "wrapper": wrapper
            }

            func.__code__ = (_:=lambda*a,**k:None).__code__
    
    return wrapper


# region Function
@_ephemera
def spawnCompanion(stdscr) -> None:
    if  not s.stage\
    and not s.isLoadfromBody\
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
    elif s.isLoadfromBody and not l.isSaveLoaded:
        l.isSaveLoaded = True
        entity.loadEntities()

@_ephemera
def startComment() -> None:
    player.say(
        choice(
            c.loadsaveStart\
                if  s.bodyPreservationMode
                and s.isLoadfromBody\
            else c.startWithCowardmode\
                if s.bodyPreservationMode\
            else c.start
        )
    )