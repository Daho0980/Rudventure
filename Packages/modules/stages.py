import random
from   Packages.modules import states, rooms, enemy, player
from   Packages import globalFunctions

s, p, r = states, player, rooms
gbf = globalFunctions
e = enemy.enemy(0, 0, 0)
e1 = enemy.enemy(0, 0, 0)
boss = enemy.enemy(0, 0, 0)

class stages:
    def stage(stage):
        s.steppedBlock = '.'
        eHp = 4 + stage
        if stage == 0:
            s.room = r.field[:]
            s.stageName = "안녕 세상"
            p.player.start(1, 1)
            gbf.addEntity(0, eHp)
            for i in range(2):
                while True:
                    Rx = random.randrange(1,10)
                    Ry = random.randrange(1,10)
                    if s.room[Ry][Rx] == s.p1 or\
                    s.room[Ry][Rx] == s.e or\
                    s.room[Ry][Rx] == '◼':
                        continue
                    else:
                        s.room[Ry][Rx] = '◘'
                        break
            r.room_1[3][3] = s.goal
        elif stage == 1:
            s.stageName = "미로"
            s.room = r.maze_big[:]
            p.player.start(9, 0)
            gbf.addEntity(0, eHp)
            gbf.addEntity(0, eHp)
            for i in range(4):
                while True:
                    Rx = random.randrange(0,20)
                    Ry = random.randrange(0,20)
                    if s.room[Ry][Rx] == s.p1 or\
                    s.room[Ry][Rx] == s.e or\
                    s.room[Ry][Rx] == '◼':
                        continue
                    else:
                        s.room[Ry][Rx] = '◘'
                        break
            s.room[20][11] = s.goal
        elif stage == 2:
            s.stageName = "움직이는 상자"
            s.room = r.field[:]
            s.room[0][1] = s.room[0][2] = s.room[0][3] = '◼'
            p.player.start(4, 8)
            for i in range(2):
                while True:
                    Rx = random.randrange(0, 9)
                    Ry = random.randrange(0, 9)
                    if s.room[Ry][Rx] == s.p1 or\
                    s.room[Ry][Rx] == '◼' or\
                    s.room[Ry][Rx] == '☒' or\
                    (Ry == 4 and Rx == 1):
                        continue
                    else:
                        s.room[Ry][Rx] = '✘'
                        if i == 0:
                            s.btnY = Ry
                            s.btnX = Rx
                        elif i == 1:
                            s.btn1Y = Ry
                            s.btn1X = Rx
                        break
                while True:
                    Rx = random.randrange(2, 7)
                    Ry = random.randrange(2, 7)
                    if s.room[Ry][Rx] == s.p1 or\
                    s.room[Ry][Rx] == '◼' or\
                    s.room[Ry][Rx] == '✘':
                        continue
                    else:
                        s.room[Ry][Rx] = '☒'
                        break
            if r.field.count('☒') == 1:
                while True:
                    Rx = random.randrange(2, 7)
                    Ry = random.randrange(2, 7)
                    if s.room[Ry][Rx] == s.p1 or\
                    s.room[Ry][Rx] == '◼' or\
                    s.room[Ry][Rx] == '✘':
                        continue
                    else:
                        s.room[Ry][Rx] = '☒'
                        break
        elif stage == 3:
            s.stageName = "기억의 길"
            s.room = r.invisible_walls1
            r.invisible_walls2[9][14] = s.goal
            p.player.start(1, 1)
        elif stage == 4:
            s.stageName = "감시자"
            s.room = r.bossStage
            p.player.start(7, 14)
            gbf.addEntity(1, 15, 1, 9)
            gbf.addEntity(1, 15, 1, 5)
        elif stage == 5:
            s.stageName = "Shelter"
            s.room = r.shelter
            p.player.start(2, 2)
