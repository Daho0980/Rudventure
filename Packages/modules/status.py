import os
from   Packages.modules import rooms as r

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

#    ┏━━━━ Wait, you're not color >:(
#   v
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
    else: output = MarkdownKinds[Type]

    return output


# positions
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
p1             = f"{colors['G']}{markdown(3)}@{colors['end']}" # 0, 255, 10
e              = '𓃦'
boss           = '𓃙'
wall           = '◼'
R              = '▒'
item           = f"{colors['Y']}◘{colors['end']}"
box            = '☒'
goal           = f'\033[31m⚑\033[0m'
floor          = '.'
fakeFloor      = '∙'
doorRooms      = [r.field, r.room_1, r.invisible_walls1]
doors          = [[[0,2,5,3,r.room_1]], [[6,3,1,2,r.field]], [[9,14,1,1,r.invisible_walls2]]]
stepableBlocks = [floor]

# Stage settings
nowStage  = 0
stage     = 0
stageName = ""

# Background vars
s        = ''
room     = r.field
jpsf     = False
TFP      = f'{os.getcwd()}/Packages/'
sound    = True
yctuoh   = False
entities = []
Wanted   = []

# Log system
onDisplay = [] # max is 5
onTime    = [] # max is 5
maxOnTime = 5 # max is 5

# In game print settings
showStateDesign = 1 # normal = 1
frame           = 0