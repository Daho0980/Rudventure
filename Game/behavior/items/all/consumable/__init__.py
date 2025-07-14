from ...base import ItemBehavior

from .testConsumable import TestConsumable


behaviorMap:dict[str, ItemBehavior] = {
    "testConsumable" : TestConsumable()
}