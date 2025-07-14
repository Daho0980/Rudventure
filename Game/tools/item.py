from Game.core.system.data.dataLoader import obj
from Game.utils.system.block          import iset


def get(itemType:str, itemId:str, **extraData) -> dict:
    return obj(
        f'-i{'t'
                if itemType=='tool'
            else 'w'
                if itemType=='weapon'
            else 'c'
        }',

        itemId,
        **extraData
    )

def package(itemData:dict, face:str='n') -> dict:
    output = obj(
        "-bb", 'item',
        block=iset(itemData['icon'], Type=face),
        nbt  ={ "itemData" : itemData }
    )

    return output