from ...all  import behaviorMap
from ...base import ItemBehavior


class AnimusAnima(ItemBehavior):
    def collect(self) -> None:
        return super().collect()
    
    def use(self) -> None:
        return super().use()
    
    def attack(self) -> None:
        return super().attack()
    
    def put(self) -> None:
        return super().put()
    
    def tread(self, itemId: str, itemType: str, payload: int) -> str:
        return super().tread(itemId, itemType, payload)
    
behaviorMap['weapon']["animusAnima"] = AnimusAnima()