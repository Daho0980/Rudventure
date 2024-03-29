import random, time

from   Assets.data             import status, lockers
from   Assets.data.status      import entities
from   Assets.data.color       import cColors        as cc
from   Game.core.system.logger import addLog
from   Game.entities.enemy     import event          as eEvent
from   Game.entities.player    import event


l  = lockers
s  = status

class enemy:
    def __init__(self, name:str, icon:str, ID:int) -> None:
        global entities

        self.name     = name
        self.Dy       = 0
        self.Dx       = 0
        self.y        = 0
        self.x        = 0

        self.atk      = 0
        self.hp       = 0
        self.coolTime = 0
        self.stepped  = 0

        self.icon     = icon
        self.id       = ID

    def damaged(self) -> None:
        if len(s.hitPos) > 0 and [self.y, self.x] in s.hitPos:
            rate:int         = random.randrange(1,101)
            crit, dmg, = 0, s.atk
            if rate <= s.critRate:
                crit = 1
                dmg  = round(eval(f"(s.atk+(s.critDMG*0.1)){random.choice(['+', '-'])}(s.atk*(s.critDMG*0.005))"))
            elif rate >= 90:
                dmg = 0

            self.hp -= dmg
            if self.hp > 0:
                msg = f"{cc['fg']['F']}{self.name}{cc['end']}이(가) {cc['fg']['L']}{dmg}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}"
                if not dmg: msg = f"{cc['fg']['L']}공격{cc['end']}이 빗나갔습니다!"
                elif crit: msg += f" {cc['fg']['L']}치명타!{cc['end']}"
                if dmg: eEvent.hitted(self.y, self.x, self.icon, self.id)
                addLog(msg)

    def start(self, sethp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None:
        self.hp:int       = sethp
        self.atk:int      = setAtk
        self.Dy, self.Dx  = Dy, Dx
        nowDRP:dict       = s.Dungeon[self.Dy][self.Dx]

        if isinstance(y, list) and isinstance(x, list):
            while 1:
                sY  = random.randrange(1,len(nowDRP['room'])-1)
                sX  = random.randrange(1,len(nowDRP['room'][0])-1)
                if s.Dungeon[Dy][Dx]['room'][sY][sX]["id"] in [2, 1, 5, 600, 601, 4, 300, 6, 7]:
                    continue
                else:
                    self.x, self.y = sX, sY
                    eEvent.spawn(self.y, self.x, self.icon)
                    break
        else:
            self.Dy, self.Dx = Dy, Dx
            self.y, self.x   = y, x

    def pDamage(self) -> None:
        event.hitted()
        s.DROD = [f"{cc['fg']['F']}{self.name}{cc['end']}", 'F']
        if s.df > 0:
            s.df -= self.atk
            if s.df < 0                    : s.hp += s.df
            if round(s.df) < 0             : s.df = 0
            if s.df == 0 and s.dfCrack <= 0:
                addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")
                s.dfCrack = 1
        else: s.hp -= self.atk

        addLog(f"{s.lightName}이(가) {cc['fg']['F']}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{self.atk}{cc['end']}만큼의 피해를 입었습니다!")

    def move(self) -> None:
        nowDRP:dict = s.Dungeon[self.Dy][self.Dx]

        if self.coolTime == 0:
            self.coolTime = int((random.randrange(60, 81)*10)/2) if s.publicMode else random.randrange(60, 81)*10
            if self.stepped not in s.stepableBlocks: self.stepped = 0
            elif nowDRP['room'][self.y][self.x]["id"] in s.stepableBlocks and nowDRP['room'][self.y][self.x]["id"] not in [4, 7]:
                self.stepped = nowDRP['room'][self.y][self.x]["id"]
            
            bfx, bfy = self.x, self.y
            if self.hp > 0:
                if random.randrange(1,3000) == 1215:
                    self.atk += 1+(round(s.stage/10))
                    addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon})이 울부짖습니다!")
                    addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon})의 공격력이 {cc['fg']['L']}{1+(round(s.stage/10))}{cc['end']} 상승합니다.")
                    for _ in range(3):
                        nowDRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : self.id}; time.sleep(0.1)
                        nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}; time.sleep(0.1)

                exPos = [
                    nowDRP['room'][self.y-1][self.x]["id"],
                    nowDRP['room'][self.y+1][self.x]["id"],
                    nowDRP['room'][self.y][self.x-1]["id"],
                    nowDRP['room'][self.y][self.x+1]["id"]
                ]

                if 300 in exPos:
                    nowDRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : -1}; time.sleep(0.1)
                    nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
                    if s.ezMode:
                        if random.randrange(1,11)<8: addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!")
                        else:                        enemy.pDamage(self)
                    else: enemy.pDamage(self)
                else:
                    while 1:
                        moveTo:int = random.randrange(-1,2)

                        if random.randrange(0,2):
                            if self.x + moveTo > len(nowDRP['room'][self.y])-1: continue
                            self.x += moveTo
                        else:
                            if self.y + moveTo > len(nowDRP['room'])-1: continue
                            self.y += moveTo

                        if nowDRP['room'][self.y][self.x]["id"] in s.interactableBlocks['cannotStepOn']:
                            self.x, self.y = bfx, bfy
                            continue

                        if nowDRP['room'][self.y][self.x]["id"] == 300:
                            if s.ezMode:
                                if random.randrange(1,11)<8: addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!")
                                else:                        enemy.pDamage(self)
                            else: enemy.pDamage(self)
                        break
                s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx]       = {"block" : s.ids[self.stepped], "id" : self.stepped}
                s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
        else:
            self.coolTime -= 1
            enemy.damaged(self)

            if self.hp > 0 and nowDRP['room'][self.y][self.x] in s.stepableBlocks+s.interactableBlocks['canStepOn']:
                nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
            elif self.hp <= 0: self.coolTime = 0
            time.sleep(0.001)


class observer(enemy):
    def __init__(self, name, icon, ID): super().__init__(name, icon, ID)

    def start(self, sethp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None: super().start(sethp, setAtk, Dy, Dx, y, x)

    def move(self) -> None:
        nowDRP = s.Dungeon[self.Dy][self.Dx]

        def Targetted() -> None:
            for _ in range(2):
                nowDRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : -1}; time.sleep(0.07)
                nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}; time.sleep(0.07)

        if self.coolTime == 0:
            self.coolTime = int((random.randrange(40, 61)*10)/2) if s.publicMode else random.randrange(40, 61)*10
            if self.stepped not in s.stepableBlocks: self.stepped = 0
            elif nowDRP['room'][self.y][self.x]["id"] in s.stepableBlocks and nowDRP['room'][self.y][self.x]["id"] not in [4, 7]:
                self.stepped = nowDRP['room'][self.y][self.x]["id"]

            bfx, bfy = self.x, self.y
            if self.hp > 0:
                Moves, Moves1 = ["+=", "-="], ["+", "-"]
                canBreak:list = [4, 0]
                a:int         = 0

                if self.Dy == s.Dy and self.Dx == s.Dx and (self.x == s.x or self.y == s.y):
                    if self.x == s.x:
                        Targetted()
                        if self.y < s.y: a = 0
                        else           : a = 1

                        while 1:
                            if not l.pause:
                                if nowDRP['room'][eval(f"self.y{Moves1[a]}1")][self.x]["id"] == 300:
                                    if s.ezMode:
                                        if random.randrange(1,11)<8: addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!")
                                        else:                        enemy.pDamage(self)
                                    else: enemy.pDamage(self)
                                if nowDRP['room'][eval(f"self.y{Moves1[a]}1")][self.x]["id"] not in canBreak: break
                                nowDRP['room'][self.y][self.x] = {"block" : s.ids[0], "id" : 0}
                                exec(f"self.y{Moves[a]}1"); nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
                            time.sleep(0.1)

                    elif self.y == s.y:
                        Targetted()
                        if self.x < s.x: a = 0
                        else           : a = 1

                        while 1:
                            if not l.pause:
                                if nowDRP['room'][self.y][eval(f"self.x{Moves1[a]}1")]["id"] == 300:
                                    if s.ezMode:
                                        if random.randrange(1,11)<8: addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!")
                                        else:                        enemy.pDamage(self)
                                    else: enemy.pDamage(self)
                                if nowDRP['room'][self.y][eval(f"self.x{Moves1[a]}1")]["id"] not in canBreak: break
                                nowDRP['room'][self.y][self.x] = {"block" : s.ids[0], "id" : 0}
                                exec(f"self.x{Moves[a]}1"); nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
                            time.sleep(0.1)
                else:
                    bfx, bfy = self.x, self.y
                    if random.randrange(0,2):
                        self.x += 1 if self.x<s.x and nowDRP['room'][self.y][self.x+1]["id"] in s.stepableBlocks\
                            else -1 if self.x>s.x and nowDRP['room'][self.y][self.x-1]["id"] in s.stepableBlocks\
                            else  0
                    else:
                        self.y += 1 if self.y<s.y and nowDRP['room'][self.y+1][self.x]["id"] in s.stepableBlocks\
                            else -1 if self.y>s.y and nowDRP['room'][self.y-1][self.x]["id"] in s.stepableBlocks\
                            else  0
                    nowDRP['room'][bfy][bfx]       = {"block" : s.ids[0], "id" : 0}
                    nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
        else:
            self.coolTime -= 1
            super().damaged()
            
            if self.hp > 0 and nowDRP['room'][self.y][self.x] in s.stepableBlocks+s.interactableBlocks['canStepOn']:
                nowDRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id}
            elif self.hp <= 0: self.coolTime = 0
            time.sleep(0.001)
    