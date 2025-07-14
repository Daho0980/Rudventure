import time
from   random import randrange

from .                       import event           as eev
from Assets.data             import totalGameStatus as s
from Assets.data.color       import cColors         as cc
from functions.grammar       import pstpos          as pp
from Game.entities.player    import event           as pev
from Game.entities.functions import getFace
from Game.tools              import block
from Game.utils.graphics     import escapeAnsi
from Game.utils.system.block import iset
from Game.utils.system.sound import play

from Game.entities.player import (
    event as pev
)
from Game.core.system.io.logger import (
    addLog
)
from Game.core.system.data.dataLoader import (
    obj
)


# region Base
class Enemy:
    def __init__(self, name:str, icon:str, ID:str, tag:str) -> None:
        self.tag  = tag
        self.name = name
        self.Dy   = 0
        self.Dx   = 0
        self.y    = 0
        self.x    = 0
        self.face = 'n'

        self.atk      = 0
        self.hp       = 0
        self.coolTime = 0
        self.stepped  = {}

        self.icon = icon
        self.id   = ID

        self.isFocused = True
        
        self.xpMultiplier = 1

    def start(self           ,
              setHp :int     ,
              setAtk:int     ,
              Dy    :int     ,
              Dx    :int     ,
              y     :list|int,
              x     :list|int,
              perm            ) -> None:
        self.hp  = setHp
        self.atk = setAtk

        self.perm = perm

        self.Dy, self.Dx = Dy, Dx
        DRP              = s.Dungeon[self.Dy][self.Dx]
        if isinstance(y, list) or isinstance(x, list):
            while 1:
                sY = randrange(1, s.roomData['maxHeight']-1)
                sX = randrange(1, s.roomData['maxWidth'] -1)

                if self.perm.data[block.take(sY, sX)['id']] & self.perm.STEP:
                    self.y = sY if isinstance(y, list) else y
                    self.x = sX if isinstance(x, list) else x
                    eev.spawn(self.y, self.x, self.icon, self.tag)

                    break

                else: continue

        else: self.y, self.x = y, x

        blockData = block.take(self.y, self.x)
        
        self.stepped = blockData\
                if  hasattr(self.perm, 'MAINTAIN')\
                and self.perm.data[blockData['id']]&self.perm.MAINTAIN\
            else blockData['blockData']\
                if blockData.get('blockData', False)\
            else obj('-bb', 'floor')

    def attack(self, Dir:list, DR:str="") -> None:
        if randrange(1,101) <= eval(s.statusFormula['evasion']):
            play  ("player", "evasion")
            addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!", colorKey='A')

        else:
            sound  = ("entity", "enemy", "enemyHit")
            s.DROD = (
                f"{cc['fg']['F']}{self.name if not DR else DR}{cc['end']}",
                'F'
            )

            if s.target['tag'] != self.tag:
                s.target['tag']        = self.tag
                s.target['attackable'] = False

            if s.df > 0:
                pev.defended()
                sound = ("player", "armor", "defended")
                self.knockback(Dir, randrange(1,3), s.atk)
                s.df -= 1

                if s.df == 0: dmg = int(self.atk/2)
                else:         dmg = int(self.atk/3)

                if s.df==0 and s.dfCrack<=0:
                    sound     = ("player", "armor", "armorCrack")
                    s.dfCrack = 1
                    play  ("player", "armor", "crack")
                    addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!", colorKey='B1')

            else:
                pev.hitted()
                dmg = self.atk

            s.hp -= dmg
            pev.bleeding(dmg)

            play(*sound)
            addLog(
                f"{s.lightName}{pp(s.name,'sub',True)} {cc['fg']['F']}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{self.atk}{cc['end']}만큼의 피해를 입었습니다!",
                colorKey='R'
            )

    def hitted(self) -> None:
        block.place(
            obj(
                '-be', 'invincibleEntity',
                block=iset(
                    f"{cc['fg']['R']}{escapeAnsi(self.icon)}{cc['end']}"
                ),
                tag=self.tag
            ),
            self.y, self.x,
            self.Dy, self.Dx
        )
        time.sleep(0.03)

        block.place(
            obj(
                '-be', self.id,
                block=iset(self.icon),
                tag  =self.tag
            ),
            self.y, self.x,
            self.Dy, self.Dx
        )

    def knockback(self, Dir:list, length:int, atk:int) -> None:
        for i in range(length):
            if not self.perm.data[block.take(
                self.y-Dir[0],
                self.x-Dir[1]
            )['id']] & self.perm.STEP:
                play("object", "wall", "hit")
                self.hitted()
                self.hp -= atk-i
                addLog(f"{cc['fg']['F']}{self.name}{cc['end']}{pp(self.name,'sub',True)} {cc['fg']['L']}{atk-i}{cc['end']}만큼의 피해를 입었습니다!", colorKey='R')

                return
            
            block.place(self.stepped, self.y, self.x, self.Dy, self.Dx)

            self.face = getFace(self.x-Dir[1], self.x, self.face)
            self.y   -= Dir[0]
            self.x   -= Dir[1]

            self.stepped = block.take(self.y, self.x)
            
            block.place(
                obj(
                    '-be', self.id,
                    block=iset(self.icon),
                    tag  =self.tag
                ),
                self.y, self.x,
                self.Dy, self.Dx
            )

            time.sleep(0.05)

    def isTargetted(self) -> None:
        if  s.target['tag'] == self.tag\
        and s.target['command']:
            for _ in range(2):
                block.place(
                    obj(
                        '-be', 'invincibleEntity',
                        block=iset(f"{cc['bg']['L']}{self.icon}{cc['end']}"),
                        tag  =self.tag
                    ),
                    self.y, self.x,
                    self.Dy, self.Dx
                ); time.sleep(0.07)

                block.place(
                    obj(
                        '-be', 'invincibleEntity',
                        block=iset(self.icon),
                        tag  =self.tag
                    ),
                    self.y, self.x,
                    self.Dy, self.Dx
                ); time.sleep(0.07)

            s.target['command'] = False

    def wait(self) -> None:
        self.coolTime -= 1

        if self.isFocused:
            self.isTargetted()
            if self.hp <= 0: self.coolTime = 0

            time.sleep(0.001)

        elif not self.isFocused:
            if[self.Dy, self.Dx] == [s.Dy, s.Dx]:
                self.isFocused = True
                self.coolTime  = 0

            time.sleep(0.5)

    def step(self, bfy:int, bfx:int, saveStepped:bool=True) -> None:
        blockData = block.take(self.y, self.x)

        self.face = getFace(self.x, bfx, self.face)
        s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx] = self.stepped

        if saveStepped:
            self.stepped = blockData\
                    if self.perm.data[blockData['id']]&self.perm.MAINTAIN\
                else blockData['blockData']\
                    if blockData.get('blockData', False)\
                else block.get('floor')
            
        block.place(
            obj(
                '-be', self.id,
                block=iset(self.icon),
                tag  =self.tag
            ),
            self.y, self.x,
            self.Dy, self.Dx
        )