# Colors
cColors = {
    "fg" : {
        "B" :   "\033[;38;5;0m",
        "M" :   "\033[;38;5;1m",
        "G" :   "\033[;38;5;2m",
        "O" :   "\033[;38;5;3m",
        "N" :   "\033[;38;5;4m",
        "P" :   "\033[;38;5;5m",
        "T" :   "\033[;38;5;6m",
        "S" :   "\033[;38;5;7m",
        "G1" :  "\033[;38;5;8m",
        "R" :   "\033[;38;5;9m",
        "L" :  "\033[;38;5;10m",
        "Y" :  "\033[;38;5;11m",
        "B1" : "\033[;38;5;12m",
        "F" :  "\033[;38;5;13m",
        "A" :  "\033[;38;5;14m",
        "W" :  "\033[;38;5;15m"
    },
    "bg" : {
        "B" :   "\033[;48;5;0m",
        "M" :   "\033[;48;5;1m",
        "G" :   "\033[;48;5;2m",
        "O" :   "\033[;48;5;3m",
        "N" :   "\033[;48;5;4m",
        "P" :   "\033[;48;5;5m",
        "T" :   "\033[;48;5;6m",
        "S" :   "\033[;48;5;7m",
        "G1" :  "\033[;48;5;8m",
        "R" :   "\033[;48;5;9m",
        "L" :  "\033[;48;5;10m",
        "Y" :  "\033[;48;5;11m",
        "B1" : "\033[;48;5;12m",
        "F" :  "\033[;48;5;13m",
        "A" :  "\033[;48;5;14m",
        "W" :  "\033[;48;5;15m",
    },
    "end" : "\033[0m"
}

def customColor(R, G, B, Type=1):
    """
    `R, G, B`(int): RGB값을 정함\n
    `Type`(int) : 어떤 색을 변경할 지 정함\n
        - `1` : 글자 색 변경\n
        - `2` : 배경 색 변경\n
    """
    return f'\033[{38 if Type == 1 else 48};2;{R};{G};{B}m'

#  ┏━━━━ Wait, you're not a color >:(
# v
def cMarkdown(Type=0):
    """
    list 형식으로 여러개 쓸 수 있음

    `0` : 기본\n
    `1` : 두껍게\n
    `2` : 밑줄\n
    `3` : 배경색과 글자색 반전 아님말고\n
    `4` : 없음. 진짜 그냥 사라짐
    """
    MarkdownKinds = {
        0 : "\033[0m", # normal (end)
        1 : "\033[1m", # bold
        2 : "\033[4m", # underscore
        3 : "\033[7m", # reversal
        4 : "\033[8m"  # invisible
    }
    output = ""

    if isinstance(Type, list):
        for i in Type: output += MarkdownKinds[i]
    else: output = MarkdownKinds[Type]

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
killCount    = 0

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
LOGO = f"""
  _   
 /_/     _/   _  _ _/_    _ _ 
/ \ /_//_/ |//_\'/ //  /_// /_\'

  {cColors['fg']['R']}.-  .-..  .--.  ....  .-{cColors['end']}

"""

welcomeMessage = []

p1             = f"{customColor(0, 255, 10)}@{cColors['end']}" # 0, 255, 10
p2             = "&"
e              = '%'
boss           = '#'

enemies = {
    "snippets" : {
        "pain"   : '%',
        "unrest" : '#'
    }
}

squishy        = [f"{cColors['fg']['B1']}{cMarkdown(1)}O{cColors['end']}", f"{cColors['fg']['B1']}{cMarkdown(1)}o{cColors['end']}"]
wall           = '■'
R              = '▤'
item           = f"{cColors['fg']['Y']}ᢂ{cColors['end']}"
box            = '☒'
boxMark        = f"{cColors['fg']['R']}✘{cColors['end']}"
goal           = f"{cColors['fg']['R']}F{cColors['end']}"
floor          = '.'
fakeFloor      = '∙'
# hp -> def -> atk -> hng -> exp
orbs = {
    "size" : {
        "smallOne" : [
            f"{cColors['fg']['R']}o{cColors['end']}",
            f"{cColors['fg']['B1']}o{cColors['end']}",
            f"{cColors['fg']['L']}o{cColors['end']}",
            f"{cColors['fg']['Y']}o{cColors['end']}",
            f"{cColors['fg']['F']}÷{cColors['end']}"
        ],
        "bigOne" : [
            f"{cColors['fg']['R']}O{cColors['end']}",
            f"{cColors['fg']['B1']}O{cColors['end']}",
            f"{cColors['fg']['L']}O{cColors['end']}",
            f"{cColors['fg']['Y']}O{cColors['end']}",
            f"{cColors['fg']['F']}+{cColors['end']}"
        ]
    },
    "type" : {
        "hp"     : [f"{cColors['fg']['R']}o{cColors['end']}",  f"{cColors['fg']['R']}O{cColors['end']}"],
        "def"    : [f"{cColors['fg']['B1']}o{cColors['end']}", f"{cColors['fg']['B1']}O{cColors['end']}"],
        "atk"    : [f"{cColors['fg']['L']}o{cColors['end']}",  f"{cColors['fg']['L']}O{cColors['end']}"],
        "hunger" : [f"{cColors['fg']['Y']}o{cColors['end']}",  f"{cColors['fg']['Y']}O{cColors['end']}"],
        "exp"    : [f"{cColors['fg']['F']}+{cColors['end']}",  f"{cColors['fg']['F']}÷{cColors['end']}"]
    }
}

stepableBlocks = [floor, item, boxMark]

# Stage settings
stage     = 0

# Background vars
s            = ''
room         = ""
Dungeon      = []
roomLock     = False
killAll      = False
deadReason   = None
maxInputSize = 250

TFP      = ""
sound    = True

entities = []
hitPos   = []

# Option available
option = False

# Log system
onDisplay = [] # max is 5
onTime    = [] # max is 5

# In game print settings
showStateDesign = 2 # normal = 1
frame           = 0
showDungeonMap  = 0 # normal = 0
