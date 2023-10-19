import time
import curses
import random
from   Packages.lib.data                     import rooms, status
from   Packages.lib.modules                  import logger
from   Packages.lib.system.globalFunc.system import xpSystem
from   Packages.lib.system.globalFunc.sound  import play

s, r     = status, rooms
cc       = s.cColors

class player:
    def set():
        s.hp     = 10
        s.Mhp    = s.hp
        s.df     = 5
        s.Mdf    = s.df
        s.atk    = 1
        s.hunger = 500
        s.Mxp    = 10

    def start(Dy, Dx, y, x):
        s.Dungeon[Dy][Dx]['room'][y][x] = s.p1
        s.Dy, s.Dx, s.y, s.x            = Dy, Dx, y, x

    def damage(block="?"):
        if s.df > 0: s.df -= 1
        else       : s.hp -= 1
        logger.addLog(f"{s.lightName}이(가) [ {block} ] 에 의해 상처입었습니다")

    def itemEvent():
        typeIndex = None
        percent   = random.randrange(1, 101)

        if   percent > 0  and percent <= 45: typeIndex = "hunger"
        elif percent > 45 and percent <= 70: typeIndex = "hp"
        elif percent > 70 and percent <= 80: typeIndex = "def"
        elif percent > 80 and percent <= 85: typeIndex = "atk"
        else: typeIndex = "exp"

        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = s.orbs['type'][typeIndex][1]
        
    def orbEvent(Size, Type):
        sizeIndex = ["bigOne", "smallOne"].index(Size)
        typeIndex = ["hp", "def", "atk", "hunger", "exp"].index(Type)
        orbData   = [
            [3,   1],
            [3,   1],
            [2,   1],
            [50, 25],
            [5,   1]
        ]

        point = orbData[typeIndex][sizeIndex]
        match typeIndex:
            case 0: s.hp = s.Mhp if s.hp+point > s.Mhp else s.hp+point
            case 1: s.df = s.Mdf if s.df+point > s.Mdf else s.df+point

            case 2: s.atk    += point
            case 3: s.hunger += point

            case 4: xpSystem.getXP(point)


    def move(Dir, Int): 
        enemies  = [s.enemies["snippets"]["pain"], s.enemies["snippets"]["unrest"]]
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

        if roomGrid[s.y][s.x] in [s.wall, s.fakeFloor]:
            player.damage(roomGrid[s.y][s.x])

            s.y, s.x   = bfy, bfx
            s.Dy, s.Dx = bfDy, bfDx

            if s.df <= 0 and s.dfCrack <= 0:
                sound     = "crack"
                s.dfCrack = 1
                logger.addLog(f"{cc['fg']['B1']}방어구{cc['end']}가 부서졌습니다!")
            else: sound = "Hit"

        elif roomGrid[s.y][s.x] in enemies:
            sound = "slash"

            s.hitPos.append([s.y, s.x])
            time.sleep(0.001)
            s.hitPos.remove([s.y, s.x])

            s.y,  s.x  = bfy,  bfx
            s.Dy, s.Dx = bfDy, bfDx

        elif s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] == s.item:
            sound = "move_box"
            player.itemEvent()
            s.y, s.x = bfy, bfx

        elif roomGrid[s.y][s.x] in s.orbs["size"]["smallOne"] or roomGrid[s.y][s.x] in s.orbs["size"]["bigOne"]:
            sound = "get_item"
            block = roomGrid[s.y][s.x]
            sizeK, typeK = ["bigOne", "smallOne"], ["hp", "def", "atk", "hunger", "exp"]
            sizeD, typeD = None, None

            for i in sizeK:
                if block in s.orbs['size'][i]:
                    sizeD = i
                    for j in typeK:
                        if block in s.orbs['type'][j]: typeD = j; break
                    break
            player.orbEvent(sizeD, typeD)

        elif roomGrid[s.y][s.x] == s.R:
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = s.R
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

        elif roomGrid[s.y][s.x] == ' ': s.hp, s.df = 0, 0

        elif roomGrid[s.y][s.x] == s.box:
            sound  = "move_box"
            cx, cy = 0, 0
            Type   = 1 if Dir in [curses.KEY_LEFT, curses.KEY_RIGHT] else 0
            match Dir:
                case curses.KEY_UP:    cy = s.y - Int
                case curses.KEY_DOWN:  cy = s.y + Int
                case curses.KEY_LEFT:  cx = s.x - Int
                case curses.KEY_RIGHT: cx = s.x + Int

            positions = [[cy, s.x], [s.y, cx]]
            if roomGrid[positions[Type][0]][positions[Type][1]] in [s.wall, s.enemies["snippets"]["pain"], s.R, s.boss, s.box, s.fakeFloor, s.goal, s.squishy]:
                s.y, s.x   = bfy, bfx
                s.Dy, s.Dx = bfDy, bfDx
            else: s.Dungeon[s.Dy][s.Dx]['room'][positions[Type][0]][positions[Type][1]] = s.box

        elif roomGrid[s.y][s.x] in s.squishy:
            sound = "squish"
            s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = s.squishy[0] if roomGrid[s.y][s.x] == s.squishy[1] else s.squishy[0]

            s.y, s.x   = bfy, bfx
            s.Dy, s.Dx = bfDy, bfDx
            logger.addLog(f"{s.lightName}이(가) {cc['fg']['B1']}말랑이{cc['end']}를 만졌습니다 (말랑)")

        s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = s.floor
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = s.p1
        play(sound)