import random, time
from   pynput.keyboard          import Key
from   Packages.modules         import status, rooms, stages
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

    def damage():
        if s.df > 0: s.df -= 1
        else: s.hp -= 1

    def start(x, y):
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
        sound     = f'{s.TFP}sounds{s.s}move.wav'

        if s.room[s.y][s.x] in [s.wall, s.fakeFloor]:
            player.damage()
            s.x = s.bfx
            s.y = s.bfy
            if s.df <= 0 and s.dfCrack <= 0:
                sound = f'{s.TFP}sounds{s.s}crack.wav'
                s.dfCrack = 1
            else: sound = f'{s.TFP}sounds{s.s}Hit.wav'

        elif s.room[s.y][s.x] in enemies:
            s.Wanted = [eval(f"{s.y}"), eval(f"{s.x}")]
            time.sleep(0.01)
            s.Wanted = []
            s.y, s.x = s.bfy, s.bfx
            sound = f'{s.TFP}sounds{s.s}slash.wav'

        elif s.room[s.y][s.x] == s.item:
            boxEvent()
            sound = f'{s.TFP}sounds{s.s}get_item.wav'

        elif s.room[s.y][s.x] == s.R:
            s.room[s.y][s.x] = s.floor
            sound = f'{s.TFP}sounds{s.s}open.wav'
            nowRdoorsNum = s.doors[s.doorRooms.index(s.room)]
            for i in range(len(nowRdoorsNum)):
                if nowRdoorsNum[i][0] == s.y and nowRdoorsNum[i][1] == s.x:
                    s.y = nowRdoorsNum[i][2]
                    s.x = nowRdoorsNum[i][3]
                    s.room = nowRdoorsNum[i][4]
                    break

        elif s.room[s.y][s.x] == ' ': s.hp, s.df = 0, 0

        if s.room[s.y][s.x] == s.box:
            sound  = f'{s.TFP}sounds{s.s}move_box.wav'
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

        s.room[s.bfy][s.bfx] = s.floor
        s.room[s.y][s.x] = s.p1
        play(sound)