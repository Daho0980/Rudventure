import random, time
from   pynput.keyboard                       import Key
from   Packages.lib                          import stages
from   Packages.lib.data                     import rooms, status
from   Packages.lib.modules                 import logger
from   Packages.lib.system.globalFunc.system import xpSystem
from   Packages.lib.system.globalFunc.sound  import play

S1, s, r = stages, status, rooms
dfCrack  = 0

def boxEvent():
    if s.hp < s.Mhp: s.hp += random.randrange(1, 2)
    s.hunger += 25

class player:
    def set():
        s.hp = 10
        s.Mhp = s.hp
        s.df = 5
        s.Mdf = s.df

    def start(Dy, Dx, y, x):
        s.Dungeon[Dy][Dx]['room'][y][x] = s.p1
        s.Dy, s.Dx, s.y, s.x            = Dy, Dx, y, x

    def damage(block="?"):
        if s.df > 0: s.df -= 1
        else       : s.hp -= 1
        logger.addLog(f"{s.lightName}이(가) {s.markdown(1)}[ {block} ]{s.colors['end']} 에 의해 상처입었습니다 {s.colors['R']}(남은 체력 : {s.hp}){s.colors['end']} {s.colors['B']}(남은 방어력 : {s.df}){s.colors['end']}")
        
    def orbEvent(Size, Type):
        sizeIndex = ["bigOne", "smallOne"].index(Size)
        typeIndex = ["hp", "def", "atk", "hunger", "exp"].index(Type)
        data = [
            [
            "s.hp += 3",
            "s.df += 3",
            "s.atk += 2",
            "s.hunger += 50",
            "xpSystem.getXP(3)"
            ],
            [
            "s.hp += 1",
            "s.df += 1",
            "s.atk += 1",
            "s.hunger += 25",
            "xpSystem.getXP(1)"
            ]
        ]
        var = {"s":s, "xpSystem":xpSystem}
        exec(data[sizeIndex][typeIndex], var)

    def move(Dir, Int): 
        enemies = [s.enemies["snippets"]["pain"], s.enemies["snippets"]["unrest"]]
        roomGrid = s.Dungeon[s.Dy][s.Dx]['room']

        if s.df > 0: s.dfCrack = 0
        bfy, bfx   = s.y, s.x
        bfDy, bfDx = s.Dy, s.Dx

        match Dir:
            case Key.up   : s.y -= Int
            case Key.down : s.y += Int
            case Key.left : s.x -= Int
            case Key.right: s.x += Int
        s.hunger -= 1
        sound     = "move"

        if roomGrid[s.y][s.x] in [s.wall, s.fakeFloor]:
            player.damage(roomGrid[s.y][s.x])
            s.y, s.x   = bfy, bfx
            s.Dy, s.Dx = bfDy, bfDx
            if s.df <= 0 and s.dfCrack <= 0:
                sound = "crack"
                logger.addLog(f"{s.colors['B']}방어구{s.colors['end']}가 부서졌습니다!")
                s.dfCrack = 1
            else                           : sound = "Hit"

        elif roomGrid[s.y][s.x] in enemies:
            sound = "slash"

            s.Wanted   = [eval(f"{s.y}"), eval(f"{s.x}")]
            time.sleep(0.01)
            s.Wanted   = []

            s.y, s.x   = bfy, bfx
            s.Dy, s.Dx = bfDy, bfDx

        # elif s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] == s.item:
        #     boxEvent()
        #     sound = "get_item"
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
            # v|y, x|    U to D   D to U  L to R   R to L
            resetYX   = [[11, 6], [1, 6], [6, 11], [6, 1]]
            resetType = None

            if pos[0] == 1   : s.Dy -= 1; resetType = 0
            elif pos[0] == -1: s.Dy += 1; resetType = 1
            elif pos[1] == 1 : s.Dx -= 1; resetType = 2
            elif pos[1] == -1: s.Dx += 1; resetType = 3
            s.y, s.x = resetYX[resetType][0], resetYX[resetType][1]

            s.Dungeon[s.Dy][s.Dx]['isPlayerVisited'] = 2
            roomPos = [[s.Dy-1 if s.Dy>0 else s.Dy, s.Dx], [s.Dy, s.Dx+1 if s.Dx<len(s.Dungeon[0])-1 else s.Dx], [s.Dy+1 if s.Dy<len(s.Dungeon)-1 else s.Dy, s.Dx], [s.Dy, s.Dx-1 if s.Dx>0 else s.Dx]]
            for i in range(len(roomPos)):
                if len(s.Dungeon[roomPos[i][0]][roomPos[i][1]]) > 0 and s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] == 0 and list(s.Dungeon[s.Dy][s.Dx]['doorPos'].values())[i] == 1:
                    s.Dungeon[roomPos[i][0]][roomPos[i][1]]['isPlayerVisited'] = 1
            s.Dungeon[bfDy][bfDx]['isPlayerHere'] = False
            s.Dungeon[s.Dy][s.Dx]['isPlayerHere'] = True

        elif roomGrid[s.y][s.x] == ' ': s.hp, s.df = 0, 0

        elif roomGrid[s.y][s.x] == s.box:
            sound  = "move_box"
            cx, cy = 0, 0
            Type   = 0
            if Dir in [Key.up, Key.down]:
                if Dir == Key.up    : cy = s.y - Int
                elif Dir == Key.down: cy = s.y + Int

            elif Dir in [Key.left, Key.right]:
                Type = 1
                if Dir == Key.left   : cx = s.x - Int
                elif Dir == Key.right: cx = s.x + Int

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
            logger.addLog(f"{s.lightName}이(가) {s.colors['B']}말랑이{s.colors['end']}를 만졌습니다 (말랑)")

        s.Dungeon[bfDy][bfDx]['room'][bfy][bfx] = s.floor
        s.Dungeon[s.Dy][s.Dx]['room'][s.y][s.x] = s.p1
        play(sound)