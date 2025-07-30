from ...all                import behaviorMap
from ...base               import ItemBehavior
from ...weightCalcStandard import weightCalculate

from Game.entities.player.event import sayCmt
from Game.core.system.io.logger import addLog
from Game.tools                 import inventory, item

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


class Animus(ItemBehavior):
    def collect(self) -> None:
        if s.playerIdentity == 'upload':
            target = c.specialComment['animus']['get']
            sayCmt(target['cmt'], target['prob'])

    def use(self) -> None:
        if (targetIndex:=inventory.search('anima')) == -1:
            if s.playerIdentity == 'upload':
                target = c.specialComment['animus']['merge']['failure']
                sayCmt(target['cmt'], target['prob'])
            
            else: addLog("아무런 반응도 없습니다...")

        else:
            inventory.pop(targetIndex, True)
            item.registration('weapon', "animusAnima")
            inventory.place(item.get(
                'weapon', 'animusAnima',
                nbt = { "link" : inventory.pop()['nbt']['link'] } # type: ignore
            ))
            if s.playerIdentity == 'upload':
                target = c.specialComment['animus']['merge']['success']
                sayCmt(target['cmt'], target['prob'])

            else: addLog("아니무스가 융합되었습니다!")
    
    def attack(self) -> None:
        return super().attack()
    
    def put(self) -> None:
        if s.playerIdentity == 'upload':
            target = c.specialComment['animus']['put']
            sayCmt(target['cmt'], target['prob'])

        else: addLog("이 아이템은 버려질 수 없습니다.")
    
    @weightCalculate
    def tread(self, itemId:str, itemType:str, payload:int) -> None:
        if s.playerIdentity == 'upload':
            target = c.specialComment['animus']['tread']
            sayCmt(target['cmt'], target['prob'])

behaviorMap['weapon']["animus"] = Animus()