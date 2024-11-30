from Assets.data.color import cColors as cc


name:str      = ""
lightName:str = ""

Dy:int = 0
Dx:int = 0
x:int  = 0
y:int  = 0

bfDy:int = 0
bfDx:int = 0
bfx:int  = 0
bfy:int  = 0

hp:int       = 0
xp:int       = 0
df:int       = 0
hunger:int   = 0
lvl:int      = 0
fairWind:int = 0

Mhp:int       = 0
Mdf:int       = 0
Mxp:int       = 0
Mlvl:int      = 0
MFairWind:int = 0

atk:int         = 0
critRate:int    = 0
critDMG:int     = 0
evasionRate:int = 0

statusFormula = {
    "evasion"           : "s.evasionRate",
    "curseBloodSucking" : "s.hp -= 1"
}

ashChip:int = 0

steppedBlock:dict = {"block" : '  ', "id" : 0, "type" : 0}
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

dfCrack:int = 0
hpLow:bool  = False

playerMode:str = "normal" # normal||observe

monologueCount = 0
monologueRange = 0

playerDamageIcon = ['@ ']

playerVoice = "glagatrof"
playerColor = [cc['fg']['L'], "L"]