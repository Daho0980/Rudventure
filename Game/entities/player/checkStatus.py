from random import choice

from .                       import event   as pev
from Assets.data.color       import cColors as cc
from Game.entities           import player  as p
from Game.core.system.logger import addLog
from Game.utils.system.sound import play

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


def hpCheck() -> None:
    if s.hp<=int(s.Mhp*0.3) and not s.hpLow:
        play("system", "hpLow")
        s.hpLow = True
        p.say(choice(c.lowHp))

    elif int((s.hp / s.Mhp) * 10) > 3: s.hpLow = False

def defCheck() -> None:
    if s.df > 0: s.dfCrack = 0

def ashChipCheck() -> None:
    if s.ashChip >= 100:
        s.ashChip -= 100
        s.Mlvl    += 1

        play("system", "ashDiskUp")
        addLog(
            f"{cc['fg']['G1']}재의 그릇{cc['end']}의 수가 증가했습니다! (그릇의 수 {cc['fg']['G1']}{s.Mlvl-1}{cc['end']} -> {cc['fg']['F']}{s.Mlvl}{cc['end']})",
            colorKey='G1'
        )

def curseCheck() -> None:
    if s.lvl >= s.Mlvl: pev.cursedDeath()