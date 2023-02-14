import os
from   Packages.modules import rooms as r

# colors
colors = {
    'R':"\033[31m",
    'G':"\033[32m",
    'Y':"\033[33m",
    'lY':"\033[93m",
    'B':"\033[34m",
    'C':"\033[36m",
    'lB1':"\033[90m",
    'bold':"\033[1m",
    'end':"\033[0m"
}

# positions
x = 0
bfx = 0
y = 0
bfy = 0
hp = 0
Mhp = 0
df = 0
Mdf = 0
dfCrack = 0
atk = 1
hunger = 500
steppedBlock = '.'

btnX = 0
btnY = 0
btn1X = 0
btn1Y = 0

goalX = 0
goalY = 0

# power
main = 1

# icons and doors
LOGO   = "  _   \n /_/     _/   _  _ _/_    _ _ \n/ \ /_//_/ |//_\'/ //  /_// /_\'\n\n𝘢 𝘭 𝘱 𝘩 𝘢\n\n"
LOGO_LIST = ["  _   ", " /_/     _/   _  _ _/_    _ _ ", "/ \ /_//_/ |//_\'/ //  /_// /_\'", "", "𝘢 𝘭 𝘱 𝘩 𝘢", "", ""]
p1 = '@'
e = '𓃦'
boss = '𓀚'
wall = '◼'
R = '▒'
item = '◘'
goal = f'\033[31m⚑\033[0m'
floor = '.'
fakeFloor = '∙'
doorRooms = [r.field, r.room_1, r.invisible_walls1]
doors = [[[0,2,5,3,r.room_1]], [[6,3,1,2,r.field]], [[9,14,1,1,r.invisible_walls2]]]

# stage
nowStage = 0
stage = 0
stageName = ""

# background Vars
s = ''
room = r.field
STOP = '\033[0m'
power = 1
jpsf = False
hpLow = False
TFP = f'{os.getcwd()}/Packages/'
frame = 0
sound = True
objects = []

# in game print settings
showStateDesign = 1 # normal = 1

# ?
Rooms = []
for name in dir(r):
    if not name.startswith('__'):
        Rooms.append(name)