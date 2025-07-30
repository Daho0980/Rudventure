from ..base import BlockBehavior

from Game.behavior.items.all import behaviorMap
from Game.tools              import block
from Game.tools.item         import registration
from Game.tools.inventory    import collectFromBlock


class Item(BlockBehavior):
    def interact(self, **data):
        blockData = block.take(data['ty'], data['tx'])
        itemData  = blockData['nbt']['itemData']
        itemId    = itemData['id']
        itemType  = itemData['type']

        registration(itemType, itemId)

        match collectFromBlock(
            itemData,
            behaviorMap[itemType][itemId],
            blockData['blockData'],
            data['ty'], data['tx']
        ):
            case 'destroyed':
                data['sound'] = ("object", "item", "destroy")
                block.place(blockData['blockData'], data['ty'], data['tx'])

            case 'success':
                data['sound'] = ("player", "getItem")

            case 'treadOn': pass

        return data['ty'], data['tx'], data['sound']