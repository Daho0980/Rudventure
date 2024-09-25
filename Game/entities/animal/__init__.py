import time
from   random import randrange, choice

from Assets.data             import lockers, status
from Assets.data.color       import cColors as cc
from Game.core.system.logger import addLog
from Game.entities           import event
from Game.entities.player    import event as pEvent
from Game.utils.system.sound import play


l, s = lockers, status

class Animal:
    def __init__(self,
                 tribe:str,
                 name:str,
                 icon:str,
                 ID:int,
                 color:str,
                 colorKey:str,
                 hashKey:str,
                 initFuncParams:list) -> None:
        self.tribe   = tribe
        self.hashKey = hashKey

        self.name = name
        self.Dy   = 0
        self.Dx   = 0
        self.y    = 0
        self.x    = 0

        self.atk      = 0
        self.hp       = 0
        self.coolTime = 0
        self.stepped  = {}

        self.Mhp = 0

        self.icon     = icon
        self.id       = ID
        self.color    = color
        self.colorKey = colorKey

        self.isFocused = True

        self.initFuncParams = initFuncParams

    def start(
            self,
            setHp:int,
            setAtk:int,
            Dy:int,
            Dx:int,
            y:list|int,
            x:list|int
        ) -> None:
        self.hp          = setHp
        self.atk         = setAtk
        self.stage       = 1

        self.Mhp = setHp

        DRP = s.Dungeon[self.Dy][self.Dx]

        if isinstance(y, list) or isinstance(x, list):
            while 1:
                sY = randrange(1,len(DRP['room'])-1)
                sX = randrange(1,len(DRP['room'][0])-1)
                if s.Dungeon[Dy][Dx]['room'][sY][sX]["id"] in s.monsterInteractableBlocks['unsteppable']:
                    continue
                else:
                    self.y = sY if isinstance(y, list) else y
                    self.x = sX if isinstance(x, list) else x
                    event.spawn(self.y, self.x, f"{self.color}{self.icon}{cc['end']}", self.hashKey)
                    break
        else:
            self.Dy, self.Dx = Dy, Dx
            self.y, self.x   = y, x

        self.stepped = DRP['room'][self.y][self.x]\
                       if   DRP in s.interactableBlocks['steppable']['maintainable']\
                       else {"block" : " ", "id" : 0, "type" : 0}
        
    def damaged(self) -> None:
        if s.hitPos['pos'] and [self.y, self.x] in s.hitPos['pos']:
            posIndex = s.hitPos['pos'].index([self.y, self.x])

            rate:int         = randrange(1,101)
            sound            = None
            crit, isHit      = True, True
            entity, dmg, attackSound = s.hitPos['data'][posIndex][0], s.hitPos['data'][posIndex][1], s.hitPos['data'][posIndex][2]

            if entity == "player":
                if rate <= s.critRate:
                    sound, crit = "critical", True
                    dmg         = round(eval(f"(s.atk+(s.critDMG*0.1)){choice(['+', '-'])}(s.atk*(s.critDMG*0.005))"))
                elif rate >= 90:
                    sound, dmg, isHit = "miss", 0, False

            self.hp -= dmg
            if self.hp > 0:
                msg = f"{cc['fg']['F']}{self.name}{cc['end']}이(가) {cc['fg']['L']}{dmg}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}"
                if   not dmg: msg  = f"{cc['fg']['L']}공격{cc['end']}이 빗나갔습니다!"
                elif crit:    msg += f" {cc['fg']['L']}치명타!{cc['end']}"

                if dmg: event.hitted(self.y, self.x, f"{self.color}{self.icon}{cc['end']}", self.id, self.hashKey)
                addLog(msg)
                if sound: play("entity", "enemy", "damage", sound)
                if isHit: play(*attackSound)
        
    def wait(self) -> None:
        self.coolTime -= 1
        
        if self.isFocused:
            self.damaged()
            if self.hp <= 0: self.coolTime = 0
            time.sleep(0.001)

        elif not self.isFocused:
            if[self.Dy, self.Dx] == [s.Dy, s.Dx]:
                self.isFocused = True
                self.coolTime  = 0
            time.sleep(0.01)

    def attack(self, ty:int, tx:int, attackSound:tuple) -> None:
        s.hitPos['pos'].append([ty, tx])
        s.hitPos['data'].append([self.tribe, self.atk, attackSound])
        time.sleep(0.001)
        s.hitPos['pos'].remove([ty, tx])
        s.hitPos['data'].remove([self.tribe, self.atk, attackSound])

    def attackPlayer(self, atk:int, attackSound:tuple, DR:str="") -> None:
        sound = ("entity", "enemy", "enemyHit")
        s.DROD = [f"{self.color}{DR or self.name}{cc['end']}", self.colorKey]
        if s.df > 0:
            pEvent.defended()
            play("player", "armor", "defended")
            s.df -= 1
            if s.df == 0: s.hp -= int(atk/2)
            else:         s.hp -= int(atk/3)

            if s.df == 0 and s.dfCrack <= 0:
                sound     = ("player", "armor", "crack")
                s.dfCrack = 1
                addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")
        else:
            pEvent.hitted()
            s.hp -= atk

        play(*attackSound)
        play(*sound)
        addLog(f"{s.lightName}이(가) {self.color}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{atk}{cc['end']}만큼의 피해를 입었습니다!")

    def step(self, bfy:int, bfx:int) -> None:
        s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx] = self.stepped
        self.stepped = s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]\
                       if   s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]['id'] in s.monsterInteractableBlocks['steppable']['maintainable']\
                       else {"block" : " ", "id" : 0, "type" : 0}
        s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = {
            "block"   : f"{self.color}{self.icon}{cc['end']}",
            "id"      : self.id,
            "type"    : 1,
            "hashKey" : self.hashKey
            }
        
    def saveData(self):
        s.entityDataMaintained['addAnimal'][self.hashKey] = {}
        s.entityDataMaintained['addAnimal'][self.hashKey]["funcParams"] = self.initFuncParams
        s.entityDataMaintained['addAnimal'][self.hashKey]['selfParams'] = self.__dict__

    def loadData(self, data):
        for key, value in data.items():
            exec(f"self.{key} = {repr(value)}")

    def waitingGame(self):
        if s.entitySaveTrigger: self.saveData()