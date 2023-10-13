"""
Global Functions 중 System 옵션

    ``placeRandomBlock`` : 방에서 블럭 등을 랜덤하게 배치할 수 있게 만든 함수
    ``upgradeStatus``    : 던전 클리어 시 나오는 스탯 업그레이드 창
"""

import curses
import random
from   Packages.lib.data                     import comments,  lockers, status
from   Packages.lib.modules                  import cSelector, logger
from   Packages.lib.system.globalFunc.entity import addEntity
from   Packages.lib.system.globalFunc.sound  import play

c, l, s  = comments, lockers, status
selector = cSelector.selector

def cinp(stdscr, text="", end='', echo=True, cursor=False):
    if echo   == True: curses.echo()
    if cursor == True: curses.curs_set(1)

    if not text.isspace():
        stdscr.addstr(f"{text}{end}")
        stdscr.refresh()
    try:    Inp = stdscr.getstr().decode("utf-8")
    except: Inp = ""

    if echo   == True: curses.noecho()
    if cursor == True: curses.curs_set(0)

    return Inp

def placeRandomBlock(block:str, y:list, x:list, allowedBlocks:list):
    """
    방에서 블럭 등을 랜덤하게 배치할 수 있게 만든 함수

    `block`(char)      : 랜덤하게 배치될 블럭의 아이콘, 무조건 기입해야 됨
    `y`(list)          : 방의 y 최솟값과 최댓값 데이터를 포함함, 무조건 기입해야 됨
        ex) `y` = `[최솟값, 최댓값]`

    `x`(list)          : 방의 x 최솟값과 최댓값 데이터를 포함함, 무조건 기입해야 됨
        ex) `x` = `[최솟값, 최댓값]`

    `disallowedBlocks`(list) : 블럭을 랜덤으로 설치 시 피해야 할 블럭 설정, 무조건 기입해야 함
    """
    while True:
        Ry, Rx = random.randrange(y[0], y[1]), random.randrange(x[0], x[1])
        if s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx] not in allowedBlocks: continue
        s.Dungeon[s.Dy][s.Dx]['room'][Ry][Rx] = block
        break

# def upgradeStatus():
#     print(f"{s.markdown([2, 3])}Enter를 한 번 눌러주세요{s.cColors['end']}")
#     selectStat = selector.main("올릴 스탯을 선택해주세요", {"체력 증가":"체력의 최대치가 1 증가합니다.", "방어력 증가":"방어력의 최대치가 1 증가합니다.","공격력 증가":"공격력이 1 상승합니다."}, [1,0,255,10], '@')
#     if selectStat == 1:
#         s.Mhp += 1
#         if s.Mhp < s.hp: s.hp += 1
#     elif selectStat == 2:
#         s.Mdf += 1
#         if s.Mdf < s.df: s.df += 1
#     else: s.atk += 1
    
#     if random.randrange(1,4) == 3:
#         if s.hp < s.Mhp and s.Mhp - s.hp == 1: s.hp += 1
#         elif s.hp < s.Mhp and s.Mhp - s.hp >= 2: s.hp += random.randrange(1,3)

#     if s.Mdf < s.df: s.df += 1

class xpSystem:
    def getXP(count:int=0):
        """
        xp를 얻을 때 발생하는 이벤트

            `count`(int) : xp 증가율
        """
        while s.xp + count > s.Mxp:
            play("levelUp")
            logger.addLog(f"{s.cColors['fg']['F']}저주가 한 층 더 깊어집니다...{s.cColors['end']}")
            s.lvl += 1
            s.Mxp += 3
            if count > s.xp: count -= s.xp
            else: count -= (s.Mxp - s.xp)
            s.xp = 0
        s.xp += count

    def loseXp(count:int=0):
        """
        xp를 잃을 때 발생하는 이벤트

            `count`(int) : xp 감소율
        """
        bfxp, bfMxp, bfLvl = s.xp, s.Mxp, s.lvl
        a = s.lvl

        while count > 0:
            if s.xp < count:
                if s.lvl == 0:
                    logger.addLog(f"{s.cColors['fg']['F']}저주{s.cColors['end']}가 부족합니다!")
                    s.xp, s.Mxp, s.lvl = bfxp, bfMxp, bfLvl
                    break

                count -= s.xp
                s.lvl -= 1
                s.Mxp -= 3
                s.xp   = s.Mxp
            elif s.xp >= count: s.xp -= count; break

class roomChecker:
    """
        `room`(list(2d))            : 화면으로 출력되는 방 그래픽
        `roomIcon`(char)            : 맵에서 표시되는 방 그래픽
        `doorPos`(dict)             : 방에 있는 문의 위치
        `roomType`(int)             : 방의 속성
        `isPlayerHere`(bool)        : 현재 플레이어가 이 위치에 존재하는지에 대한 여부
        `isPlayerVisited`(int(0~2)) : 플레이어가 들린 곳 또는 갈 수 있는 곳을 표시함, 0은 밝혀지지 않음, 1은 밝힐 수 있음, 2는 이미 밝혀짐
        `summonCount`(int)          : 방에서 소환되는 최대 몬스터 수
    """
    def changeDoorPosBlock(block, data):
        DPG = {
            'U' : [0, 6],
            'R' : [6, 12],
            'D' : [12, 6],
            'L' : [6, 0]
            }
        
        for i in range(len(data['doorPos'])):
            keys, values = list(data['doorPos'].keys()), list(data['doorPos'].values())
            if values[i] == 1:
                DPY, DPX = DPG[keys[i]][0], DPG[keys[i]][1]

                s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX] = block
                if   keys[i] in ['U','D']: s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX-1], s.Dungeon[s.Dy][s.Dx]['room'][DPY][DPX+1] = block, block
                elif keys[i] in ['R','L']: s.Dungeon[s.Dy][s.Dx]['room'][DPY-1][DPX], s.Dungeon[s.Dy][s.Dx]['room'][DPY+1][DPX] = block, block

    def summonRandomMonster(data):
        # type, hp
        monsterData = [[0, 4], [1, 10]]
        for i in range(data['summonCount']):
            choiced = random.choice(monsterData)
            addEntity(
                choiced[0],
                choiced[1],
                Dy=s.Dy,
                Dx=s.Dx,
                y=[1, len(data['room'])-2],
                x=[1, len(data['room'][0])-2]
                )
    
    def placeRandomOrbs():
        roomGrid = s.Dungeon[s.Dy][s.Dx]['room']
        for i in range(random.randrange(2, 6)):
            sizeIndex = random.randrange(0, 2)

            typeIndex = None
            percent = random.randrange(1, 101)
            if   percent > 0  and percent <= 45: typeIndex = "hunger"
            elif percent > 45 and percent <= 70: typeIndex = "hp"
            elif percent > 70 and percent <= 80: typeIndex = "def"
            elif percent > 80 and percent <= 85: typeIndex = "atk"
            else                               : typeIndex = "exp"

            placeRandomBlock(
                s.orbs['type'][typeIndex][sizeIndex],
                [1, len(roomGrid)-2],
                [1, len(roomGrid)-2],
                [s.floor]
                )

    def main():
        data = s.Dungeon[s.Dy][s.Dx]

        if l.jpsf == 1 and data['interaction'] == False:
            commentP = True if random.randrange(1, 3) == 1 else False
            match data['roomType']:
                case 1:
                    if data['summonCount'] > 0:
                        play("close_door")
                        roomChecker.summonRandomMonster(data)

                        data['summonCount'] = 0
                        s.roomLock          = True
                        roomChecker.changeDoorPosBlock(s.wall, data)
                    elif len(s.entities) == 0 and s.roomLock == True:
                        play("open_door")

                        s.roomLock                           = False
                        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
                        roomChecker.placeRandomOrbs()
                        roomChecker.changeDoorPosBlock(s.R, data)

                case 2:
                    logger.addLog(f"(슬쩍) 아직 {s.cColors['fg']['L']}이벤트{s.cColors['end']}는 {s.cColors['fg']['R']}{s.cMarkdown([1, 2])}안{s.cColors['end']} 만들었답니다 ㅎㅎ;")
                    s.Dungeon[s.Dy][s.Dx]['interaction'] = True

                case 3:
                    rewardP = random.randrange(1, 101)
                    if rewardP > 30:
                        s.Dungeon[s.Dy][s.Dx]['room'][6][6] = s.item
                        if commentP == True: logger.addLog(f"\"{random.choice(c.treasureRoomComment[0])}\"")
                    elif rewardP >= 10 and rewardP < 30:
                        for i in range(5, 8): s.Dungeon[s.Dy][s.Dx]['room'][i][i] = s.item
                        if commentP == True: logger.addLog(f"\"{random.choice(c.treasureRoomComment[1])}\"")
                    else:
                        for i in range(5, 8): s.Dungeon[s.Dy][s.Dx]['room'][i][i] = s.item
                        s.Dungeon[s.Dy][s.Dx]['room'][5][7] = s.item
                        s.Dungeon[s.Dy][s.Dx]['room'][7][5] = s.item
                        if commentP == True: logger.addLog(f"\"{random.choice(c.treasureRoomComment[2])}\"")
                    s.Dungeon[s.Dy][s.Dx]['interaction'] = True

                case 4:
                    if data['summonCount'] > 0:
                        play("close_door")
                        roomChecker.summonRandomMonster(data)

                        s.Dungeon[s.Dy][s.Dx]['room'][6][6] = s.floor
                        data['summonCount'] = 0
                        s.roomLock          = True
                        roomChecker.changeDoorPosBlock(s.wall, data)
                    elif len(s.entities) == 0 and s.roomLock == True:
                        play("open_door")

                        s.roomLock = False
                        s.Dungeon[s.Dy][s.Dx]['room'][6][6] = s.goal
                        s.Dungeon[s.Dy][s.Dx]['interaction'] = True
                        roomChecker.placeRandomOrbs()
                        roomChecker.changeDoorPosBlock(s.R, data)
