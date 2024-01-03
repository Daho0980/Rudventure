# Colors
cColors:dict = {
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

# def customColor(R, G, B, Type=1):
#     """
#     `R, G, B`(int): RGB값을 정함\n
#     `Type`(int) : 어떤 색을 변경할 지 정함\n
#         - `1` : 글자 색 변경\n
#         - `2` : 배경 색 변경\n
#     """
#     return f'\033[{38 if Type == 1 else 48};2;{R};{G};{B}m'

customColor = lambda R,G,B,T=1: f"\033[{[0,38,48][T]};2;{R};{G};{B}m"

#  ┏━━━━ Wait, you're not a color >:(
# v
def cMarkdown(Type:(list[int]|int)=0) -> str:
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
name:str         = ""
lightName:str    = ""

Dy:int           = 0
bfDy:int         = 0
Dx:int           = 0
bfDx:int         = 0
x:int            = 0
bfx:int          = 0
y:int            = 0
bfy:int          = 0

hp:int           = 0
Mhp:int          = 0
hpLow:bool       = False
df:int           = 0
Mdf:int          = 0
dfCrack:int      = 0
atk:int          = 0
critRate:int     = 0
critDMG:int      = 0
hunger:int       = 0
xp:int           = 0
Mxp:int          = 0
lvl:int          = 0
steppedBlock:str = ' '
killCount:int    = 0

# Power
main:int = 1

# Texts and icons
LOGO:str = f"""
  _   
 /_/     _/   _  _ _/_    _ _ 
/ \\ /_//_/ |//_\'/ //  /_// /_\'

  {cColors['fg']['R']}.-  .-..  .--.  ....  .-{cColors['end']}

"""

welcomeMessage:list = []

ids:dict = {
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

orbIds:dict = {
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

stepableBlocks:list     = [0, 4, 7]
interactableBlocks:dict = {
    "canStepOn"    : [4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "cannotStepOn" : [1, 2, 3, 5, 6, 600, 601]
}

# Stage settings
stage:int     = 0

# Background vars
s:str   = ''
TFP:str = ""

Dungeon:list     = []
roomLock:bool    = False
killAll:bool     = False
deadReason       = None
DROD:list        = [None, '']
pauseText:str    = f"\n{cMarkdown(1)}{cColors['fg']['L']}P a u s e{cColors['end']}\n"
debugScreen:bool = False

allSound:bool = True
sound:dict    = {
    "hostileMob"  : True,
    "friendlyMob" : True,
    "interaction" : True,
    "system"      : True,
    "player"      : True
}

entities:list = []
hitPos:list   = []

# Option available
option:bool = False

# Log system
maxStack:int   = 10
onDisplay:list = []
onTime:list    = []

# InGame print settings
showStateDesign:int = 2 # normal = 1
frame:int           = 0
showDungeonMap:int  = 0 # normal = 0
