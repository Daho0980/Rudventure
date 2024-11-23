import math # 이거 쓰는거임
import time
from   random import randrange, choice

from .                        import event        as eEvent
from .status                  import cooltimes
from Assets.data.color        import cColors      as cc
from Assets.data.comments     import TIOTA
from Game.core.system.logger  import addLog
from Game.entities.algorithms import AStar
from Game.entities.player     import event, say
from Game.utils.system.sound  import play
from Game.utils.graphics      import escapeAnsi

from Assets.data import (
    totalGameStatus as s,
    lockers         as l
    )


# region Monster common code
class Enemy:
    def __init__(self, name:str, icon:str, ID:int, hashKey:str) -> None:
        self.hashKey = hashKey
        self.name    = name
        self.Dy      = 0
        self.Dx      = 0
        self.y       = 0
        self.x       = 0

        self.atk      = 0
        self.hp       = 0
        self.coolTime = 0
        self.stepped  = {}

        self.icon = icon
        self.id   = ID

        self.isFocused = True
        
        self.xpMultiplier = 1

    def start(
            self,
            setHp:int,
            setAtk:int,
            Dy:int,
            Dx:int,
            y:list|int,
            x:list|int
    ) -> None:
        self.hp           = setHp
        self.atk          = setAtk
        self.Dy, self.Dx  = Dy, Dx

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
                    eEvent.spawn(self.y, self.x, self.icon)
                    break
        else:
            self.Dy, self.Dx = Dy, Dx
            self.y, self.x   = y, x
        
        self.stepped = DRP['room'][self.y][self.x]\
                       if   DRP in s.monsterInteractableBlocks['steppable']['maintainable']\
                       else {"block" : " ", "id" : 0, "type" : 0}

    def damaged(self) -> None:
        if s.hitPos['pos'] and [self.y, self.x] in s.hitPos['pos']:
            posIndex = s.hitPos['pos'].index([self.y, self.x])

            rate:int         = randrange(1,101)
            sound            = None
            crit, isHit      = None, True
            entity, dmg, attackSound = s.hitPos['data'][posIndex][0], s.hitPos['data'][posIndex][1], s.hitPos['data'][posIndex][2]

            if entity == "player":
                if rate <= s.critRate:
                    sound, crit = "critical", True
                    dmg         = round(eval(f"(s.atk+(s.critDMG*0.1)){choice(['+', '-'])}(s.atk*(s.critDMG*0.005))"))
                elif rate >= 90:
                    sound, dmg, isHit = "miss", 0, False
            else: crit = False

            self.hp -= dmg
            if self.hp > 0:
                msg = f"{cc['fg']['F']}{self.name}{cc['end']}이(가) {cc['fg']['L']}{dmg}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}"
                if   not dmg: msg = f"{cc['fg']['L']}공격{cc['end']}이 빗나갔습니다!"
                elif crit:    msg += f" {cc['fg']['L']}치명타!{cc['end']}"

                if dmg: eEvent.hitted(self.y, self.x, self.icon, self.id, self.hashKey)
                addLog(msg, colorKey='L')
                if sound: play("entity", "enemy", "damage", sound)
                if isHit: play(*attackSound)

    def attack(self, Dir:list, DR:str="") -> None:
        if randrange(1,101) <= eval(s.statusFormula['evasion']):
            play("player", "evasion")
            addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!", colorKey='A')
        else:
            sound  = ("entity", "enemy", "enemyHit")
            s.DROD = [f"{cc['fg']['F']}{self.name if not DR else DR}{cc['end']}", 'F']

            if s.target['hashKey'] != self.hashKey:
                s.target['hashKey']    = self.hashKey
                s.target['attackable'] = False

            if s.df > 0:
                event.defended()
                sound = ("player", "armor", "defended")
                self.knockback(Dir, randrange(1,3), s.atk)
                s.df -= 1
                if s.df == 0: s.hp -= int(self.atk/2)
                else:         s.hp -= int(self.atk/3)

                if s.df==0 and s.dfCrack<=0:
                    sound     = ("player", "armor", "armorCrack")
                    s.dfCrack = 1
                    play("player", "armor", "crack")
                    addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!", colorKey='B1')
            else:
                event.hitted()
                s.hp -= self.atk

            play(*sound)
            addLog(f"{s.lightName}이(가) {cc['fg']['F']}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{self.atk}{cc['end']}만큼의 피해를 입었습니다!", colorKey='R')

    def knockback(self, Dir:list, length:int, atk:int) -> None:
        DRP = s.Dungeon[self.Dy][self.Dx]

        for i in range(length):
            if DRP['room'][self.y-Dir[0]][self.x-Dir[1]]['id']\
            in s.monsterInteractableBlocks['unsteppable']:
                play("object", "wall", "hit")
                eEvent.hitted(self.y, self.x, self.icon, self.id, self.hashKey)
                self.hp -= atk-i
                addLog(f"{cc['fg']['F']}{self.name}{cc['end']}이(가) {cc['fg']['L']}{atk-i}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}", colorKey='R')
                return
            
            s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = self.stepped

            self.y -= Dir[0]
            self.x -= Dir[1]

            self.stepped                                        = s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]
            s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id, "type" : 1, "hashKey" : self.hashKey}

            time.sleep(0.05)

    def isTargetted(self) -> None:
        if  s.target['hashKey'] == self.hashKey\
        and s.target['command']:
            for _ in range(2):
                s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = {"block" : f"{cc['bg']['L']}{self.icon}{cc['end']}", "id" : -1, "type" : 1, "hashKey" : self.hashKey}; time.sleep(0.07)
                s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = {"block" : self.icon, "id" : -1, "type" : 1, "hashKey" : self.hashKey};                                time.sleep(0.07)
            s.target['command'] = False

    def wait(self) -> None:
        self.coolTime -= 1

        if self.isFocused:
            self.damaged()
            self.isTargetted()
            if self.hp <= 0: self.coolTime = 0
            time.sleep(0.001)

        elif not self.isFocused:
            if[self.Dy, self.Dx] == [s.Dy, s.Dx]:
                self.isFocused = True
                self.coolTime  = 0
            time.sleep(0.5)

    def step(self, bfy:int, bfx:int, saveStepped:bool=True) -> None:
        s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx] = self.stepped
        if saveStepped:
            self.stepped = s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]\
                                if s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]['id'] in s.monsterInteractableBlocks['steppable']['maintainable']\
                        else {"block" : " ", "id" : 0, "type" : 0}
            
        s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = {
            "block"   : self.icon,
            "id"      : self.id,
            "type"    : 1,
            "hashKey" : self.hashKey
            }
        

# region Pain
class Pain(Enemy):
    """
    # 고통의 편린
    - 일개 잡몹
    - 플레이어를 추격함
    - 체력은 4+(2*stage)
    - 플레이어가 상/하/좌/우 1 칸 이내에 있다면 공격함
    - 확률적으로 포효를 내질러 자신의 공격력이 1+(round(stage/10)) 증가함
    - 기본적인 아이콘 -> %

    - 보스방 스폰 가능
    """
    def __init__(self, name, icon, ID, hashKey):
        super().__init__(name, icon, ID, hashKey)
        self.coolTimes = cooltimes.Pain()

        if s.sanjibaMode: self.coolTimes.divideHalf()

    def start(self, setHp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None: super().start(setHp, setAtk, Dy, Dx, y, x)

    def move(self) -> None:
        DRP  = s.Dungeon[self.Dy][self.Dx]

        if not self.coolTime:
            # self.coolTime = int((randrange(60, 81)*10)/2) if s.sanjibaMode else randrange(60, 81)*10
            self.coolTime = randrange(*self.coolTimes.turnEnd)
            if self.isFocused:
                if [self.Dy, self.Dx] != [s.Dy, s.Dx]: self.isFocused = False; return
                
                bfx, bfy = self.x, self.y
                if self.hp > 0:
                    if randrange(1,3000) == 1215:
                        self.atk += 1+(round(s.stage/10))
                        play("entity", "enemy", "pain", "growl")
                        addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon})이 울부짖습니다!",                                                          colorKey='F')
                        addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon})의 공격력이 {cc['fg']['L']}{1+(round(s.stage/10))}{cc['end']} 상승합니다.", colorKey='F')
                        for _ in range(3):
                            DRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : -1, "type" : 1, "hashKey" : self.hashKey}; time.sleep(0.1)
                            DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : -1, "type" : 1, "hashKey" : self.hashKey};                                time.sleep(0.1)
                        DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id, "type" : 1, "hashKey" : self.hashKey}

                    path = AStar.main(
                        (self.y, self.x),
                        [300],
                        s.monsterInteractableBlocks['steppable']['total']
                        )
                    if not path:
                        ay, ax = -1, -1
                        if sum([ay,ax])==-2 or (self.y,self.x) == (ay,ax):
                            while 1:
                                ay = randrange(1, len(DRP['room'])-1)
                                ax = randrange(1, len(DRP['room'][0])-1)
                                if DRP['room'][ay][ax]['id'] in s.interactableBlocks['unsteppable']: continue
                                break

                        if randrange(0,2):
                            self.x += 1\
                                    if self.x<ax\
                                       and DRP['room'][self.y][self.x+1]["id"] in s.interactableBlocks['steppable']['total']\
                                else -1\
                                    if self.x>ax\
                                       and DRP['room'][self.y][self.x-1]["id"] in s.interactableBlocks['steppable']['total']\
                                else  0
                        else:
                            self.y += 1\
                                   if self.y<ay\
                                   and DRP['room'][self.y+1][self.x]["id"] in s.interactableBlocks['steppable']['total']\
                                else -1\
                                   if self.y>ay\
                                   and DRP['room'][self.y-1][self.x]["id"] in s.interactableBlocks['steppable']['total']\
                                else  0
                    elif DRP['room'][path[0]][path[1]]['id'] == 300:
                        DRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : -1, "type" : 1, "hashKey" : self.hashKey}; time.sleep(0.1)
                        DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id, "type" : 1, "hashKey" : self.hashKey}

                        self.attack(
                            [path[0]-self.y, path[1]-self.x],
                            choice(["물어뜯김", "과다출혈", "쇼크"])
                            )
                    else: self.y, self.x = path
                    super().step(bfy, bfx)
        else: self.wait()


# region Unrest
class Unrest(Enemy):
    """
    # 불안의 편린
    - 돌격형 유닛
    - 언제나 플레이어의 위치를 알고 쫓아옴
    - 체력은 10+(2*stage)
    - x값 또는 y값이 플레이어와 같다면 플레이어가 있는 방향으로 돌진함
    - 기본적인 아이콘 -> #

    - 보스방 스폰 가능
    """
    def __init__(self, name, icon, ID, hashKey):
        super().__init__(name, icon, ID, hashKey)
        self.coolTimes = cooltimes.Unrest()

        if s.sanjibaMode: self.coolTimes.divideHalf()

    def start(self, setHp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None: super().start(setHp, setAtk, Dy, Dx, y, x)

    def Targetted(self, DRP) -> None:
        play("entity", "enemy", "unrest", "targetLock")
        for _ in range(3):
            DRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : -1, "type" : 1, "hashKey" : self.hashKey}
            time.sleep(self.coolTimes.targetted)
            DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : -1, "type" : 1, "hashKey" : self.hashKey}
            time.sleep(self.coolTimes.targetted)

    def move(self) -> None:
        DRP = s.Dungeon[self.Dy][self.Dx]

        if not self.coolTime:
            # self.coolTime = int((randrange(40, 51)*10)/2) if s.sanjibaMode else randrange(40, 51)*10
            self.coolTime = randrange(*self.coolTimes.turnEnd)
            if self.isFocused:
                if [self.Dy, self.Dx] != [s.Dy, s.Dx]: self.isFocused = False; return

                bfx, bfy = self.x, self.y
                if self.hp > 0:
                    Moves, Moves1 = ["+=", "-="], ["+", "-"]

                    if (self.Dy, self.Dx)==(s.Dy, s.Dx) and (self.y==s.y or self.x==s.x):
                        self.stepped = {"block" : s.ids[0], "id" : 0, "type" : 0}

                        if self.x == s.x:
                            a = 0 if self.y<s.y else 1
                            self.Targetted(DRP)

                            while 1:
                                if not l.pause:
                                    if DRP['room'][eval(f"self.y{Moves1[a]}1")][self.x]["id"] == 300:
                                        self.attack(
                                            [eval(f"0{Moves1[a]}1"), 0],
                                            choice(["충격파", "교통사고", "들이박힘"])
                                            ); break
                                    if DRP['room'][eval(f"self.y{Moves1[a]}1")][self.x]["id"] not in s.monsterInteractableBlocks['breakable']: break

                                    bfy, bfx = self.y, self.x
                                    exec(f"self.y{Moves[a]}1")
                                    super().step(bfy, bfx, saveStepped=False)
                                time.sleep(self.coolTimes.rush)

                        elif self.y == s.y:
                            a = 0 if self.x<s.x else 1
                            self.Targetted(DRP)

                            while 1:
                                if not l.pause:
                                    if DRP['room'][self.y][eval(f"self.x{Moves1[a]}1")]["id"] == 300:
                                        self.attack(
                                            [0, eval(f"0{Moves1[a]}1")],
                                            choice(["충격파", "교통사고", "들이박힘"])
                                            ); break
                                    if DRP['room'][self.y][eval(f"self.x{Moves1[a]}1")]["id"] not in s.monsterInteractableBlocks['breakable']: break

                                    bfy, bfx = self.y, self.x
                                    exec(f"self.x{Moves[a]}1")
                                    super().step(bfy, bfx, saveStepped=False)
                                time.sleep(self.coolTimes.rush)

                        DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id, "type" : 1, "hashKey" : self.hashKey}

                    else:
                        if randrange(0,2):
                            self.x += 1 if self.x<s.x and DRP['room'][self.y][self.x+1]["id"] in s.monsterInteractableBlocks['steppable']['total']\
                                else -1 if self.x>s.x and DRP['room'][self.y][self.x-1]["id"] in s.monsterInteractableBlocks['steppable']['total']\
                                else  0
                        else:
                            self.y += 1 if self.y<s.y and DRP['room'][self.y+1][self.x]["id"] in s.monsterInteractableBlocks['steppable']['total']\
                                else -1 if self.y>s.y and DRP['room'][self.y-1][self.x]["id"] in s.monsterInteractableBlocks['steppable']['total']\
                                else  0
                        super().step(bfy, bfx)
        else: super().wait()


# region Resentment
class Resentment(Enemy):
    """
    # 원망의 편린
    - 지뢰
    - 기본적으로 움직이지 않고 enemyCount에 합산되지 않음
    - 체력은 5+(2*stage)
    - 감지 범위는 상/하/좌/우 모두 1임. 대각선으로는 탐지 불가능
    - 기본적인 아이콘 -> ※
    
    - 보스방에서는 스폰되지 않음.
    """
    def __init__(self, name, icon, ID, hashKey):
        super().__init__(name, icon, ID, hashKey)
        self.coolTimes = cooltimes.Resentment()

        if s.sanjibaMode:
            self.coolTimes.divideHalf()
            addLog(str(self.coolTimes.blink), duration=1000)

    def start(self,
              setHp:int,
              setAtk:int,
              Dy:int,
              Dx:int,
              y:int,
              x:int
    ) -> None: super().start(setHp, setAtk, Dy, Dx, y, x)

    def blink(self, DRP) -> None:
        DRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}{self.icon}{cc['end']}", "id" : -1, "type" : 1, "hashKey" : self.hashKey}
        time.sleep(self.coolTimes.blink)
        DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id, "type" : 1, "hashKey" : self.hashKey}
        time.sleep(self.coolTimes.blink)

    def targetted(self, DRP) -> None:
        for _ in range(3): self.blink(DRP)

    def explotion(self, DRP) -> None:
        expPs = [
            [self.y-1,self.x],
            [self.y+1,self.x],
            [self.y,self.x-1],
            [self.y,self.x+1]
            ]

        DRP['room'][self.y][self.x] = {"block" : f"{cc['fg']['F']}X{cc['end']}", "id" : -1, "type" : 0}
            
        for expP in expPs:
            if DRP['room'][expP[0]][expP[1]]["id"] in s.interactableBlocks["explodable"]:
               DRP['room'][expP[0]][expP[1]] = {"block" : f"{cc['fg']['F']}.{cc['end']}", "id" : -1, "type" : 0}
            elif DRP['room'][expP[0]][expP[1]]["id"] in [300, 301]:
                s.steppedBlock = {
                    "block" : f"{cc['fg']['G1']}{escapeAnsi(DRP['room'][expP[0]][expP[1]]['block'])}{cc['end']}",
                    "id"    : 900,
                    "type"  : 0,
                    "nbt"   : {
                        "count" : 0
                    }
                    }
        time.sleep(self.coolTimes.explotion)
            
        for expP in expPs:
            if DRP['room'][expP[0]][expP[1]] == {"block" : f"{cc['fg']['F']}.{cc['end']}", "id" : -1, "type" : 0}:
               DRP['room'][expP[0]][expP[1]] = {
                   "block" : f"{cc['fg']['G1']}.{cc['end']}",
                   "id"    : 900,
                   "type"  : 0,
                   "nbt"   : {
                       "count" : 0
                   }
                   }
            
        self.icon = choice(['×', 'x', 'X'])
        self.hp   = 0

    def move(self) -> None:
        DRP = s.Dungeon[self.Dy][self.Dx]
            
        if not self.coolTime:
            self.coolTime = self.coolTimes.turnEnd
            if self.isFocused:
                if [self.Dy, self.Dx] != [s.Dy, s.Dx]: self.isFocused = False; return

                if self.hp > 0:
                    if 300 in [
                        DRP['room'][self.y-1][self.x]["id"],
                        DRP['room'][self.y+1][self.x]["id"],
                        DRP['room'][self.y][self.x-1]["id"],
                        DRP['room'][self.y][self.x+1]["id"]
                        ]:
                        self.targetted(DRP)

                        if 300 in [
                            DRP['room'][self.y-1][self.x]["id"],
                            DRP['room'][self.y+1][self.x]["id"],
                            DRP['room'][self.y][self.x-1]["id"],
                            DRP['room'][self.y][self.x+1]["id"]
                            ]:
                            play("entity", "enemy", "resentment", "explosion")
                            self.attack([0, 0], "폭발")
                            
                            self.explotion(DRP)
                            self.xpMultiplier = 2
                            if randrange(0,2): say(choice(TIOTA))
                        else: DRP['room'][self.y][self.x] = {"block" : self.icon, "id" : self.id, "type" : 1, "hashKey" : self.hashKey}
                    else: self.blink(DRP)

        else: super().wait()
