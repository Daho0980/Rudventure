# Colors
colors = {
    'R'  :"\033[31m",
    'G'  :"\033[32m",
    'Y'  :"\033[33m",
    'lY' :"\033[93m",
    'B'  :"\033[34m",
    'C'  :"\033[36m",
    'lB1':"\033[90m",
    'lP' :"\033[95m",
    'end':"\033[0m"
}

def customColor(R, G, B, Type=1):
    colorKinds = {
        1 : '38', # text color
        2 : '48' # bg color
    }
    return f'\033[{colorKinds[Type]};2;{R};{G};{B}m'

  #  ┏━━━━ Wait, you're not a color >:(
  # v
def markdown(Type=0):
    """
    list 형식으로 여러개 쓸 수 있음

    `0` : 기본
    `1` : 두껍게
    `2` : 가려짐, 어떤 색이든 더 진한 색으로 표시됨
    `3` : 기울임꼴
    `4` : 밑줄
    `5` : 배경색과 글자색 반전 아님말고
    `6` : 없음. 진짜 그냥 없음
    `7` : 중간줄
    """
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
    output = ""
    
    if isinstance(Type, list):
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
xp           = 0
Mxp          = 10
lvl          = 0
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

# Texts and icons
LOGO           = f"""
  _   
 /_/     _/   _  _ _/_    _ _ 
/ \ /_//_/ |//_\'/ //  /_// /_\'

  {colors['R']}.-  .-..  .--.  ....  .-{colors['end']}

"""

welcomeMessage = []

p1             = f"{customColor(0, 255, 10)}{markdown(3)}@{colors['end']}" # 0, 255, 10
p2             = "&"
e              = '%'
boss           = '#'

enemies = {
    "snippets" : {
        "pain"   : '%',
        "unrest" : '#'
    }
}

squishy        = [f"{colors['B']}{markdown(1)}O{colors['end']}", f"{colors['B']}{markdown(1)}o{colors['end']}"]
wall           = '■'
R              = '▤'
item           = f"{colors['Y']}◘{colors['end']}"
box            = '☒'
boxMark        = f"{colors['R']}✘{colors['end']}"
goal           = f'\033[31mF\033[0m'
floor          = '.'
fakeFloor      = '∙'
# hp -> def -> atk -> hng -> exp
orbs = {
    "size" : {
        "smallOne" : [
            f"{colors['R']}o{colors['end']}",
            f"{colors['B']}o{colors['end']}",
            f"{colors['G']}o{colors['end']}",
            f"{colors['lY']}o{colors['end']}",
            f"{colors['lP']}+{colors['end']}"
        ],
        "bigOne" : [
            f"{colors['R']}O{colors['end']}",
            f"{colors['B']}O{colors['end']}",
            f"{colors['G']}O{colors['end']}",
            f"{colors['lY']}O{colors['end']}",
            f"{colors['lP']}÷{colors['end']}"
        ]
    },
    "type" : {
        "hp"     : [f"{colors['R']}o{colors['end']}", f"{colors['R']}O{colors['end']}"],
        "def"    : [f"{colors['B']}o{colors['end']}", f"{colors['B']}O{colors['end']}"],
        "atk"    : [f"{colors['G']}o{colors['end']}", f"{colors['G']}O{colors['end']}"],
        "hunger" : [f"{colors['lY']}o{colors['end']}", f"{colors['lY']}O{colors['end']}"],
        "exp"    : [f"{colors['lP']}+{colors['end']}", f"{colors['lP']}÷{colors['end']}"]
    }
}

stepableBlocks = [floor, item, boxMark]

# Stage settings
stage     = 0

# Background vars
s        = ''
room     = ""
Dungeon  = []
roomLock = False
killAll = False

TFP      = ""
sound    = True

entities = []
Wanted   = []

# Log system
onDisplay = [] # max is 5
onTime    = [] # max is 5

# In game print settings
showStateDesign = 1 # normal = 1
frame           = 0
showDungeonMap  = 0 # normal = 0
