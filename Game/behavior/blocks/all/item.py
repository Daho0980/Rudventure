from ..base import BlockBehavior

from Game.behavior.items.all import behaviorMap
from Game.tools.inventory    import collectFromBlock
from Game.tools              import block


class Item(BlockBehavior):
    def interact(self, **data):
        blockData = block.take(data['ty'], data['tx'])
        itemData  = blockData['nbt']['itemData']
        match collectFromBlock(
            itemData,
            behaviorMap[itemData['type']][itemData['id']],
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