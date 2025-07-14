from .entities              import entity
from .entities.player.event import sayCmt
from Assets.data.color      import cColors    as cc
from Game.tools             import item, block

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
    and s.playerIdentity == 'upload':
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
    target = c.loadsaveStart\
        if  s.bodyPreservationMode\
        and f.isLoadfromBody\
    else c.startWithCowardmode\
        if s.cowardMode\
    else c.start
    sayCmt(target['cmt'], target['prob'])

def placeExclusiveItem() -> None:
    match s.playerIdentity:
        case "repo":
            block.randPlace(
                item.package(item.get(
                    'tool', 'ásotus',
                    nbt = {
                        'link' : True,
                        'orbSlot' : []
                    }
                )),
                (1, s.roomData['maxHeight']-2),
                (1,  s.roomData['maxWidth']-2),
                    
                ['floor']
            )

        case "upload":
            block.randPlace(
                item.package(item.get(
                    'weapon', 'animus',
                    nbt = { 'link' : True }
                )),
                (1, s.roomData['maxHeight']-2),
                (1,  s.roomData['maxWidth']-2),
                    
                ['floor']
            )
            block.randPlace(
                item.package(item.get(
                    'weapon', 'anima',
                    nbt = { 'link' : True }
                )),
                (1, s.roomData['maxHeight']-2),
                (1,  s.roomData['maxWidth']-2),
                    
                ['floor']
            )