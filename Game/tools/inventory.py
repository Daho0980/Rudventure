from copy import deepcopy

from Assets.data                import totalGameStatus as s
from Assets.data.color          import cColors         as cc
from Game.behavior.items.base   import ItemBehavior
from Game.core.system.io.logger import addLog
from Game.tools.item            import package
from Game.tools.block           import place  as placeBlock

from functions.grammar import (
    pstpos as pp
)


# region Func.local
def _setSlotIndex(slt) -> int:
    return (s.inventory['pointer']
        if slt<=-1 or slt>=len(s.inventory['cells'])
    else slt)

def _collectAction(itemData:dict, slot:int, behavior:ItemBehavior) -> None:
    s.inventory['cells'][slot]['item'] = itemData
    addLog(f"{cc['fg']['Y']}'{itemData['name']}'{cc['end']}{pp(itemData['name'], 'obj', True)} 얻었습니다.", colorKey='Y')
    behavior.collect()

# region Func.global
def collect(itemData:dict        ,
            behavior:ItemBehavior,
            slot    :int =-1     ,
            force   :bool=False   ) -> None:
    slot = _setSlotIndex(slot)

    if (s.inventory['cells'][slot]['item']     and not force)\
    or (s.inventory['cells'][slot]['disabled'] and not force):
        return

    _collectAction(itemData, slot, behavior)

def collectFromBlock(itemData :dict        ,
                     behavior :ItemBehavior,
                     blockData:dict        ,
                     ty       :int         ,
                     tx       :int          ) -> str:
    slot = s.inventory['pointer']

    if s.inventory['cells'][slot]['item']:
        return behavior.tread(
            itemData['id'],
            itemData['type'],
            itemData['status']['payload']
        )
    
    _collectAction(itemData, slot, behavior)
    placeBlock(blockData, ty, tx)

    return "success"

def get(slot:int=-1) -> dict:
    slot = _setSlotIndex(slot)

    return s.inventory['cells'][slot]['item']

def place(itemData:dict, slot:int=-1) -> None:
    slot = _setSlotIndex(slot)

    s.inventory['cells'][slot]['item'] = itemData

def stack(itemData:dict, limit:int=-1, force:bool=False) -> bool:
    if limit<=-1 or limit>len(s.inventory['cells']):
        limit = len(s.inventory['cells'])

    if all(
        cell['item'] or cell['disabled']
        for cell in s.inventory['cells']
    ):
        return False
    
    for i, cell in enumerate(s.inventory['cells']):
        if i == limit: return False
        
        if (
            not ( cell['item'] or cell['disabled'] )
        ) or (
            ( cell['item'] or cell['disabled'] ) and force
        ):
            cell['item'] = itemData

            return True
            
    
    return False

def search(itemId:str) -> int:
    for i, target in enumerate(map(
        lambda i: i['item'],
        s.inventory['cells']
    )):
        if target and target['id']==itemId: return i

    else: return -1

def lock(slot:int=-1) -> bool:
    slot = _setSlotIndex(slot)

    if s.inventory['cells'][slot]['disabled']:
        return False
    
    s.inventory['cells'][slot]['disabled'] = True

    return True

def unlock(slot:int=-1) -> bool:
    slot = _setSlotIndex(slot)

    if not s.inventory['cells'][slot]['disabled']:
        return False
    
    s.inventory['cells'][slot]['disabled'] = False

    return True

def pop(slot :int =-1  ,
        force:bool=False) -> dict|None:
    slot = _setSlotIndex(slot)

    if not s.inventory['cells'][slot]['item']:
        return None
    
    if  s.inventory['cells'][slot]['disabled']\
    and not force:
        return None
    
    itemData = deepcopy(s.inventory['cells'][slot]['item'])
    s.inventory['cells'][slot]['item'] = {}

    return itemData

def extend(count:int) -> None:
    if count<=0\
    or (len(s.inventory['cells'])+count)>s.inventory['max']:
        return
    
    for _ in range(count):
        s.inventory['cells'].append({ "item":{}, "disabled":False })

def durabilityDecrease(slot:int=-1) -> None:
    slot = _setSlotIndex(slot)
    if not get(slot): return

    durability = s.inventory['cells'][slot]['item']['status']['durability']

    if durability[0] == '∞': return

    durability[0] -= 1

    if durability[0] == 0:
        itemName = pop(slot, True)['name'] # type: ignore
        addLog(f"{cc['fg']['Y']}'{itemName}'{pp(itemName,'sub',True)} 파괴되었습니다!")

# region Decorator
def put(slot:int=-1) -> str:
    slot     = _setSlotIndex(slot)
    itemData = get(slot)

    if not itemData: return "itemPopFailure"

    for y in range(s.y-1, s.y+2):
        for x in range(s.x-1, s.x+2):
            if s.Dungeon[s.Dy][s.Dx]['room'][y][x]['id']\
            in s.itemPlaceableBlock:
                pop(slot)
                placeBlock(package(itemData), y, x)

                return "success"
                
    return "allowedBlockNotFound"