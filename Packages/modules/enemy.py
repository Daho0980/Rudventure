import random, time
from   Packages.modules         import states, player
from   Packages.globalFunctions import play
from   Packages.modules.states  import entities

s, p = states, player
onoPoint = [s.R, s.wall, s.goal]

class enemy:
    def __init__(self, y, x, hp, name):
        global entities
        self.y    = y
        self.x    = x
        self.hp   = hp
        entities.append(name)

    def start(self, sethp):
        self.hp = sethp
        while True:
            sX  = random.randrange(1,len(s.room)-1)
            sY  = random.randrange(1,len(s.room)-1)
            CEZ = [s.p1, s.R, s.wall, s.item, s.goal]
            if s.room[sY][sX] in CEZ: continue
            else:
                self.x, self.y = sX, sY
                s.room[self.y][self.x] = s.e
                break

    def bossStart(self, sethp, x, y):
        self.hp                = sethp
        self.x                 = x
        self.y                 = y
        s.room[self.y][self.x] = s.boss

    def pDamage(damage):
        sound = f'{s.TFP}sounds{s.s}enemy_Hit.wav'
        if s.df > 0:
            s.df -= damage
            if s.df < 0: s.hp += s.df
            s.df = round(s.df)
            if s.df == 0 and s.dfCrack <= 0:
                sound     = f'{s.TFP}sounds{s.s}crack.wav'
                s.dfCrack = 1
        else: s.hp -= damage
        play(sound)

    def move(self):
        global onoPoint

        bfx, bfy = self.x, self.y
        if self.hp > 0:
            if s.p1 in [eval("s.room[self.y-1][self.x]"), eval("s.room[self.y+1][self.x]"), eval("s.room[self.y][self.x-1]"), eval("s.room[self.y][self.x+1]")]:
                enemy.pDamage(1)
                if random.randrange(1,6) == 3: play(f"{s.TFP}sounds{s.s}growl.wav")

                if s.room[self.y-1][self.x] == s.p1: self.y -= 1
                elif s.room[self.y+1][self.x] == s.p1: self.y += 1
                elif s.room[self.y][self.x-1] == s.p1: self.x -= 1
                elif s.room[self.y][self.x+1] == s.p1: self.x += 1
            else:
                while True:
                    if random.randrange(1,25) == 3: play(f"{s.TFP}sounds{s.s}growl.wav")
                    enemyMove = random.randrange(1,3)
                    Rx        = random.randrange(-1,2)
                    Ry        = random.randrange(-1,2)
                    if enemyMove == 1:
                        if self.x + Rx > len(s.room[self.x])-1: continue
                        self.x += Rx
                    elif enemyMove == 2:
                        if self.y + Ry > len(s.room)-1: continue
                        self.y += Ry
                    if s.room[self.y][self.x] in onoPoint:
                        self.x, self.y = bfx, bfy
                        continue
                    if s.room[self.y][self.x] == s.p1: enemy.pDamage(1)
                    break
            s.room[bfy][bfx] = s.floor
            s.room[self.y][self.x] = s.e
        time.sleep(0.3)

    def bossMove(self):
        global onoPoint

        if self.hp > 0:
            Moves, Moves1 = ["+=", "-="], ["+", "-"]
            a = 0
            if self.x == s.x or self.y == s.y:
                play(f"{s.TFP}sounds{s.s}TargetLocked.wav")
                if self.x == s.x:
                    for i in range(2):
                        s.room[self.y][self.x] = f"{s.colors['R']}{s.boss}{s.colors['end']}"
                        time.sleep(0.1)
                        s.room[self.y][self.x] = s.boss
                    if self.y < s.y: a = 0
                    else: a = 1
                    while True:
                        if self.hp > 0:
                            if s.room[eval(f"self.y{Moves1[a]}1")][self.x] in onoPoint: break
                            elif s.room[eval(f"self.y{Moves1[a]}1")][self.x] == s.p1: enemy.pDamage(2)
                            s.room[self.y][self.x] = s.floor
                            exec(f"self.y{Moves[a]}1"); s.room[self.y][self.x] = s.boss
                            time.sleep(0.1)
                        else: break

                elif self.y == s.y:
                    for i in range(2):
                        s.room[self.y][self.x] = f"{s.colors['R']}{s.boss}{s.colors['end']}"
                        time.sleep(0.2)
                        s.room[self.y][self.x] = s.boss
                    if self.x < s.x: a = 0
                    else: a = 1
                    while True:
                        if self.hp > 0:
                            if s.room[self.y][eval(f"self.x{Moves1[a]}1")] in onoPoint: break
                            elif s.room[self.y][eval(f"self.x{Moves1[a]}1")] == s.p1: enemy.pDamage(2)
                            s.room[self.y][self.x] = s.floor
                            exec(f"self.x{Moves[a]}1"); s.room[self.y][self.x] = s.boss
                            time.sleep(0.1)
                        else: break

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
            time.sleep(0.1)

    def __del__(self):
        1+1

class boss(enemy):
    def __init__(self, x, y, hp, name):
        super(boss, self).__init__()

    def move(self):
        global onoPoint

        if self.hp > 0:
            Moves, Moves1 = ["+=", "-="], ["+", "-"]
            a = 0
            if self.x == s.x or self.y == s.y:
                play(f"{s.TFP}sounds{s.s}TargetLocked.wav")
                if self.x == s.x:
                    for i in range(2):
                        s.room[self.y][self.x] = f"{s.colors['R']}{s.boss}{s.colors['end']}"
                        time.sleep(0.1)
                        s.room[self.y][self.x] = s.boss
                    if self.y < s.y: a = 0
                    else: a = 1
                    while True:
                        if self.hp > 0:
                            if s.room[eval(f"self.y{Moves1[a]}1")][self.x] in onoPoint: break
                            elif s.room[eval(f"self.y{Moves1[a]}1")][self.x] == s.p1: enemy.pDamage(2)
                            s.room[self.y][self.x] = s.floor
                            exec(f"self.y{Moves[a]}1"); s.room[self.y][self.x] = s.boss
                            time.sleep(0.1)
                        else: break

                elif self.y == s.y:
                    for i in range(2):
                        s.room[self.y][self.x] = f"{s.colors['R']}{s.boss}{s.colors['end']}"
                        time.sleep(0.2)
                        s.room[self.y][self.x] = s.boss
                    if self.x < s.x: a = 0
                    else: a = 1
                    while True:
                        if self.hp > 0:
                            if s.room[self.y][eval(f"self.x{Moves1[a]}1")] in onoPoint: break
                            elif s.room[self.y][eval(f"self.x{Moves1[a]}1")] == s.p1: enemy.pDamage(2)
                            s.room[self.y][self.x] = s.floor
                            exec(f"self.x{Moves[a]}1"); s.room[self.y][self.x] = s.boss
                            time.sleep(0.1)
                        else: break

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
            time.sleep(0.1)

    def start(self, sethp, x, y):
        self.hp                = sethp
        self.x                 = x
        self.y                 = y
        s.room[self.y][self.x] = s.boss
    