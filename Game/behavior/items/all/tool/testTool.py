from ...all                import behaviorMap
from ...base               import ItemBehavior
from ...putItemStandard    import putItem
from ...weightCalcStandard import weightCalculate

from Game.core.system.io.logger import addLog


class TestTool(ItemBehavior):
    def collect(self) -> None:
        addLog("음정말멋진도구야 - Sent from TestTool.collect method")

    def use(self) -> None:
        return super().use()
    
    def attack(self) -> None:
        return super().attack()
    
    @putItem
    def put(self) -> None:
        return super().put()
    
    @weightCalculate
    def tread(self, itemId:str, itemType:str, payload:int) -> None:
        addLog("오이런정말멋진도구를밟아버렸어 - Sent from TestTool.tread method")

behaviorMap['tool']["testTool"] = TestTool()