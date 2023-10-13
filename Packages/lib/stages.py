import copy
import random
from   Packages.lib                   import player
from   Packages.lib.data              import rooms, status
from   Packages.lib.system.globalFunc import entity, system

player, p, r = status, player, rooms
ent, sys = entity, system

class stages:
    def stage(stage):
        player.steppedBlock = '.'
        eHp = 4 + stage
        if stage == 0:
            player.stageName = "안녕 세상"
            player.room      = copy.deepcopy(r.field)
            player.roomName  = "field"
            p.player.start(1, 1)
            ent.addEntity(0, eHp)
            for Item in range(2): sys.placeRandomBlock(player.room, player.item, [1, 9], [1, 9], [player.p1, player.enemies["snippets"]["pain"], player.wall])
            r.room_1[3][3] = player.goal

        elif stage == 1:
            player.stageName = "미로"
            player.room      = copy.deepcopy(r.maze_big)
            player.roomName  = "maze_big"
            p.player.start(0, 9)
            for Monster in range(3): ent.addEntity(0, eHp)
            for Item in range(4)   : sys.placeRandomBlock(player.room, player.item, [1, 20], [1, 20], [player.p1, player.enemies["snippets"]["pain"], player.wall])
            player.room[20][11] = player.goal

        elif stage == 2:
            player.stageName = "움직이는 상자"
            player.room      = copy.deepcopy(r.field)
            player.roomName  = "field"
            p.player.start(8, 4)
            for addMark in range(2):
                while True:
                    Ry, Rx = random.randrange(1, 9), random.randrange(1, 9)
                    if player.room[Ry][Rx] in [player.p1, player.boxMark, player.box] or (Ry == 4 and Rx == 1): continue
                    player.room[Ry][Rx] = player.boxMark
                    break
                if addMark == 1: player.btn1Y, player.btn1X = Ry, Rx
                else           : player.btnY, player.btnX = Ry, Rx
            for addBox in range(2): sys.placeRandomBlock(player.room, player.box, [2, 8], [2, 8], [player.p1, player.boxMark, player.box])

        elif stage == 3:
            player.stageName               = "기억의 길"
            player.room                    = copy.deepcopy(r.invisible_walls1)
            player.roomName                = "invisible_walls1"
            r.invisible_walls2[9][14] = player.goal
            p.player.start(1, 1)

        elif stage == 4:
            player.stageName = "감시자"
            player.room      = copy.deepcopy(r.bossStage)
            player.roomName  = "bossStage"
            p.player.start(14, 7)
            ent.addEntity(1, 25, 1, 9)
            ent.addEntity(1, 25, 1, 5)

        elif stage == 5:
            player.stageName  = "Shelter"
            player.room       = copy.deepcopy(r.shelter)
            player.roomName   = "shelter"
            player.room[2][3] = player.squishy[0]
            p.player.start(2, 2)
