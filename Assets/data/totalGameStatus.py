from .color import cColors as _cc


version:str|int = "???"

# region player status
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
fairWind:int     = 0

Mhp:int          = 0
Mdf:int          = 0
Mxp:int          = 0
Mlvl:int         = 0
MFairWind:int    = 0

atk:int          = 0
critRate:int     = 0
critDMG:int      = 0
evasionRate:int  = 0

statusFormula = {
    "evasion"           : "s.evasionRate",
    "curseBloodSucking" : "s.hp -= 1"
}

ashChip:int      = 0

steppedBlock:dict = {"block" : ' ', "id" : 0, "type" : 0}
killCount:int     = 0

inventory:dict   = {
    "cells" : [
        {"item":{}, "disabled":False},
        {"item":{}, "disabled":False},
        {"item":{}, "disabled":False}
    ], # full = 6 cells
    "pointer" : 0,
    "max"     : 6
}

target:dict = {
    "hashKey"    : "",
    "attackable" : False,
    "command"    : False
}

dfCrack:int      = 0
hpLow:bool       = False

# region player move
#       playerMode has 2 modes:
#               "normal" and "observe"
#               The default settings are "normal".
playerMode:str = "normal"
isLoadfromBody = False

soliloquyCount = 0
soliloquyRange = 0

playerDamageIcon = ['@']

playerVoice = "glagatrof"
playerColor = [_cc['fg']['L'], "L"]

# region power
main:int = 1

# region id
ids:dict[int,str] = {
    -1 : ' ',  # 무적
    0 :  ' ',  # 바닥
    1 :  '■', # 벽
    2 :  '.',  # 문
    3 :  ' ',  # 가짜 바닥
    4 :  'É',  # 구슬 상자
    5 :  'F',  # 출구
    6 :  '☒',  # 상자
    7 :  'X',  # 상자 표적
    8 :  'O',  # 말랑이 1
    9 :  'o',  # 말랑이 2
    10 : 'o',  # 작은 체력 구슬
    11 : 'q',  # 작은 방어력 구슬
    12 : 'v',  # 작은 공격력 구슬
    13 : 'o',  # 작은 허기 구슬
    14 : 'ø',  # 작은 저주 구슬
    15 : 'O',  # 큰 체력 구슬
    16 : 'Q',  # 큰 방어력 구슬
    17 : 'V',  # 큰 공격력 구슬
    18 : 'O',  # 큰 허기 구슬
    19 : 'Ø',  # 큰 저주 구슬
    20 : '☲',  # 토용
    21 : '☲',  # 죽은 토용
    22 : '*',  # 꽃
    23 : '.',  # 꽃잎
    24 : '?',  # 아이템
    25 : ' ',  # 구멍
    26 : 'X',  # 시체

    200 : 'R', # 고양이

    300 : '@', # 0, 255, 10 & 플레이어 1
    301 : '&', # 0, 255, 10 & 플레이어 2

    400 : 'Y', # 저주를 씻어내는 신상
    401 : 'Y', # 오염된 저주를 씻어내는 신상

    501 : 'H', # 최대 체력 증가(대동맥)
    502 : 'U', # 최대 방어력 증가(대정맥)

    600 : '%', # 고통
    601 : '#', # 불안
    602 : "※", # 원망

    900 : ';'  # 잿조각
}

types = {
    0 : "block",
    1 : "entity",
    2 : "item",
    3 : "item-weapon",
    4 : "item-food"
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

monsterInteractableBlocks:dict = {
    "steppable" : {
        "maintainable"   : [0, 7],
        "unmaintainable" : [4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 501, 502, 900],
        "total"          : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 501, 502, 900]
    },
    "unsteppable" : [-1, 1, 2, 3, 5, 6, 20, 21, 25, 200, 300, 301, 400, 401, 600, 601, 602],
    "breakable"   : [0, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 501, 502, 900]
}
interactableBlocks:dict = {
    "steppable" : {
        "maintainable"   : [0, 7],
        "unmaintainable" : [4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 501, 502, 900],
        "total"          : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 501, 502, 900]
    },
    "unsteppable" : [-1, 1, 2, 3, 5, 6, 20, 21, 25, 200, 300, 301, 400, 401, 600, 601, 602],
    "explodable"  : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 24, 400, 401, 900]
}


enemyIds:list[int]  = [600, 601, 602]
animalIds:list[int] = [200]

# region stage
stage:int     = 0

# region background
s:str         = ''
TFP:str       = ""
pythonVersion = __import__("sys").version_info

Dungeon:list     = []
roomLock:bool    = False
killAll:bool     = False
clearEntity:bool = False
DROD:list        = [None, '']

debugConsole:bool = False

startTime:float   = 0
elapsedTime:float = 0

# region gamemodes
bodyPreservationMode:bool  = False
ezMode:bool                = False
sanjibaMode:bool           = False

# region entity
enemyCount:int              = 0
entityCount:int             = 0
totalEntityCount:int        = 0
entityHashPool:list[str]    = []
hitPos:dict[str,list[list]] = {
    "pos" : [],
    "data": []
}
friendlyEntity:list[str] = []
entityDataMaintained     = {"addAnimal"  : {}}
entitySaveTrigger        = False

# region log
maxStack:int        = 10
onDisplay:list[str] = []
onTime:list[int]    = []
port:int            = -1

# region block description
infoWindow = {
    "text"    : "",
    "time"    : 0,
    "setTime" : 1
}

# region display
frameRate:int   = -1
frame:int|float = 0

currentCurseNoiseFrequency = 0
curseNoiseFrequency        = 5

dynamicCameraMoving:int = 0 # normal = 0

statusDesign:int   = 1 # normal = 0
showDungeonMap:int = 0 # normal = 0

# region sound volume
volume = 50

# Terminal screen size table
# 'S'creen'S'ize'S'
# I know. This variable name looks so f**king silly.
# But the name before that was too long.
sss = {
    "minimum"     : (58, 122),
    "recommended" : (67, 195)
}
autoTerminalSize  = None
checkTerminalSize = None

# region system
recordKey = False
key       = __import__("Game.core.system.keyBind", fromlist=["KeyBind"]).KeyBind()

gameRecord:bool = True