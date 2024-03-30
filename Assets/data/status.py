from Assets.data.color import cColors

_cc = cColors

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
Dx:int           = 0
x:int            = 0
y:int            = 0

bfDy:int         = 0
bfDx:int         = 0
bfx:int          = 0
bfy:int          = 0

hp:int           = 0
xp:int           = 0
df:int           = 0
hunger:int       = 0
lvl:int          = 0

Mhp:int          = 0
Mdf:int          = 0
Mxp:int          = 0

atk:int          = 0
critRate:int     = 0
critDMG:int      = 0

ashChip:int      = 0

steppedBlock:str = ' '
killCount:int    = 0

dfCrack:int      = 0
hpLow:bool       = False

# Power
main:int = 1

# Texts and icons
LOGO:str = f"""
  _   
 /_/     _/   _  _ _/_    _ _ 
/ \\ /_//_/ |//_\'/ //  /_// /_\'

  {_cc['fg']['R']}.-  .-..  .--.  ....  .-{_cc['end']}

"""

welcomeMessage:list[str] = []

ids:dict[int,str] = {
    -1 : ' ',
    0 :  ' ',
    1 :  '■',
    2 :  '.',
    3 :  ' ',
    4 :  "É",
    5 :  "F",
    6 :  '☒',
    7 :  "X",
    8 :  "O",
    9 :  "o",
    10 : "o",
    11 : "q",
    12 : "v",
    13 : "o",
    14 : "ø",
    15 : "O",
    16 : "Q",
    17 : "V",
    18 : "O",
    19 : "Ø",

    300 : "@", # 0, 255, 10
    301 : "&", # 0, 255, 10

    600 : '%',
    601 : '#',
    602 : "※",

    900 : ';'
}

orbIds:dict[str,dict[str,list[int]]] = {
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

stepableBlocks:list[int]               = [0, 4, 7]
interactableBlocks:dict[str,list[int]] = {
    "canStepOn"    : [4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 900],
    "cannotStepOn" : [-1, 1, 2, 3, 5, 6, 600, 601],
    "explodable"   : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 900]
}

enemyIds:list[int] = [600, 601, 602]

# Stage settings
stage:int     = 0

# Background vars
s:str         = ''
TFP:str       = ""
pythonVersion = __import__("sys").version_info

Dungeon:list     = []
roomLock:bool    = False
killAll:bool     = False
DROD:list        = [None, '']
pauseText:str    = f"\n{cMarkdown(1)}{_cc['fg']['L']}일 시 정 지{_cc['end']}\n"
debugScreen:bool = False

# Modes
cowardMode:bool  = False
ezMode:bool      = False
publicMode:bool  = False

entityCount:int      = 0
totalEntityCount:int = 0
hitPos:list           = []

# Log system
maxStack:int        = 10
onDisplay:list[str] = []
onTime:list[int]    = []

# InGame print settings
frameRate:int      = -1
frame:int|float    = 0
statusDesign:int   = 1 # normal = 0
showDungeonMap:int = 0 # normal = 0
