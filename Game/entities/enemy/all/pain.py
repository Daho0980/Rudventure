import time
from   random import randrange, choice

from ..base   import Enemy
from ..status import cooltimes

from Assets.data                import totalGameStatus as s
from Assets.data.color          import cColors         as cc
from functions.grammar          import pstpos as pp
from Game.core.system.io.logger import addLog
from Game.entities.player       import statusEffect as se
from Game.entities.algorithms   import AStar
from Game.tools                 import block
from Game.utils.system.sound    import play

from Game.core.system.data.dataLoader import (
    obj
)


class Pain(Enemy):
    """
    # 고통의 편린
    - 일개 잡몹
    - 플레이어를 추격함
    - 체력은 4+(2*stage)
    - 플레이어가 상/하/좌/우 1 칸 이내에 있다면 공격함
    - 확률적으로 포효를 내질러 자신의 공격력이 1+(round(stage/10)) 증가함
    - 기본적인 아이콘 -> %
    """
    def __init__(self, name, icon, ID, tag):
        super().__init__(name, icon, ID, tag)
        self.coolTimes = cooltimes.Pain()

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

    def move(self) -> None:
        DRP  = s.Dungeon[self.Dy][self.Dx]

        if not self.coolTime:
            self.coolTime = randrange(*self.coolTimes.turnEnd)
            if self.isFocused:
                if (self.Dy,self.Dx) != (s.Dy,s.Dx): self.isFocused = False; return
                
                bfx, bfy = self.x, self.y
                if self.hp > 0:
                    if randrange(1,1216) == 1215:
                        self.atk += 1+(round(s.stage/10))
                        play("entity", "enemy", "pain", "growl")
                        se.addEffect('kitrima', 45)
                        addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon}){pp(self.name,'sub',True)} 울부짖습니다!", colorKey='F')
                        addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon})의 공격력이 {cc['fg']['L']}{1+(round(s.stage/10))}{cc['end']}만큼 상승합니다.", colorKey='F')

                        for _ in range(3):
                            block.place(
                                obj(
                                    '-be', 'invincibleEntity',
                                    block=f"{cc['fg']['F']}{self.icon}{cc['end']}",
                                    tag  =self.tag
                                ),
                                self.y, self.x,
                                self.Dy, self.Dx
                            ); time.sleep(0.1)

                            block.place(
                                obj(
                                    '-be', 'invincibleEntity',
                                    block=self.icon,
                                    tag  =self.tag
                                ),
                                self.y, self.x,
                                self.Dy, self.Dx
                            ); time.sleep(0.1)

                        block.place(
                            obj('-be', self.id, block=self.icon, tag=self.tag),
                            self.y, self.x,
                            self.Dy, self.Dx
                        )

                    path = AStar.main(
                        (self.y, self.x),
                        ['player1', 'player2'],
                        self.perm.IDSet['step']
                    )

                    if not path:
                        ay, ax = -1, -1
                        if sum([ay,ax])==-2 or (self.y,self.x)==(ay,ax):
                            while 1:
                                if not self.perm.data[DRP['room']\
                                [ay:=randrange(1, s.roomData['maxHeight']-1)]\
                                [ax:=randrange(1, s.roomData['maxWidth'] -1)]\
                                ['id']] & self.perm.STEP: continue

                                break

                        if randrange(0,2):
                            self.x += 1\
                                    if  self.x<ax\
                                    and self.perm.data[block.take(self.y, self.x+1)['id']]&self.perm.STEP\
                                else -1\
                                    if  self.x>ax\
                                    and self.perm.data[block.take(self.y, self.x)['id']]&self.perm.STEP\
                                else 0
                            
                        else:
                            self.y += 1\
                                   if  self.y<ay\
                                   and self.perm.data[block.take(self.y+1, self.x)['id']]&self.perm.STEP\
                                else -1\
                                   if  self.y>ay\
                                   and self.perm.data[block.take(self.y-1, self.x)['id']]&self.perm.STEP\
                                else 0
                            
                    elif block.take(*path)['id'] in ('player1', 'player2'):
                        block.place(
                            obj(
                                '-be', 'invincibleEntity',
                                block=f"{cc['fg']['F']}{self.icon}{cc['end']}",
                                tag  =self.tag
                            ),
                            self.y, self.x,
                            self.Dy, self.Dx
                        ); time.sleep(0.1)

                        block.place(
                            obj(
                                '-be', self.id,
                                block=self.icon,
                                tag  =self.tag
                            ),
                            self.y, self.x,
                            self.Dy, self.Dx
                        )

                        self.attack(
                            [path[0]-self.y, path[1]-self.x],
                            choice(["물어뜯김", "과다출혈", "쇼크"])
                        )

                    else: self.y, self.x = path

                    super().step(bfy, bfx)

        else: self.wait()
