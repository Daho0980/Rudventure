import random, time
from   pynput.keyboard          import Key
from   Packages.lib             import stages
from   Packages.lib.data        import rooms, status
from   Packages. lib.modules    import logger
from   Packages.globalFunctions import play

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

    def damage(block="?"):
        if s.df > 0: s.df -= 1
        else: s.hp -= 1
        logger.addLog(f"{s.lightName}이(가) {s.markdown(1)}[ {block} ]{s.colors['end']} 에 의해 상처입었습니다 {s.colors['R']}(남은 체력 : {s.hp}){s.colors['end']} {s.colors['B']}(남은 방어력 : {s.df}){s.colors['end']}")

    def start(y, x):
        s.room[y][x] = s.p1
        s.x = x
        s.y = y

    def move(Dir, Int): 
        enemies = [s.e, s.boss]

        if s.df > 0: s.dfCrack = 0
        s.bfx = s.x
        s.bfy = s.y
        if Dir == Key.up: s.y -= Int
        elif Dir == Key.down: s.y += Int
        elif Dir == Key.left: s.x -= Int
        elif Dir == Key.right: s.x += Int
        s.hunger -= 1
        sound     = f'{s.TFP}Packages{s.s}sounds{s.s}move.wav'

        if s.room[s.y][s.x] in [s.wall, s.fakeFloor]:
            player.damage(s.room[s.y][s.x])
            s.x = s.bfx
            s.y = s.bfy
            if s.df <= 0 and s.dfCrack <= 0:
                sound = f'{s.TFP}Packages{s.s}sounds{s.s}crack.wav'
                logger.addLog(f"{s.colors['B']}방어구{s.colors['end']}가 부서졌습니다!")
                s.dfCrack = 1
            else: sound = f'{s.TFP}Packages{s.s}sounds{s.s}Hit.wav'

        elif s.room[s.y][s.x] in enemies:
            s.Wanted = [eval(f"{s.y}"), eval(f"{s.x}")]
            time.sleep(0.01)
            s.Wanted = []
            s.y, s.x = s.bfy, s.bfx
            sound = f'{s.TFP}Packages{s.s}sounds{s.s}slash.wav'

        elif s.room[s.y][s.x] == s.item:
            boxEvent()
            sound = f'{s.TFP}Packages{s.s}sounds{s.s}get_item.wav'

        elif s.room[s.y][s.x] == s.R:
            s.room[s.y][s.x] = s.floor
            sound = f'{s.TFP}Packages{s.s}sounds{s.s}open.wav'
            nowRdoorsNum = s.doors[s.doorRooms.index(s.room)]
            for i in range(len(nowRdoorsNum)):
                if nowRdoorsNum[i][0] == s.y and nowRdoorsNum[i][1] == s.x:
                    s.y = nowRdoorsNum[i][2]
                    s.x = nowRdoorsNum[i][3]
                    s.room = nowRdoorsNum[i][4]
                    break

        elif s.room[s.y][s.x] == ' ': s.hp, s.df = 0, 0

        elif s.room[s.y][s.x] == s.box:
            sound  = f'{s.TFP}Packages{s.s}sounds{s.s}move_box.wav'
            cx, cy = 0, 0
            if Dir == Key.up or Dir == Key.down:
                if Dir == Key.up: cy = s.y - Int
                elif Dir == Key.down: cy = s.y + Int
                if s.room[cy][s.x] == s.wall or\
                s.room[cy][s.x] == s.e or\
                s.room[cy][s.x] == s.R: s.y, s.x = s.bfy, s.bfx
                else: s.room[cy][s.x] = s.box
            elif Dir == Key.left or Dir == Key.right:
                if Dir == Key.left: cx = s.x - Int
                elif Dir == Key.right: cx = s.x + Int
                if s.room[s.y][cx] == s.wall or\
                s.room[s.y][cx] == s.e or\
                s.room[s.y][cx] == s.R: s.y, s.x = s.bfy, s.bfx
                else: s.room[s.y][cx] = s.box

        elif s.room[s.y][s.x] in s.squishy:
            sound = f'{s.TFP}Packages{s.s}sounds{s.s}squish.wav'
            if s.room[s.y][s.x] == s.squishy[0]: s.room[s.y][s.x] = s.squishy[1]
            else: s.room[s.y][s.x] = s.squishy[0]
            s.y, s.x = s.bfy, s.bfx
            logger.addLog(f"{s.lightName}이(가) {s.colors['B']}말랑이{s.colors['end']}를 만졌습니다 (말랑)")

        s.room[s.bfy][s.bfx] = s.floor
        s.room[s.y][s.x] = s.p1
        play(sound)