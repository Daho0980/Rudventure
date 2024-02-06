from playsound import playsound as play

from   Assets.data        import status
from   Game.core.system   import logger
# from   Game.utils.sound   import play


s  = status
cc = s.cColors

def getXP(count:int=0) -> None:
    """
    xp를 얻을 때 발생하는 이벤트
        `count`(int) : xp 증가율
    """
    while s.xp + count > s.Mxp:
        play("levelUp", 'interaction')
        logger.addLog(f"{cc['fg']['F']}저주가 한 층 더 깊어집니다...{cc['end']}")
        s.lvl += 1
        s.Mxp += 3
        if count > s.xp: count -= s.xp
        else:            count -= (s.Mxp-s.xp)
        s.xp = 0
    s.xp += count

def loseXp(count:int=0) -> None:
    """
    xp를 잃을 때 발생하는 이벤트
        `count`(int) : xp 감소율
    """
    bfxp, bfMxp, bfLvl = s.xp, s.Mxp, s.lvl

    while count > 0:
        if s.xp < count:
            if s.lvl == 0:
                logger.addLog(f"{cc['fg']['F']}저주{cc['end']}가 부족합니다!")
                s.xp, s.Mxp, s.lvl = bfxp, bfMxp, bfLvl
                break
            count -= s.xp
            s.lvl -= 1
            s.Mxp -= 3
            s.xp   = s.Mxp
        elif s.xp >= count: s.xp -= count; break