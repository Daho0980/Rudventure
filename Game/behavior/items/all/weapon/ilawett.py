from ...all                import behaviorMap
from ...base               import ItemBehavior
from ...putItemStandard    import putItem
from ...weightCalcStandard import weightCalculate


class Ilawett(ItemBehavior):
    def collect(self) -> None:
        return super().collect()

    def use(self) -> None:
        return super().use()
    
    def attack(self) -> None:
        return super().attack()
    
    @putItem
    def put(self) -> None:
        return super().put()
    
    @weightCalculate
    def tread(self, itemId:str, itemType:str, payload:int) -> str:
        return super().tread(itemId, itemType, payload)
    
behaviorMap['weapon']["ilawett"] = Ilawett()