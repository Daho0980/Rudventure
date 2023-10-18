import random, time
from   Packages.lib                         import player
from   Packages.lib.data                    import status
from   Packages.lib.data.status             import entities
from   Packages.lib.modules.logger          import addLog
from   Packages.lib.system.globalFunc.sound import play

s, p = status, player.player
cc   = s.cColors

class enemy:
    def __init__(self, name, icon):
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

    def start(self, sethp, setAtk, Dy, Dx, y, x):
        self.hp          = sethp
        self.atk         = setAtk
        self.Dy, self.Dx = Dy, Dx
        nowDRP           = s.Dungeon[self.Dy][self.Dx]

        if isinstance(y, list) and isinstance(x, list):
            while 1:
                sY  = random.randrange(1,len(nowDRP['room'])-1)
                sX  = random.randrange(1,len(nowDRP['room'][0])-1)
                if s.Dungeon[Dy][Dx]['room'][sY][sX] in [
                    s.R,
                    s.wall,
                    s.goal,
                    s.enemies["snippets"]["pain"],
                    s.boss,
                    s.item,
                    s.p1,
                    s.box,
                    s.boxMark
                    ]:
                    continue
                else:
                    self.x, self.y = sX, sY
                    break
        else:
            self.Dy, self.Dx = Dy, Dx
            self.y, self.x   = y, x

    def pDamage(self):
        sound = f'enemy_Hit'
        if s.df > 0:
            s.df -= self.atk
            if s.df < 0                    : s.hp += s.df
            if round(s.df) < 0             : s.df = 0
            if s.df == 0 and s.dfCrack <= 0:
                sound     = f'crack'
                addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")
                s.dfCrack = 1
        else: s.hp -= self.atk

        addLog(f"{s.lightName}이(가) {cc['fg']['F']}{self.name}{cc['end']}({self.icon}) 에 의해 {cc['fg']['R']}{self.atk}{cc['end']}만큼의 피해를 입었습니다!")
        play(sound)
        return

    def move(self):
        nowDRP = s.Dungeon[self.Dy][self.Dx]
        if len(s.hitPos) > 0 and [self.y, self.x] in s.hitPos:
            self.hp -= s.atk
            if self.hp > 0: addLog(f"{cc['fg']['F']}{self.name}{cc['end']}이(가) {cc['fg']['L']}{s.atk}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}")

        if self.coolTime == 0:
            self.coolTime = random.randrange(60, 81)
            if self.stepped not in s.stepableBlocks: self.stepped = s.floor
            elif nowDRP['room'][self.y][self.x] in s.stepableBlocks and nowDRP['room'][self.y][self.x] not in [s.item, s.boxMark]:
                self.stepped = s.stepableBlocks[s.stepableBlocks.index(nowDRP['room'][self.y][self.x])]
            
            bfx, bfy = self.x, self.y
            if self.hp > 0:
                exPos = [
                    nowDRP['room'][self.y-1][self.x],
                    nowDRP['room'][self.y+1][self.x],
                    nowDRP['room'][self.y][self.x-1],
                    nowDRP['room'][self.y][self.x+1]
                ]

                if s.p1 in exPos:
                    enemy.pDamage(self)
                else:
                    while 1:
                        if random.randrange(1,3000) == 1215: play(f"growl")
                        enemyMove = random.randrange(1,4)
                        Rx, Ry    = random.randrange(-1,2), random.randrange(-1,2)

                        match enemyMove:
                            case 1:
                                if self.x + Rx > len(nowDRP['room'][self.y])-1: continue
                                self.x += Rx
                            case 2:
                                if self.y + Ry > len(nowDRP['room'])-1: continue
                                self.y += Ry

                        if nowDRP['room'][self.y][self.x] not in s.stepableBlocks:
                            self.x, self.y = bfx, bfy
                            continue

                        if nowDRP['room'][self.y][self.x] == s.p1: enemy.pDamage(self)
                        break
                s.Dungeon[self.Dy][self.Dx]['room'][bfy][bfx]       = s.stepableBlocks[s.stepableBlocks.index(self.stepped)]
                s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = self.icon
        else:
            self.coolTime -= 1
            time.sleep(0.01)


class observer(enemy):
    def __init__(self, name, icon): super().__init__(name, icon)

    def start(self, sethp, setAtk, Dy, Dx, y, x): super().start(sethp, setAtk, Dy, Dx, y, x)

    def move(self):
        nowDRP = s.Dungeon[self.Dy][self.Dx]

        def Targetted():
            for _ in range(2):
                nowDRP['room'][self.y][self.x] = f"{cc['fg']['R']}{self.icon}{cc['end']}"; time.sleep(0.1)
                nowDRP['room'][self.y][self.x] = self.icon; time.sleep(0.1)

        if len(s.hitPos) > 0 and [self.y, self.x] in s.hitPos:
            self.hp -= s.atk
            if self.hp > 0: addLog(f"{cc['fg']['F']}{self.name}{cc['end']}이(가) {cc['fg']['L']}{s.atk}{cc['end']}만큼의 피해를 입었습니다! {cc['fg']['R']}(체력 : {self.hp}){cc['end']}")

        if self.coolTime == 0:
            self.coolTime = random.randrange(40, 61)
            if self.stepped not in s.stepableBlocks: self.stepped = s.floor
            elif nowDRP['room'][self.y][self.x] in s.stepableBlocks and\
                nowDRP['room'][self.y][self.x] not in [s.item, s.boxMark]:
                self.stepped = s.stepableBlocks[s.stepableBlocks.index(nowDRP['room'][self.y][self.x])]

            bfx, bfy = self.x, self.y
            if self.hp > 0:
                Moves, Moves1 = ["+=", "-="], ["+", "-"]
                canBreak      = [s.item, s.floor]
                a             = 0

                if self.Dy == s.Dy and self.Dx == s.Dx and (self.x == s.x or self.y == s.y):
                    play(f"TargetLocked")
                    if self.x == s.x:
                        Targetted()
                        if self.y < s.y: a = 0
                        else           : a = 1

                        while 1:
                            if nowDRP['room'][eval(f"self.y{Moves1[a]}1")][self.x] == s.p1: enemy.pDamage(self)
                            if nowDRP['room'][eval(f"self.y{Moves1[a]}1")][self.x] not in canBreak: break
                            nowDRP['room'][self.y][self.x] = s.floor
                            exec(f"self.y{Moves[a]}1"); nowDRP['room'][self.y][self.x] = self.icon
                            time.sleep(0.1)

                    elif self.y == s.y:
                        Targetted()
                        if self.x < s.x: a = 0
                        else           : a = 1

                        while 1:
                            if nowDRP['room'][self.y][eval(f"self.x{Moves1[a]}1")] == s.p1: enemy.pDamage(self)
                            if nowDRP['room'][self.y][eval(f"self.x{Moves1[a]}1")] not in canBreak: break
                            nowDRP['room'][self.y][self.x] = s.floor
                            exec(f"self.x{Moves[a]}1"); nowDRP['room'][self.y][self.x] = self.icon
                            time.sleep(0.1)
                else:
                    bfx, bfy = self.x, self.y
                    if random.randrange(1,3) == 1:
                        if   self.x < s.x and nowDRP['room'][self.y][self.x+1] in s.stepableBlocks: self.x += 1
                        elif self.x > s.x and nowDRP['room'][self.y][self.x-1] in s.stepableBlocks: self.x -= 1
                    else:
                        if   self.y < s.y and nowDRP['room'][self.y+1][self.x] in s.stepableBlocks: self.y += 1
                        elif self.y > s.y and nowDRP['room'][self.y-1][self.x] in s.stepableBlocks: self.y -= 1
                    nowDRP['room'][bfy][bfx]       = s.floor
                    nowDRP['room'][self.y][self.x] = self.icon
        else:
            self.coolTime -= 1
            time.sleep(0.01)
    