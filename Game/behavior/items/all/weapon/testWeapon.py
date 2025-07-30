from ...all                import behaviorMap
from ...base               import ItemBehavior
from ...putItemStandard    import putItem
from ...weightCalcStandard import weightCalculate

from Game.core.system.io.logger import addLog


class TestWeapon(ItemBehavior):
    def collect(self) -> None:
        addLog("음정말멋진무기야 - Sent from TestWeapon.collect method")

    def use(self) -> None:
        return super().use()
    
    def attack(self) -> None:
        return super().attack()
    
    @putItem
    def put(self) -> None:
        return super().put()
    
    @weightCalculate
    def tread(self, itemId:str, itemType:str, payload:int) -> None:
        addLog("오이런정말멋진무기를밟아버렸어 - Sended from TestWeapon.tread method")

behaviorMap['weapon']["testWeapon"] = TestWeapon()