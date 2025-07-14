import time
from   random import randrange

from Assets.data.color       import cColors as cc
from functions.grammar       import pstpos  as pp
from Game.entities.functions import getFace
from Game.entities           import event
from Game.entities.player    import event as pEvent
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
from Game.core.system.io.logger import (
    addLog
)


negativeVars = ("perm")

class Animal:
    def __init__(self              ,
                 tribe         :str,
                 name          :str,
                 icon          :str,
                 ID            :str,
                 color         :str,
                 colorKey      :str,
                 tag           :str,
                 initFuncParams:list) -> None:
        self.tribe = tribe
        self.tag   = tag

        self.Dy = 0
        self.Dx = 0
        self.y  = 0
        self.x  = 0

        self.atk      = 0
        self.hp       = 0
        self.coolTime = 0
        self.stepped  = {}

        self.Mhp = 0

        self.name     = name
        self.icon     = icon
        self.id       = ID
        self.color    = color
        self.colorKey = colorKey

        self.isFocused = True

        self.initFuncParams = initFuncParams

    def start(self           ,
              setHp :int     ,
              setAtk:int     ,
              Dy    :int     ,
              Dx    :int     ,
              y     :list|int,
              x     :list|int,
              perm            ) -> None:
        self.hp    = setHp
        self.atk   = setAtk
        self.stage = 1

        self.Mhp = setHp

        self.face = 'n'

        self.perm = perm

        self.Dy, self.Dx = Dy, Dx
        DRP              = s.Dungeon[self.Dy][self.Dx]
        if isinstance(y, list) or isinstance(x, list):
            while 1:
                sY = randrange(1, s.roomData['maxHeight']-1)
                sX = randrange(1, s.roomData['maxWidth'] -1)

                if self.perm.data[s.Dungeon[Dy][Dx]['room'][sY][sX]["id"]] & self.perm.STEP:
                    self.y = sY if isinstance(y, list) else y
                    self.x = sX if isinstance(x, list) else x
                    event.spawn(
                        self.y, self.x,
                        f"{self.color}{self.icon}{cc['end']}",
                        self.tag
                    )
                    
                    break

                else: continue

        else: self.y,  self.x  = y, x

        blockData = block.take(self.y, self.x)

        self.stepped = blockData\
                if self.perm.data[blockData['id']]&self.perm.MAINTAIN\
            else blockData['blockData']\
                if blockData.get('blockData', False)\
            else block.get('floor')
        
    def wait(self) -> None:
        self.coolTime -= 1
        
        if self.isFocused:
            if self.hp <= 0: self.coolTime = 0
            time.sleep(0.001)

        elif not self.isFocused:
            if[self.Dy, self.Dx] == [s.Dy, s.Dx]:
                self.isFocused = True
                self.coolTime  = 0
            time.sleep(0.01)

    def attack(self, entityData:dict, attackSound:tuple) -> None:
        if not (target:=s.entityMap.get(entityData['tag'])):
            return

        atk = self.atk

        crit     = None
        dmgSound = None

        if randrange(1, 101) <= 10:
            dmgSound = "critical"
            crit     = True
            atk      = int(self.atk*1.5)

        if target.hp-atk > 0:
            msg = f"{self.color}{self.name}{cc['end']}{pp(self.name,'sub',True)} {cc['fg']['R']}{target.name}{cc['end']}에게 {cc['fg']['L']}{atk}{cc['end']}만큼의 피해를 입혔습니다!"
            if crit: msg += f" {cc['fg']['L']}치명타!{cc['end']}"

            target.hitted()
            addLog(msg)

            play(*attackSound)
            if dmgSound:
                play("entity", "enemy", "damage", dmgSound)

        target.hp -= atk

    def attackPlayer(self, atk:int, attackSound:tuple, DR:str="") -> None:
        sound = ("entity", "enemy", "enemyHit")
        s.DROD = (f"{self.color}{DR or self.name}{cc['end']}", self.colorKey)
        if s.df > 0:
            pEvent.defended()
            sound = ("player", "armor", "defended")
            s.df -= 1

            if s.df == 0: dmg = int(atk/2)
            else        : dmg = int(atk/3)

            if s.df==0 and s.dfCrack<=0:
                sound     = ("player", "armor", "armorCrack")
                s.dfCrack = 1

                play  ("player", "armor", "crack")
                addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!", colorKey='B1')
        else:
            pEvent.hitted()
            dmg = atk
        
        s.hp -= dmg
        pEvent.bleeding(dmg)

        play(*attackSound)
        play(*sound)

        addLog(f"{s.lightName}{pp(s.name,'sub',True)} {self.color}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{atk}{cc['end']}만큼의 피해를 입었습니다!", colorKey='R')

    def hitted(self) -> None:
        block.place(
            obj(
                '-be', 'invincibleEntity',
                block=iset(
                    f"{cc['fg']['R']}{self.icon}{cc['end']}"
                ),
                tag=self.tag
            ),
            self.y, self.x
        )
        time.sleep(0.03)

        block.place(
            obj(
                '-be', self.id,
                block=iset(
                    f"{self.color}{self.icon}{cc['end']}"
                ),
                tag=self.tag
            ),
            self.y, self.x
        )

    def step(self, bfy:int, bfx:int) -> None:
        blockData = block.take(self.y, self.x)

        self.face = getFace(self.x, bfx, self.face)
        s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx] = self.stepped
        self.stepped = blockData\
                if self.perm.data[blockData['id']]&self.perm.MAINTAIN\
            else blockData['blockData']\
                if blockData.get('blockData', False)\
            else block.get('floor')
        
        block.place(
            obj(
                '-be', self.id,
                block=iset(f"{self.color}{self.icon}{cc['end']}"),
                tag=self.tag
            ),
            self.y, self.x
        )
        
    def saveData(self):
        s.entityDataMaintained['addAnimal'][self.tag]               = {}
        s.entityDataMaintained['addAnimal'][self.tag]["funcParams"] = self.initFuncParams
        s.entityDataMaintained['addAnimal'][self.tag]['selfParams'] = { k:v for k, v in self.__dict__.items() if k not in negativeVars }

    def loadData(self, data):
        for key, value in data.items():
            exec(f"self.{key} = {repr(value)}")

    def waitingGame(self):
        if f.saveEntity: self.saveData()