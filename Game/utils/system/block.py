from random import randrange
from copy   import deepcopy

from Game.core.system.structures import Conveyor
from Game.utils.graphics         import actualLen, escapeAnsi


isetCache:Conveyor = Conveyor(200)

def iset(block:str, space:str=' ', Type:str="n") -> str:
    """
    Type(str):
    ```
    n||r -> [block][space]
    l    -> [space][block]
    s    -> [?space][block][?space]
    ```
    """
    global isetCache

    key = (block,space,Type)
    if key in isetCache:
        return deepcopy(isetCache[key])
    
    if actualLen(escapeAnsi(block)) == 1:
        match Type:
            case "n"|"r": block = f"{block}{space}"
            case "l":     block = f"{space}{block}"
            case "s":
                n     = randrange(0,2)
                block = f"{space*(n&1)}{block}{space*(~n&1)}"
        
    else: return block

    if Type != 's': isetCache[key] = block

    return block