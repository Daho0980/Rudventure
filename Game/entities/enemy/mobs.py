import math # 이거 쓰는거임
import time
from   random import randrange, choice

from .                           import event    as eEv
from .status                     import cooltimes
from Assets.data.color           import cColors  as cc
from Assets.data.comments        import TIOTA
from functions.grammar           import pstpos as pp
from Game.core.system.logger     import addLog
from Game.core.system.dataLoader import obj
from Game.entities.algorithms    import AStar
from Game.entities.functions     import getFace
from Game.utils.system.block     import iset
from Game.utils.system.sound     import play
from Game.utils.graphics         import escapeAnsi

from Assets.data import (
    totalGameStatus as s,
    lockers         as l
)
from Game.entities.player import (
    event        as pEv,
    statusEffect as se,
    
    say
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
        self.face    = 'n'

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
              x     :list|int ) -> None:
        self.hp           = setHp
        self.atk          = setAtk
        self.Dy, self.Dx  = Dy, Dx

        DRP = s.Dungeon[self.Dy][self.Dx]

        if isinstance(y, list) or isinstance(x, list):
            while 1:
                sY = randrange(1,len(DRP['room']   )-1)
                sX = randrange(1,len(DRP['room'][0])-1)

                if s.Dungeon[Dy][Dx]['room'][sY][sX]["id"] in s.monsterInteractableBlocks['unsteppable']:
                    continue
                else:
                    self.y = sY if isinstance(y, list) else y
                    self.x = sX if isinstance(x, list) else x
                    eEv.spawn(self.y, self.x, self.icon)

                    break

        else:
            self.Dy, self.Dx = Dy, Dx
            self.y, self.x   = y, x
        
        self.stepped = DRP['room'][self.y][self.x]\
                       if   DRP in s.monsterInteractableBlocks['steppable']['maintainable']\
                       else obj('-bb', '0')

    def damaged(self) -> None:
        if s.hitPos['pos'] and [self.y, self.x] in s.hitPos['pos']:
            posIndex = s.hitPos['pos'].index([self.y, self.x])

            rate:int                 = randrange(1,101)
            sound                    = None
            crit, isHit              = None, True
            entity, dmg, attackSound = s.hitPos['data'][posIndex]

            if entity == "player":
                if rate <= s.critRate:
                    sound, crit = "critical", True
                    dmg         = round(eval(f"(s.atk+(s.critDMG*0.1)){choice(['+','-'])}(s.atk*(s.critDMG*0.005))"))

                elif rate >= 90:
                    sound, dmg, isHit = "miss", 0, False

            else: crit = False

            self.hp -= dmg
            if self.hp > 0:
                msg = f"{cc['fg']['F']}{self.name}{cc['end']}{pp(self.name,'sub',True)} {cc['fg']['L']}{dmg}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}"
                if   not dmg: msg  = f"{cc['fg']['L']}공격{cc['end']}이 빗나갔습니다!"
                elif crit:    msg += f" {cc['fg']['L']}치명타!{cc['end']}"

                if dmg: eEv.hitted(self.y, self.x, self.icon, self.id, self.hashKey)
                addLog(msg, colorKey='L')

                if sound: play("entity", "enemy", "damage", sound)
                if isHit: play(*attackSound)

    def attack(self, Dir:list, DR:str="") -> None:
        if randrange(1,101) <= eval(s.statusFormula['evasion']):
            play  ("player", "evasion")
            addLog(f"{cc['fg']['F']}{self.name}{cc['end']}의 공격을 피했습니다!", colorKey='A')

        else:
            sound  = ("entity", "enemy", "enemyHit")
            s.DROD = [f"{cc['fg']['F']}{self.name if not DR else DR}{cc['end']}", 'F']

            if s.target['hashKey'] != self.hashKey:
                s.target['hashKey']    = self.hashKey
                s.target['attackable'] = False

            if s.df > 0:
                pEv.defended()
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
                pEv.hitted()
                dmg = self.atk

            s.hp -= dmg
            pEv.bleeding(dmg)

            play(*sound)
            addLog(
                f"{s.lightName}{pp(s.name,'sub',True)} {cc['fg']['F']}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{self.atk}{cc['end']}만큼의 피해를 입었습니다!",
                colorKey='R'
            )

    def knockback(self, Dir:list, length:int, atk:int) -> None:
        room = s.Dungeon[self.Dy][self.Dx]['room']

        for i in range(length):
            if room[self.y-Dir[0]][self.x-Dir[1]]['id']\
            in s.monsterInteractableBlocks['unsteppable']:
                play("object", "wall", "hit")
                eEv.hitted(self.y, self.x, self.icon, self.id, self.hashKey)
                self.hp -= atk-i
                addLog(f"{cc['fg']['F']}{self.name}{cc['end']}{pp(self.name,'sub',True)} {cc['fg']['L']}{atk-i}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}", colorKey='R')

                return
            
            s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = self.stepped

            self.face = getFace(self.x-Dir[1], self.x, self.face)
            self.y   -= Dir[0]
            self.x   -= Dir[1]

            self.stepped                                        = s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]
            s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = obj('-be', str(self.id), block=iset(self.icon), hashKey=self.hashKey)

            time.sleep(0.05)

    def isTargetted(self) -> None:
        if  s.target['hashKey'] == self.hashKey\
        and s.target['command']:
            for _ in range(2):
                s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = obj('-be', '-1', block=iset(f"{cc['bg']['L']}{self.icon}{cc['end']}"), hashKey=self.hashKey); time.sleep(0.07)
                s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = obj('-be', '-1', block=iset(self.icon), hashKey=self.hashKey);                                time.sleep(0.07)

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
        block = s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x]

        self.face = getFace(self.x, bfx, self.face)
        s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx] = self.stepped

        if saveStepped:
            self.stepped = block\
                    if block['id']\
                    in s.monsterInteractableBlocks['steppable']['maintainable']\
                else block['blockData']\
                    if block.get('blockData', False)\
                else obj('-bb', '0')
            
        s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = obj('-be', str(self.id), block=iset(self.icon), hashKey=self.hashKey)
        

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

        if s.sanjibaMode: self.coolTimes.divideHalf(self.coolTimes.modeException)

    def start(self, setHp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None: super().start(setHp, setAtk, Dy, Dx, y, x)

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
                        se.addEffect('600', 50)
                        addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon}){pp(self.name,'sub',True)} 울부짖습니다!", colorKey='F')
                        addLog(f"{cc['fg']['F']}{self.name}{cc['end']}({self.icon})의 공격력이 {cc['fg']['L']}{1+(round(s.stage/10))}{cc['end']}만큼 상승합니다.", colorKey='F')

                        for _ in range(3):
                            DRP['room'][self.y][self.x] = obj(
                                '-be', '-1',
                                block  =f"{cc['fg']['F']}{self.icon}{cc['end']}",
                                hashKey=self.hashKey
                            )
                            time.sleep(0.1)

                            DRP['room'][self.y][self.x] = obj(
                                '-be', '-1',
                                block  =self.icon,
                                hashKey=self.hashKey
                            )
                            time.sleep(0.1)

                        DRP['room'][self.y][self.x] = obj('-be', str(self.id), block=self.icon, hashKey=self.hashKey)

                    path = AStar.main(
                        (self.y, self.x),
                        [300],
                        s.monsterInteractableBlocks['steppable']['total']
                        )
                    if not path:
                        ay, ax = -1, -1
                        if sum([ay,ax])==-2 or (self.y,self.x)==(ay,ax):
                            while 1:
                                if DRP['room'][
                                    ay:=randrange(1, len(DRP['room'])-1)][
                                    ax:=randrange(1, len(DRP['room'][0])-1)]\
                                ['id'] in s.interactableBlocks['unsteppable']: continue
                                break

                        if randrange(0,2):
                            self.x += 1\
                                    if self.x<ax\
                                       and DRP['room'][self.y][self.x+1]["id"] in s.interactableBlocks['steppable']['total']\
                                else -1\
                                    if self.x>ax\
                                       and DRP['room'][self.y][self.x-1]["id"] in s.interactableBlocks['steppable']['total']\
                                else 0
                            
                        else:
                            self.y += 1\
                                   if  self.y<ay\
                                   and DRP['room'][self.y+1][self.x]["id"] in s.interactableBlocks['steppable']['total']\
                                else -1\
                                   if  self.y>ay\
                                   and DRP['room'][self.y-1][self.x]["id"] in s.interactableBlocks['steppable']['total']\
                                else 0
                    elif DRP['room'][path[0]][path[1]]['id'] == 300:
                        DRP['room'][self.y][self.x] = obj(
                            '-be', '-1',
                            block=f"{cc['fg']['F']}{self.icon}{cc['end']}",
                            hashKey=self.hashKey
                        )
                        time.sleep(0.1)

                        DRP['room'][self.y][self.x] = obj(
                            '-be', str(self.id),
                            block  =self.icon,
                            hashKey=self.hashKey
                        )

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

        if s.sanjibaMode:
            self.coolTimes.divideHalf(self.coolTimes.modeException)

    def start(self, setHp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None: super().start(setHp, setAtk, Dy, Dx, y, x)

    def Targetted(self, DRP) -> None:
        play("entity", "enemy", "unrest", "targetLock")
        for _ in range(3):
            DRP['room'][self.y][self.x] = obj(
                '-be', '-1',
                block  =iset(f"{cc['fg']['F']}{self.icon}{cc['end']}"),
                hashKey=self.hashKey
            )
            time.sleep(self.coolTimes.targetted)

            DRP['room'][self.y][self.x] = obj(
                '-be', '-1',
                block  =iset(self.icon),
                hashKey=self.hashKey
            )
            time.sleep(self.coolTimes.targetted)

    def move(self) -> None:
        DRP = s.Dungeon[self.Dy][self.Dx]

        if not self.coolTime:
            self.coolTime = randrange(*self.coolTimes.turnEnd)
            if self.isFocused:
                if [self.Dy, self.Dx] != [s.Dy, s.Dx]: self.isFocused = False; return

                bfx, bfy = self.x, self.y
                if self.hp > 0:
                    Moves, Moves1 = ["+=", "-="], ["+", "-"]

                    if (self.Dy, self.Dx)==(s.Dy, s.Dx) and (self.y==s.y or self.x==s.x):
                        self.stepped = obj('-bb', '0')

                        if self.x == s.x:
                            a = 0 if self.y<s.y else 1
                            self.Targetted(DRP)

                            while 1:
                                if not l.pause:
                                    if DRP['room'][eval(f"self.y{Moves1[a]}1")][self.x]["id"] == 300:
                                        self.attack(
                                            [eval(f"0{Moves1[a]}1"), 0],
                                            choice(["충격파", "추돌", "들이박힘"])
                                        ); break
                                    
                                    if  DRP['room'][eval(f"self.y{Moves1[a]}1")][self.x]["id"]\
                                    not in s.monsterInteractableBlocks['breakable']:
                                        break

                                    bfy, bfx = self.y, self.x
                                    exec(f"self.y{Moves[a]}1")

                                    super().step(bfy, bfx, saveStepped=False)

                                time.sleep(self.coolTimes.rush)
                            
                            play("entity", "enemy", "unrest", "crash")

                        elif self.y == s.y:
                            a = 0 if self.x<s.x else 1
                            self.Targetted(DRP)

                            while 1:
                                if not l.pause:
                                    if DRP['room'][self.y][eval(f"self.x{Moves1[a]}1")]["id"] == 300:
                                        self.attack(
                                            [0, eval(f"0{Moves1[a]}1")],
                                            choice(["충격파", "추돌", "들이박힘"])
                                            ); break
                                    
                                    if  DRP['room'][self.y][eval(f"self.x{Moves1[a]}1")]["id"]\
                                    not in s.monsterInteractableBlocks['breakable']:
                                        break

                                    bfy, bfx = self.y, self.x
                                    exec(f"self.x{Moves[a]}1")

                                    super().step(bfy, bfx, saveStepped=False)

                                time.sleep(self.coolTimes.rush)
                            
                            play("entity", "enemy", "unrest", "crash")

                    else:
                        if randrange(0,2):
                            self.x += 1\
                                    if self.x<s.x and DRP['room'][self.y][self.x+1]["id"]\
                                    in s.monsterInteractableBlocks['steppable']['total']\
                                else -1\
                                    if self.x>s.x and DRP['room'][self.y][self.x-1]["id"]\
                                    in s.monsterInteractableBlocks['steppable']['total']\
                                else  0
                        else:
                            self.y += 1\
                                    if self.y<s.y and DRP['room'][self.y+1][self.x]["id"]\
                                    in s.monsterInteractableBlocks['steppable']['total']\
                                else -1\
                                    if self.y>s.y and DRP['room'][self.y-1][self.x]["id"]\
                                    in s.monsterInteractableBlocks['steppable']['total']\
                                else  0

                        super().step(bfy, bfx)

            DRP['room'][self.y][self.x] = obj(
                '-be', str(self.id),
                block  =iset(self.icon),
                hashKey=self.hashKey
            )

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

        if s.sanjibaMode: self.coolTimes.divideHalf(self.coolTimes.modeException)

    def start(self, setHp:int, setAtk:int, Dy:int, Dx:int, y:int, x:int) -> None: super().start(setHp, setAtk, Dy, Dx, y, x)

    def blink(self, DRP) -> None:
        DRP['room'][self.y][self.x] = obj(
            '-be', '-1',
            block  =iset(f"{cc['fg']['F']}{self.icon}{cc['end']}"),
            hashKey=self.hashKey
        )
        time.sleep(self.coolTimes.blink)

        DRP['room'][self.y][self.x] = obj(
            '-be', str(self.id),
            block  =iset(self.icon),
            hashKey=self.hashKey
        )
        time.sleep(self.coolTimes.blink)

    def targetted(self, DRP) -> None:
        for _ in range(3): self.blink(DRP)

    def explosion(self, DRP) -> None:
        expPs = [
            [self.y-1,self.x  ],
            [self.y+1,self.x  ],
            [self.y  ,self.x-1],
            [self.y  ,self.x+1]
        ]

        DRP['room'][self.y][self.x] = obj(
            '-bb', '-1', block=f"{cc['fg']['F']}X {cc['end']}")
        particle = f"{cc['fg']['F']}. {cc['end']}"
            
        for expP in expPs:
            if DRP['room'][expP[0]][expP[1]]["id"] in s.interactableBlocks["explodable"]:
                DRP['room'][expP[0]][expP[1]] = obj(
                   '-bb', '-1',
                   block=particle
                )
               
            elif DRP['room'][expP[0]][expP[1]]["id"] in [300, 301]:
                s.steppedBlock = obj(
                    '-bb', '900',
                    block=f"{cc['fg']['G1']}{escapeAnsi(DRP['room'][expP[0]][expP[1]]['block'])}{cc['end']}"
                )

        time.sleep(self.coolTimes.explosion)
            
        for expP in expPs:
            if DRP['room'][expP[0]][expP[1]] == obj('-bb', '-1', block=particle):
                DRP['room'][expP[0]][expP[1]] = obj(
                    '-bb', '900',
                    block=f"{cc['fg']['G1']}. {cc['end']}"
                )
            
        self.icon = iset(choice(['×', 'x', 'X']))
        self.hp   = 0

    def move(self) -> None:
        DRP = s.Dungeon[self.Dy][self.Dx]
            
        if not self.coolTime:
            self.coolTime = self.coolTimes.turnEnd
            if self.isFocused:
                if [self.Dy, self.Dx] != [s.Dy, s.Dx]: self.isFocused = False; return

                if self.hp > 0:
                    if 300 in [
                        DRP['room'][self.y-1][self.x]  ["id"],
                        DRP['room'][self.y+1][self.x]  ["id"],
                        DRP['room'][self.y]  [self.x-1]["id"],
                        DRP['room'][self.y]  [self.x+1]["id"]
                    ]:
                        self.targetted(DRP)

                        if 300 in [
                            DRP['room'][self.y-1][self.x]  ["id"],
                            DRP['room'][self.y+1][self.x]  ["id"],
                            DRP['room'][self.y]  [self.x-1]["id"],
                            DRP['room'][self.y]  [self.x+1]["id"]
                        ]:
                            play("entity", "enemy", "resentment", "explosion")
                            self.attack([0, 0], "폭발")
                            
                            self.explosion(DRP)
                            self.xpMultiplier = 2
                            if randrange(0,2): say(choice(TIOTA))

                        else: DRP['room'][self.y][self.x] = obj(
                            '-be', str(self.id),
                            block  =iset(self.icon),
                            hashKey=self.hashKey
                        )

                    else: self.blink(DRP)

        else: super().wait()

class Craving(Enemy): ... # TODO: 욕망의 항아리