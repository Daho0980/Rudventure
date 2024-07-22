import random

from Assets.data             import comments, status
from Assets.data.color       import cColors         as cc
from Game.entities           import player          as p
from Game.entities.player    import event           as pev
from Game.core.system.logger import addLog
from Game.utils.system.sound import play

c, s = comments, status


def hpCheck() -> None:
    if s.hp <= int(s.Mhp*0.3) and not s.hpLow:
        play("system", "hpLow")
        s.hpLow = True
        p.say(random.choice(c.lowHpComment))
    elif int((s.hp / s.Mhp) * 10) > 3: s.hpLow = False

def defCheck() -> None:
    if s.df > 0: s.dfCrack = 0

def ashChipCheck() -> None:
    if s.ashChip>=100:
        s.ashChip -= 100
        s.Mlvl    += 1
        play("system", "ashDiskUp")
        addLog(f"{cc['fg']['G1']}재의 그릇{cc['end']}이 {cc['fg']['F']}1{cc['end']} 개 증가했습니다. (최대 레벨 {cc['fg']['G1']}{s.Mlvl-1}{cc['end']} -> {cc['fg']['F']}{s.Mlvl}{cc['end']})")

def curseCheck() -> None:
    if s.lvl >= s.Mlvl: pev.cursedDeath()