from importlib import import_module

from Assets.data                      import totalGameStatus as s
from Game.core.system.data.dataLoader import obj
from Game.utils.system.block          import iset


def get(itemType:str, itemId:str, **extraData) -> dict:
    return obj(
        f'-i{itemType[0]}',

        itemId,
        **extraData
    )

def registration(itemType:str, itemId:str) -> None:
    import_module(f"Game.behavior.items.all.{itemType}.{itemId}")

def retain(itemId:str) -> None:
    if itemId not in s.memory['item']:
        s.memory['item'].add(itemId)

def remember(itemId:str) -> bool:
    return itemId in s.memory['item']

def package(itemData:dict, face:str='n') -> dict:
    output = obj(
        "-bb", 'item',
        block=iset(itemData['icon'], Type=face),
        nbt  ={ "itemData" : itemData }
    )

    return output