from ...base               import ItemBehavior
from ...weightCalcStandard import weightCalculate

from Game.entities.player.event import sayCmt
from Game.entities.player       import statusEffect
from Game.tools                 import inventory, item

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


class Ásotus(ItemBehavior):
    def collect(self) -> None:
        if s.playerIdentity == 'repo':
            target = c.specialComment['ásotus']['get']
            sayCmt(target['cmt'], target['prob'])

        inventory.pop()

        for i in range(3):
            inventory.lock(i)
        
        inventory.extend(3)
        inventory.stack(
            item.get(
                'tool', 'ásotus',
                nbt={ "link" : True }
            )
        )

        s.inventory['pointer'] = inventory.search('ásotus')

    def use(self) -> None:
        if not statusEffect.search('combinator', 'global'): return
        
        if s.playerIdentity == 'repo':
            target = c.specialComment['ásotus']['use']
            sayCmt(target['cmt'], target['prob'])
    
    def attack(self) -> None:
        if s.playerIdentity == 'repo':
            target = c.specialComment['ásotus']['attack']
            sayCmt(target['cmt'], target['prob'])
    
    def put(self) -> None:
        if s.playerIdentity == 'repo':
            target = c.specialComment['ásotus']['put']
            sayCmt(target['cmt'], target['prob'])
    
    @weightCalculate
    def tread(self, itemId:str, itemType:str, payload:int) -> None:
        if s.playerIdentity == 'repo':
            target = c.specialComment['ásotus']['tread']
            sayCmt(target['cmt'], target['prob'])