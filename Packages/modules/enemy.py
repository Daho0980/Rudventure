import random, time
from   Packages.modules         import status, player
from   Packages.globalFunctions import play
from   Packages.modules.status  import entities
from   Packages.modules.logger  import addLog

s, p = status, player
onoPoint = [s.R, s.wall, s.goal, s.e, s.boss, s.item, s.p1, s.box, s.boxMark]

class enemy:
    def __init__(self, y, x, hp, name):
        global entities
        self.y        = y
        self.x        = x
        self.hp       = hp
        self.stepped  = 0
        self.coolTime = 0
        self.name     = name

    def start(self, sethp, y, x):
        self.hp = sethp
        if isinstance(y, list) and isinstance(x, list):
            while True:
                sX  = random.randrange(1,len(s.room)-1)
                sY  = random.randrange(1,len(s.room)-1)
                if s.room[sY][sX] in onoPoint: continue
                else:
                    self.x, self.y = sX, sY
                    break
        else: self.y, self.x = y, x

    def pDamage(self, damage):
        sound = f'{s.TFP}sounds{s.s}enemy_Hit.wav'
        if s.df > 0:
            s.df -= damage
            if s.df < 0       : s.hp += s.df
            if round(s.df) < 0: s.df = 0
            if s.df == 0 and s.dfCrack <= 0:
                sound     = f'{s.TFP}sounds{s.s}crack.wav'
                s.dfCrack = 1
        else: s.hp -= damage
        play(sound)
        addLog(f"{s.lightName}이(가) {s.colors['R']}{self.name}{s.colors['end']} 에 의해 {s.colors['R']}{s.atk}{s.colors['end']}만큼의 피해를 입었습니다! {s.colors['R']}(현재 체력 : {s.hp}){s.colors['end']} {s.colors['B']}(현재 방어력 : {s.df}){s.colors['end']}")
        return

    def move(self):
        global onoPoint

        if len(s.Wanted) > 0 and s.Wanted[0] == self.y and s.Wanted[1] == self.x:
            self.hp -= s.atk
            if self.hp > 0: addLog(f"{s.colors['R']}{self.name}{s.colors['end']}이(가) {s.colors['G']}{s.atk}{s.colors['end']}만큼의 피해를 입었습니다! {s.colors['R']}(체력 : {self.hp}){s.colors['end']}")

        if self.coolTime == 0:
            self.coolTime = 70
            if self.stepped in onoPoint              : self.stepped = s.floor
            if s.room[self.y][self.x] not in onoPoint: self.stepped = s.stepableBlocks.index(s.room[self.y][self.x])
            bfx, bfy = self.x, self.y
            if self.hp > 0:
                nms   = {'s':s}
                exPos = [eval(f"s.room[{self.y-1}][{self.x}]", nms), eval(f"s.room[{self.y+1}][{self.x}]", nms), eval(f"s.room[{self.y}][{self.x-1}]", nms), eval(f"s.room[{self.y}][{self.x+1}]", nms)]
                exTen = ["self.y-=1", "self.y+=1", "self.x-=1", "self.x+=1"]
                if s.p1 in exPos:
                    enemy.pDamage(self, 1)
                    if random.randrange(1,110) == 92: play(f"{s.TFP}sounds{s.s}growl.wav")
                    exec(exTen[exPos.index(s.p1)])
                else:
                    while True:
                        if random.randrange(1,25) == 3: play(f"{s.TFP}sounds{s.s}growl.wav")
                        enemyMove = random.randrange(1,3)
                        Rx, Ry    = random.randrange(-1,2), random.randrange(-1,2)
                        if enemyMove == 1:
                            if self.x + Rx > len(s.room[self.x])-1: continue
                            self.x += Rx
                        elif enemyMove == 2:
                            if self.y + Ry > len(s.room)-1: continue
                            self.y += Ry
                        if s.room[self.y][self.x] in onoPoint:
                            self.x, self.y = bfx, bfy
                            continue
                        if s.room[self.y][self.x] == s.p1: enemy.pDamage(self, 1)
                        break
                s.room[bfy][bfx] = s.stepableBlocks[self.stepped]
                s.room[self.y][self.x] = s.e
        else:
            self.coolTime -= 1
            time.sleep(0.01)


class boss(enemy):
    def __init__(self, y, x, hp, name):
        super().__init__(y, x, hp, name)

    def start(self, sethp, y, x):
        super().start(sethp, y, x)

    def move(self):
        global onoPoint

        def Targetted():
            for i in range(2):
                s.room[self.y][self.x] = f"{s.colors['R']}𓃚{s.colors['end']}"
                time.sleep(0.1)
                s.room[self.y][self.x] = s.boss
                time.sleep(0.1)

        if len(s.Wanted) > 0 and s.Wanted[0] == self.y and s.Wanted[1] == self.x:
            self.hp -= s.atk
            if self.hp > 0: addLog(f"{s.colors['R']}{self.name}{s.colors['end']}이(가) {s.colors['G']}{s.atk}{s.colors['end']}만큼의 피해를 입었습니다! {s.colors['R']}(체력 : {self.hp}){s.colors['end']}")

        if self.coolTime == 0:
            self.coolTime = 50
            if self.stepped in onoPoint: self.stepped = s.floor
            elif s.room[self.y][self.x] in s.stepableBlocks: self.stepped = s.stepableBlocks.index(s.room[self.y][self.x])
            bfx, bfy = self.x, self.y
            if self.hp > 0:
                Moves, Moves1 = ["+=", "-="], ["+", "-"]
                canBreak      = [s.item, s.floor]
                a             = 0
                if self.x == s.x or self.y == s.y:
                    play(f"{s.TFP}sounds{s.s}TargetLocked.wav")
                    if self.x == s.x:
                        Targetted()
                        if self.y < s.y: a = 0
                        else: a = 1
                        while True:
                            if s.room[eval(f"self.y{Moves1[a]}1")][self.x] == s.p1: enemy.pDamage(self, 2)
                            if s.room[eval(f"self.y{Moves1[a]}1")][self.x] not in canBreak: break
                            s.room[self.y][self.x] = s.floor
                            exec(f"self.y{Moves[a]}1"); s.room[self.y][self.x] = s.boss
                            time.sleep(0.1)

                    elif self.y == s.y:
                        Targetted()
                        if self.x < s.x: a = 0
                        else: a = 1
                        while True:
                            if s.room[self.y][eval(f"self.x{Moves1[a]}1")] == s.p1: enemy.pDamage(self, 2)
                            if s.room[self.y][eval(f"self.x{Moves1[a]}1")] not in canBreak: break
                            s.room[self.y][self.x] = s.floor
                            exec(f"self.x{Moves[a]}1"); s.room[self.y][self.x] = s.boss
                            time.sleep(0.1)
                else:
                    bfx, bfy = self.x, self.y
                    if random.randrange(1,3) == 1:
                        if self.x < s.x and s.room[self.y][self.x+1] not in onoPoint: self.x += 1
                        elif self.x > s.x and s.room[self.y][self.x-1] not in onoPoint: self.x -= 1
                    else:
                        if self.y < s.y and s.room[self.y+1][self.x] not in onoPoint: self.y += 1
                        elif self.y > s.y and s.room[self.y-1][self.x] not in onoPoint: self.y -= 1
                    s.room[bfy][bfx] = s.floor
                    s.room[self.y][self.x] = s.boss
        else:
            self.coolTime -= 1
            time.sleep(0.01)
    