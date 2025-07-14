import time
from   random import choice

from ..base   import Enemy
from ..status import cooltimes

from Assets.data.color       import cColors   as cc
from Game.entities.player    import event     as pev
from Game.tools              import block
from Game.utils.graphics     import escapeAnsi
from Game.utils.system.block import iset
from Game.utils.system.sound import play

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)
from Game.core.system.data.dataLoader import (
    obj
)


class Resentment(Enemy):
    """
    # 원망의 편린
    - 지뢰
    - 기본적으로 움직이지 않고 enemyCount에 합산되지 않음
    - 체력은 5+(2*stage)
    - 감지 범위는 상/하/좌/우 모두 1임. 대각선으로는 탐지 불가능
    - 기본적인 아이콘 -> ※
    """
    def __init__(self, name, icon, ID, tag):
        super().__init__(name, icon, ID, tag)
        self.coolTimes = cooltimes.Resentment()

        if s.sanjibaMode: self.coolTimes.divideHalf(self.coolTimes.modeException)

    def start(self      ,
              setHp :int,
              setAtk:int,
              Dy    :int,
              Dx    :int,
              y     :int,
              x     :int,
              perm       ) -> None:
        super().start(setHp, setAtk, Dy, Dx, y, x, perm)

    def blink(self) -> None:
        block.place(
            obj(
                '-be', 'invincibleEntity',
                block=iset(f"{cc['fg']['F']}{self.icon}{cc['end']}"),
                tag  =self.tag
            ),
            self.y, self.x,
            self.Dy, self.Dx
        ); time.sleep(self.coolTimes.blink)

        block.place(
            obj(
                '-be', self.id,
                block=iset(self.icon),
                tag  =self.tag
            ),
            self.y, self.x,
            self.Dy, self.Dx
        )

    def targetted(self) -> None:
        for _ in range(3): self.blink()

    def explosion(self) -> None:
        expPs = (
            (self.y-1,self.x  ),
            (self.y+1,self.x  ),
            (self.y  ,self.x-1),
            (self.y  ,self.x+1)
        )

        block.place(
            obj(
                '-be', 'invincibleEntity',
                block=f"{cc['fg']['F']}X {cc['end']}"
            ),
            self.y, self.x,
            self.Dy, self.Dx
        )
        particle = f"{cc['fg']['F']}. {cc['end']}"
        for expP in expPs:
            blockData = block.take(*expP)
            if self.perm.data[blockData['id']] & self.perm.EXPLOSION:
                block.place(
                    block.get('invincibleBlock', block=particle),
                    *expP,
                    self.Dy, self.Dx
                )
               
            elif blockData['id'] in ('player1', 'player2'):
                s.steppedBlock = block.get(
                    'ashChip',
                    block=f"{cc['fg']['G1']}{escapeAnsi(blockData['block'])}{cc['end']}"
                )

        time.sleep(self.coolTimes.explosion)
            
        for expP in expPs:
            if block.take(*expP) == block.get('invincibleBlock', block=particle):
                block.place(block.get(
                        'ashChip',
                        block=f"{cc['fg']['G1']}. {cc['end']}"
                    ),
                    *expP,
                    self.Dy, self.Dx
                )
            
        self.icon = iset(choice(['×', 'x', 'X']))
        self.hp   = 0

    def getSurroundingID(self) -> tuple:
        return (
            block.take(self.y-1, self.x)['id'],
            block.take(self.y, self.x+1)['id'],
            block.take(self.y+1, self.x)['id'],
            block.take(self.y, self.x-1)['id']
        )

    def move(self) -> None:            
        if not self.coolTime:
            self.coolTime = self.coolTimes.turnEnd
            if self.isFocused:
                if [self.Dy, self.Dx] != [s.Dy, s.Dx]: self.isFocused = False; return

                if self.hp > 0:
                    if 'player1' in (data:=self.getSurroundingID())\
                    or 'player2' in data:
                        self.targetted()

                        if 'player1' in (data:=self.getSurroundingID())\
                        or 'player2' in data:
                            play("entity", "enemy", "resentment", "explosion")
                            self.attack([0, 0], "폭발")
                            
                            self.explosion()
                            self.xpMultiplier = 2
                            target = c.entity['enemy']['resentment']['explosion']
                            pev.sayCmt(target['cmt'], target['prob'])

                        else:
                            block.place(
                                obj(
                                    '-be', self.id,
                                    block=iset(self.icon),
                                    tag  =self.tag
                                ),
                                self.y, self.x,
                                self.Dy, self.Dx
                            )

                    else: self.blink()

        else: super().wait()