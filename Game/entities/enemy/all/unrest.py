import time
from   random import randrange, choice

from ..base   import Enemy
from ..status import cooltimes

from Assets.data.color       import cColors as cc
from Game.tools              import block
from Game.utils.system.block import iset
from Game.utils.system.sound import play

from Assets.data import (
    totalGameStatus as s,
    flags           as f
)
from Game.core.system.data.dataLoader import (
    obj
)


class Unrest(Enemy):
    """
    # 불안의 편린
    - 돌격형 유닛
    - 언제나 플레이어의 위치를 알고 쫓아옴
    - 체력은 10+(2*stage)
    - x값 또는 y값이 플레이어와 같다면 플레이어가 있는 방향으로 돌진함
    - 기본적인 아이콘 -> #
    """
    def __init__(self, name, icon, ID, tag):
        super().__init__(name, icon, ID, tag)
        self.coolTimes = cooltimes.Unrest()

        if s.sanjibaMode:
            self.coolTimes.divideHalf(self.coolTimes.modeException)

    def start(self      ,
              setHp :int,
              setAtk:int,
              Dy    :int,
              Dx    :int,
              y     :int,
              x     :int,
              perm       ) -> None:
        super().start(setHp, setAtk, Dy, Dx, y, x, perm)

    def Targetted(self) -> None:
        play("entity", "enemy", "unrest", "targetLock")
        for _ in range(3):
            block.place(
                obj(
                    '-be', 'invincibleEntity',
                    block=iset(f"{cc['fg']['F']}{self.icon}{cc['end']}"),
                    tag  =self.tag
                ),
                self.y, self.x,
                self.Dy, self.Dx
            ); time.sleep(self.coolTimes.targetted)

            block.place(
                obj(
                    '-be', 'invincibleEntity',
                    block=iset(self.icon),
                    tag  =self.tag
                ),
                self.y, self.x,
                self.Dy, self.Dx
            ); time.sleep(self.coolTimes.targetted)

    def move(self) -> None:
        if not self.coolTime:
            self.coolTime = randrange(*self.coolTimes.turnEnd)
            if self.isFocused:
                if (self.Dy, self.Dx) != (s.Dy, s.Dx):
                    self.isFocused = False

                    return

                bfx, bfy = self.x, self.y
                if self.hp > 0:
                    Moves, Moves1 = ("+=", "-="), ("+", "-")

                    if (self.Dy, self.Dx)==(s.Dy, s.Dx) and (self.y==s.y or self.x==s.x):
                        self.stepped = block.get('floor')

                        if self.x == s.x:
                            a = 0 if self.y<s.y else 1
                            self.Targetted()

                            while 1:
                                if not f.pause:
                                    if block.take(eval(f"self.y{Moves1[a]}1"), self.x)['id'] in ('player1', 'player2'):
                                        self.attack(
                                            [eval(f"0{Moves1[a]}1"), 0],
                                            choice(["충격파", "추돌", "들이박힘"])
                                        ); break
                                    
                                    if not self.perm.data[
                                        block.take(eval(f"self.y{Moves1[a]}1"), self.x)['id']
                                    ] & self.perm.BREAK:
                                        break

                                    bfy, bfx = self.y, self.x
                                    exec(f"self.y{Moves[a]}1")

                                    super().step(bfy, bfx, saveStepped=False)

                                time.sleep(self.coolTimes.rush)
                            
                            play("entity", "enemy", "unrest", "crash")

                        elif self.y == s.y:
                            a = 0 if self.x<s.x else 1
                            self.Targetted()

                            while 1:
                                if not f.pause:
                                    if block.take(self.y, eval(f"self.x{Moves1[a]}1"))['id'] in ('player1', 'player2'):
                                        self.attack(
                                            [0, eval(f"0{Moves1[a]}1")],
                                            choice(["충격파", "추돌", "들이박힘"])
                                            ); break
                                    
                                    if not self.perm.data[
                                        block.take(self.y, eval(f"self.x{Moves1[a]}1"))['id']
                                    ] & self.perm.BREAK:
                                        break

                                    bfy, bfx = self.y, self.x
                                    exec(f"self.x{Moves[a]}1")

                                    super().step(bfy, bfx, saveStepped=False)

                                time.sleep(self.coolTimes.rush)
                            
                            play("entity", "enemy", "unrest", "crash")

                    else:
                        if randrange(0,2):
                            self.x += 1\
                                    if  self.x<s.x\
                                    and self.perm.data[block.take(self.y, self.x+1)['id']] & self.perm.STEP\
                                else -1\
                                    if  self.x>s.x\
                                    and self.perm.data[block.take(self.y, self.x-1)['id']] & self.perm.STEP\
                                else 0
                            
                        else:
                            self.y += 1\
                                    if  self.y<s.y\
                                    and self.perm.data[block.take(self.y+1, self.x)['id']] & self.perm.STEP\
                                else -1\
                                    if  self.y>s.y\
                                    and self.perm.data[block.take(self.y-1, self.x)['id']] & self.perm.STEP\
                                else 0

                        super().step(bfy, bfx)

            block.place(
                obj(
                    '-be', self.id,
                    block=iset(self.icon),
                    tag  =self.tag
                ),
                self.y, self.x,
                self.Dy, self.Dx
            )

        else: super().wait()