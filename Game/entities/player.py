import time
import curses
import random
from   Assets.data       import rooms, status
from   Game.core.system  import logger
from   Game.utils.system import xpSystem
from   Game.utils.sound  import play

s, r     = status, rooms
cc       = s.cColors

class player:
    def set():
        s.hp       = 10
        s.Mhp      = s.hp
        s.df       = 5
        s.Mdf      = s.df
        s.atk      = 1
        s.critRate = 10
        s.critDMG  = 10
        s.hunger   = 1000
        s.Mxp      = 10

    def start(Dy, Dx, y, x):
        s.Dungeon[Dy][Dx]['room'][y][x] = {"block":s.ids[300], "id":300}
        s.Dy, s.Dx, s.y, s.x            = Dy, Dx, y, x

    def damage(block="?"):
        if s.df > 0: s.df -= 1
        else       : s.hp -= 1
        dr = random.choice([
            "과다출혈",
            "피로 과다",
            "졸도",
            "자살",
            "우울증"
        ])
        s.DROD = [f"{s.cColors['fg']['R']}{dr}{s.cColors['end']}", 'R']
        logger.addLog(f"{s.lightName}이(가) [ {block} ] 에 의해 상처입었습니다")

    def itemEvent():
        percent   = random.randrange(1, 101)

        if   percent > 0  and percent <= 45: typeIndex = "hunger"
        elif percent > 45 and percent <= 70: typeIndex = "hp"
        elif percent > 70 and percent <= 80: typeIndex = "def"
        elif percent > 80 and percent <= 85: typeIndex = "atk"
        else: typeIndex = "exp"

        orbId = s.orbIds["type"][typeIndex][random.randrange(0, 2)]

        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = {"block" : s.ids[orbId], "id" : orbId}
        
    def orbEvent(Size, Type):
        orbData   = [
            [3,   1],
            [3,   1],
            [2,   1],
            [50, 25],
            [5,   1]
        ]

        point = orbData[Type][Size]
        match Type:
            case 0: s.hp = s.Mhp if s.hp+point > s.Mhp else s.hp+point
            case 1: s.df = s.Mdf if s.df+point > s.Mdf else s.df+point

            case 2: s.atk    += point
            case 3: s.hunger += point

            case 4: xpSystem.getXP(point)


    def move(Dir, Int): 
        enemies  = [600, 601]
        roomGrid = s.Dungeon[s.Dy][s.Dx]['room']

        if s.df > 0: s.dfCrack = 0
        bfy, bfx   = s.y, s.x
        bfDy, bfDx = s.Dy, s.Dx

        match Dir:
            case curses.KEY_UP   : s.y -= Int
            case curses.KEY_DOWN : s.y += Int
            case curses.KEY_LEFT : s.x -= Int
            case curses.KEY_RIGHT: s.x += Int

        s.hunger -= 1
        sound     = "move"

        if roomGrid[s.y][s.x]["id"] in [1, 3]:
            player.damage(roomGrid[s.y][s.x]["block"])

            s.y, s.x   = bfy, bfx
            s.Dy, s.Dx = bfDy, bfDx

            if s.df <= 0 and s.dfCrack <= 0:
                sound     = "crack"
                s.dfCrack = 1
                logger.addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")
            else: sound = "Hit"

        elif roomGrid[s.y][s.x]["id"] in enemies:
            sound = "slash"

            s.hitPos.append([s.y, s.x])
            time.sleep(0.001)
            s.hitPos.remove([s.y, s.x])

            s.y,  s.x  = bfy,  bfx
            s.Dy, s.Dx = bfDy, bfDx

        elif s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]["id"] == 4:
            sound = "move_box"
            player.itemEvent()
            s.y, s.x = bfy, bfx

        elif roomGrid[s.y][s.x]["id"] in s.orbIds["size"]["smallOne"] or roomGrid[s.y][s.x]["id"] in s.orbIds["size"]["bigOne"]:
            sound = "get_item"
            orbId = roomGrid[s.y][s.x]["id"]
            sizeD, typeD = None, None
            sizeD = 0 if orbId in s.orbIds["size"]["bigOne"] else 1
            match orbId:
                case _ if orbId in s.orbIds["type"]["hp"]:     typeD = 0
                case _ if orbId in s.orbIds["type"]["def"]:    typeD = 1
                case _ if orbId in s.orbIds["type"]["atk"]:    typeD = 2
                case _ if orbId in s.orbIds["type"]["hunger"]: typeD = 3
                case _ if orbId in s.orbIds["type"]["exp"]:    typeD = 4

            # for i in sizeK:
            #     if block in s.orbs['size'][i]:
            #         sizeD = i
            #         for j in typeK:
            #             if block in s.orbs['type'][j]: typeD = j; break
            #         break
            player.orbEvent(sizeD, typeD)

        elif roomGrid[s.y][s.x]["id"] == 2:
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x]["id"] = 2
            sound = "open"
            pos   = [bfy-s.y, bfx-s.x]
            # ┏>|y, x| : U to D   D to U  L to R   R to L
            resetYX   = [[11, 6], [1, 6], [6, 11], [6, 1]]
            resetType = None

            if pos[0]   == 1 : s.Dy -= 1; resetType = 0
            elif pos[0] == -1: s.Dy += 1; resetType = 1
            elif pos[1] == 1 : s.Dx -= 1; resetType = 2
            elif pos[1] == -1: s.Dx += 1; resetType = 3
            s.y, s.x = resetYX[resetType][0], resetYX[resetType][1]

            s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2
            roomPos = [
                [s.Dy-1 if s.Dy>0 else s.Dy, s.Dx],
                [s.Dy, s.Dx+1 if s.Dx<len(s.Dungeon[0])-1 else s.Dx],
                [s.Dy+1 if s.Dy<len(s.Dungeon)-1 else s.Dy, s.Dx],
                [s.Dy, s.Dx-1 if s.Dx>0 else s.Dx]
                ]
            
            for i in range(len(roomPos)):
                if len(s.Dungeon[roomPos[i][0]][roomPos[i][1]]) > 0 and s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] == 0 and list(s.Dungeon[s.Dy][s.Dx]['doorPos'].values())[i] == 1:
                    s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] = 1
            s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

        elif roomGrid[s.y][s.x]["id"] == 6:
            sound  = "move_box"
            cx, cy = 0, 0
            Type   = 1 if Dir in [curses.KEY_LEFT, curses.KEY_RIGHT] else 0
            match Dir:
                case curses.KEY_UP:    cy = s.y - Int
                case curses.KEY_DOWN:  cy = s.y + Int
                case curses.KEY_LEFT:  cx = s.x - Int
                case curses.KEY_RIGHT: cx = s.x + Int

            positions = [[cy, s.x], [s.y, cx]]
            if roomGrid[positions[Type][0]][positions[Type][1]]["id"] in [1, 600, 601, 2, 6, 3, 5]:
                s.y, s.x   = bfy, bfx
                s.Dy, s.Dx = bfDy, bfDx
            else: s.Dungeon[s.Dy][s.Dx]['room'][positions[Type][0]][positions[Type][1]] = {"block" : s.ids[6], "id" : 6}

        s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = {"block" : s.ids[0], "id" : 0}
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = {"block":s.ids[300], "id":300}
        play(sound)