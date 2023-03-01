import random
from   Packages.modules import status, rooms, player
from   Packages import globalFunctions

s, p, r = status, player, rooms
gbf = globalFunctions

class stages:
    def stage(stage):
        s.steppedBlock = '.'
        eHp = 4 + stage
        if stage == 0:
            s.room = r.field[:]
            s.stageName = "안녕 세상"
            p.player.start(1, 1)
            gbf.addEntity(0, eHp)
            for Item in range(2): gbf.placeRandomBlock(s.room, s.item, [1, 9], [1, 9], [s.p1, s.e, s.wall])
            r.room_1[3][3] = s.goal
        elif stage == 1:
            s.stageName = "미로"
            s.room = r.maze_big[:]
            p.player.start(9, 0)
            for Monster in range(3): gbf.addEntity(0, eHp)
            for Item in range(4): gbf.placeRandomBlock(s.room, s.item, [1, 20], [1, 20], [s.p1, s.e, s.wall])
            s.room[20][11] = s.goal
        elif stage == 2:
            s.stageName = "움직이는 상자"
            s.room = r.field[:]
            s.room[0][1], s.room[0][2],  s.room[0][3] = s.wall, s.wall, s.wall
            s.room[1][2] = s.floor
            p.player.start(4, 8)
            for addMark in range(2):
                while True:
                    Ry, Rx = random.randrange(1, 9), random.randrange(1, 9)
                    if s.room[Ry][Rx] in [s.p1, s.boxMark, s.box] or (Ry == 4 and Rx == 1): continue
                    s.room[Ry][Rx] = s.boxMark
                    break
                if addMark == 1: s.btn1Y, s.btn1X = Ry, Rx
                else: s.btnY, s.btnX = Ry, Rx
            for addBox in range(2): gbf.placeRandomBlock(s.room, s.box, [2, 8], [2, 8], [s.p1, s.boxMark, s.box])
        elif stage == 3:
            s.stageName = "기억의 길"
            s.room = r.invisible_walls1
            r.invisible_walls2[9][14] = s.goal
            p.player.start(1, 1)
        elif stage == 4:
            s.stageName = "감시자"
            s.room = r.bossStage
            p.player.start(7, 14)
            gbf.addEntity(1, 25, 1, 9)
            gbf.addEntity(1, 25, 1, 5)
        elif stage == 5:
            s.stageName = "Shelter"
            s.room = r.shelter
            s.room[2][3] = s.squishy[0]
            p.player.start(2, 2)
