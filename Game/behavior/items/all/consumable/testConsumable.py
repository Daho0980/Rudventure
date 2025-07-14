from ...base               import ItemBehavior
from ...putItemStandard    import putItem
from ...weightCalcStandard import weightCalculate

from Game.core.system.io.logger import addLog


class TestConsumable(ItemBehavior):
    def collect(self) -> None:
        addLog("음정말멋진소모품이야 - Sent from TestConsumable.collect method")

    def use(self) -> None:
        return super().use()
    
    def attack(self) -> None:
        return super().attack()
    
    @putItem
    def put(self) -> None:
        return super().put()
    
    @weightCalculate
    def tread(self, itemId:str, itemType:str, payload:int) -> None:
        addLog("오이런정말멋진소모품을밟아버렸어 - Sent from TestConsumable.tread method")