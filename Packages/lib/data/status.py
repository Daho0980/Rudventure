import os
from   Packages.lib.data import rooms as r

# Colors
colors = {
    'R':"\033[31m",
    'G':"\033[32m",
    'Y':"\033[33m",
    'lY':"\033[93m",
    'B':"\033[34m",
    'C':"\033[36m",
    'lB1':"\033[90m",
    'end':"\033[0m"
}

def customColor(R, G, B, Type=1):
    colorKinds = {
        1 : '38', # text color
        2 : '48' # bg color
    }
    return f'{colorKinds[Type]};2;{R};{G};{B}'

  #  ┏━━━━ Wait, you're not a color >:(
  # v
def markdown(Type=0):
    MarkdownKinds = {
        0 : "\033[0m", # normal
        1 : "\033[1m", # bold
        2 : "\033[2m", # covered
        3 : "\033[3m", # italic
        4 : "\033[4m", # underscore
        5 : "\033[7m", # reversal
        6 : "\033[8m", # invisible
        7 : "\033[9m" # strikethrough
    }
    if isinstance(Type, list):
        output = ""
        for i in Type: output += MarkdownKinds[i]
    else                     : output = MarkdownKinds[Type]

    return output


# status
name         = ""
lightName    = ""

Dy           = 0
bfDy         = 0
Dx           = 0
bfDx         = 0
x            = 0
bfx          = 0
y            = 0
bfy          = 0

hp           = 0
Mhp          = 0
hpLow        = False
df           = 0
Mdf          = 0
dfCrack      = 0
atk          = 1
hunger       = 500
steppedBlock = '.'

# So MUCH useless but I cannot delete it because of in game systems. I'll delete it later.
btnX  = 0
btnY  = 0
btn1X = 0
btn1Y = 0

# Goal position
goalX = 0
goalY = 0

# Power
main = 1

# Icons and doors
LOGO           = "  _   \n /_/     _/   _  _ _/_    _ _ \n/ \ /_//_/ |//_\'/ //  /_// /_\'\n\n𝘢 𝘭 𝘱 𝘩 𝘢\n\n"

welcomeMessage = []

p1             = f"{colors['G']}{markdown(3)}@{colors['end']}" # 0, 255, 10
p2             = "&"
e              = '%'
boss           = '#'

squishy        = [f"{colors['B']}{markdown(1)}O{colors['end']}", f"{colors['B']}{markdown(1)}o{colors['end']}"]
wall           = '▀'
R              = '▒'
item           = f"{colors['Y']}◘{colors['end']}"
box            = '☒'
boxMark        = f"{colors['R']}✘{colors['end']}"
goal           = f'\033[31mF\033[0m'
floor          = '.'
fakeFloor      = '∙'

stepableBlocks = [floor, item, boxMark]

doorRooms      = ["field", "room_1", "invisible_walls1"]
doors          = [[[0,2,5,3,"room_1"]], [[6,3,1,2,"field"]], [[9,14,1,1,"invisible_walls2"]]]

# Stage settings
nowStage  = 0
stage     = 0
stageName = ""
roomName  = ""

# Background vars
s        = ''
room     = r.field
Dungeon  = []

jpsf     = False
TFP      = ""
sound    = True
yctuoh   = False

entities = []
Wanted   = []

# Log system
onDisplay = [] # max is 5
onTime    = [] # max is 5

# In game print settings
showStateDesign = 1 # normal = 1
frame           = 0