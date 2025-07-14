from random import randrange

from Assets.data                      import totalGameStatus as s
from Game.core.system.data.dataLoader import obj


# region Func.local
def _setDyx(Dy, Dx) -> tuple[int ,int]:
    return (
        s.Dy if Dy == None else Dy,
        s.Dx if Dx == None else Dx
    )

def get(blockId:str, **extraData) -> dict:
    return obj(
        '-bb', blockId,
        **extraData
    )

def place(blockData:dict         ,
          y        :int          ,
          x        :int          ,
          Dy       :int|None=None,
          Dx       :int|None=None,
          stack    :bool    =False) -> None:
    Dy, Dx = _setDyx(Dy, Dx)

    if blockData.get('blockData') and stack:
        blockData['blockData'] = s.Dungeon[s.Dy][s.Dx]['room'][y][x]

    s.Dungeon[Dy][Dx]['room'][y][x] = blockData

def randPlace(blockData    :dict           ,
              y            :tuple[int, int],
              x            :tuple[int, int],
              allowedBlocks:list[str]       ) -> None:
    
    while 1:
        Ry, Rx = randrange(*y), randrange(*x)
        if s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx]["id"] not in allowedBlocks: continue
            
        break

    place(blockData, Ry, Rx)

def take(y :int          ,
         x :int          ,
         Dy:int|None=None,
         Dx:int|None=None) -> dict:
    Dy, Dx = _setDyx(Dy, Dx)

    return s.Dungeon[Dy][Dx]['room'][y][x]