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
atk          = 0
critRate     = 0
critDMG      = 0
hunger       = 0
xp           = 0
Mxp          = 0
lvl          = 0
steppedBlock = ' '
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

ids = {
    0 :  ' ',
    1 :  '■',
    2 :  '.',
    3 :  ' ',
    4 :  f"{cColors['fg']['Y']}É{cColors['end']}",
    5 :  f"{cColors['fg']['R']}F{cColors['end']}",
    6 :  '☒',
    7 :  f"{cColors['fg']['R']}X{cColors['end']}",
    8 :  f"{cColors['fg']['B1']}{cMarkdown(1)}O{cColors['end']}",
    9 :  f"{cColors['fg']['B1']}{cMarkdown(1)}o{cColors['end']}",
    10 : f"{cColors['fg']['R']}o{cColors['end']}",
    11 : f"{cColors['fg']['B1']}o{cColors['end']}",
    12 : f"{cColors['fg']['L']}o{cColors['end']}",
    13 : f"{cColors['fg']['Y']}o{cColors['end']}",
    14 : f"{cColors['fg']['F']}ø{cColors['end']}",
    15 : f"{cColors['fg']['R']}O{cColors['end']}",
    16 : f"{cColors['fg']['B1']}O{cColors['end']}",
    17 : f"{cColors['fg']['L']}O{cColors['end']}",
    18 : f"{cColors['fg']['Y']}O{cColors['end']}",
    19 : f"{cColors['fg']['F']}Ø{cColors['end']}",

    300 : f"{customColor(0, 255, 10)}@{cColors['end']}", # 0, 255, 10
    301 : f"{customColor(0, 255, 10)}&{cColors['end']}", # 0, 255, 10

    600 : '%',
    601 : '#'
}

p1             = f"{customColor(0, 255, 10)}@{cColors['end']}" # 0, 255, 10
p2             = "&"
e              = '%'

enemies = {
    "snippets" : {
        "pain"   : '%',
        "unrest" : '#'
    }
}

R              = '.'
box            = '☒'
goal           = f"{cColors['fg']['R']}F{cColors['end']}"
item           = f"{cColors['fg']['Y']}É{cColors['end']}"
wall           = '■'
squishy        = [f"{cColors['fg']['B1']}{cMarkdown(1)}O{cColors['end']}", f"{cColors['fg']['B1']}{cMarkdown(1)}o{cColors['end']}"]
fakeFloor      = '∙'

boxMark        = f"{cColors['fg']['R']}X{cColors['end']}"
floor          = ' '

# hp -> def -> atk -> hng -> exp
orbs = {
    "size" : {
        "smallOne" : [
            f"{cColors['fg']['R']}o{cColors['end']}",
            f"{cColors['fg']['B1']}o{cColors['end']}",
            f"{cColors['fg']['L']}o{cColors['end']}",
            f"{cColors['fg']['Y']}o{cColors['end']}",
            f"{cColors['fg']['F']}ø{cColors['end']}"
        ],
        "bigOne" : [
            f"{cColors['fg']['R']}O{cColors['end']}",
            f"{cColors['fg']['B1']}O{cColors['end']}",
            f"{cColors['fg']['L']}O{cColors['end']}",
            f"{cColors['fg']['Y']}O{cColors['end']}",
            f"{cColors['fg']['F']}Ø{cColors['end']}"
        ]
    },
    "type" : {
        "hp"     : [f"{cColors['fg']['R']}o{cColors['end']}",  f"{cColors['fg']['R']}O{cColors['end']}"],
        "def"    : [f"{cColors['fg']['B1']}o{cColors['end']}", f"{cColors['fg']['B1']}O{cColors['end']}"],
        "atk"    : [f"{cColors['fg']['L']}o{cColors['end']}",  f"{cColors['fg']['L']}O{cColors['end']}"],
        "hunger" : [f"{cColors['fg']['Y']}o{cColors['end']}",  f"{cColors['fg']['Y']}O{cColors['end']}"],
        "exp"    : [f"{cColors['fg']['F']}ø{cColors['end']}",  f"{cColors['fg']['F']}Ø{cColors['end']}"]
    }
}

orbIds = {
    "size" : {
        "smallOne" : [10, 11, 12, 13, 14],
        "bigOne"   : [15, 16, 17, 18, 19]
    },
    "type" : {
        "hp"     : [10, 15],
        "def"    : [11, 16],
        "atk"    : [12, 17],
        "hunger" : [13, 18],
        "exp"    : [14, 19]
    }
}

stepableBlocks     = [0, 4, 7]
interactableBlocks = {
    "canStepOn"    : [4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "cannotStepOn" : [1, 2, 3, 5, 6, 600, 601]
}

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
jjol         = f"\n{cMarkdown(1)}{cColors['fg']['L']}P a u s e{cColors['end']}\n"

TFP      = ""
sound    = True

entities = []
hitPos   = []

# Option available
option = False

# Log system
maxStack  = 10
onDisplay = []
onTime    = []

# In game print settings
showStateDesign = 2 # normal = 1
frame           = 0
showDungeonMap  = 0 # normal = 0
