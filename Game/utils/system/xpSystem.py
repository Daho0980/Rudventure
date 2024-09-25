from Assets.data             import status
from Assets.data.color       import cColors as cc
from Game.core.system.logger import addLog
from Game.utils.system.sound import play


s = status

def getXP(count:int=0) -> None:
    """
    저주를 얻을 때 발생하는 이벤트
        `count`(int) : xp 증가율
    """
    while (s.xp+count) > s.Mxp:
        s.lvl += 1
        s.Mxp += 3
        if s.lvl >= (s.Mlvl/2):
            exec(s.statusFormula['curseBloodSucking'])
            s.DROD = [f"{cc['fg']['F']}흡혈{cc['end']}", 'F']
        play("system", "curseUp")
        addLog(f"{cc['fg']['F']}저주가 한 층 더 깊어집니다...{cc['end']}")
        if count > s.xp: count -= s.xp
        else:            count -= (s.Mxp-s.xp)
        s.xp = 0
    s.xp += count

def loseXp(count:int=0) -> None:
    """
    저주를 잃을 때 발생하는 이벤트
        `count`(int) : xp 감소율
    """
    bfxp, bfMxp, bfLvl = s.xp, s.Mxp, s.lvl

    while count > 0:
        if s.xp < count:
            if not s.lvl:
                addLog(f"{cc['fg']['F']}저주{cc['end']}가 바닥났습니다!")
                s.xp, s.Mxp, s.lvl = bfxp, bfMxp, bfLvl
                break
            count -= s.xp
            s.lvl -= 1
            s.Mxp -= 3
            s.xp   = s.Mxp
        elif s.xp >= count: s.xp -= count; break