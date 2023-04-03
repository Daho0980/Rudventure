# -*- coding: utf-8 -*-
import os
import time
import random
from   Packages.lib                          import player, quests
# from   Packages.lib.data                     import status, comments
from   Packages.lib                          import data
from   Packages.lib.modules                  import makeNewListener, Textbox, logger
from   Packages.lib.system                   import DungeonMaker, options, mainSettings
from   Packages.lib.system.Secret.cursorType import cursor
from   Packages.lib.system.Secret.doubleBuffer      import DoubleBuffer
from   Packages.lib.system.globalFunc        import osRelated, graphic, idRelated, entity, system, sound

roomNames               = ["\033[31mStart\033[0m", "Normal Room", "\033[32mEvent Room\033[0m", "\033[33mTreasure Room\033[0m", "\033[34mExit\033[0m"]
s, l                    = data.status, data.lockers
p, dgm, mnl, t          = player.player, DungeonMaker, makeNewListener, Textbox
osr, grp, idr, ent, snd = osRelated, graphic, idRelated, entity, sound
q                       = quests
s.s                     = osr.slash()
s.TFP                   = f"{os.getcwd()}{s.s}"
dbf                     = DoubleBuffer()


def gameChecker():
    if s.main == 1:
        grp.clear()
        l.jpsf == 0
        if s.hp <= 0 or s.hunger <= 0:
            s.killAll = True
            snd.play("defeat")
            print(f"{s.colors['R']}{s.markdown(1)}")
            print(t.TextBox(f"   사 망 하 셨 습 니 다   \n\n   {s.markdown([0, 3])}{s.colors['R']}\"{random.choice(data.comments.defeatComment)}\"{s.markdown([0, 1])}{s.colors['R']}   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold"))
            print(s.colors['end'])
            time.sleep(2.5)
            Achievements = {
                "내려간 깊이" : f"{s.colors['lY']}{s.stage}{s.colors['end']}",
                "최대 레벨"   : f"{s.colors['lP']}{s.lvl}{s.colors['end']}"
            }
            for num, text in enumerate(Achievements):
                print(f"{text} : {list(Achievements.values())[num]}")
                time.sleep(0.2)
            cursor.show()
            s.main = 0

        else:
            snd.play("clear")
            print(f"{s.colors['G']}{s.markdown(1)}")
            print(t.TextBox(f"   지 배   성 공   \n\n   {s.markdown([0, 3])}{s.colors['G']}\"{random.choice(data.comments.victoryComment)}\"{s.markdown([0, 1])}{s.colors['G']}   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold"))
            print(s.colors['end'])
            time.sleep(2)

def playerChecker():
    if s.df > 0   : s.dfCrack = 0

    if int((s.hp / s.Mhp) * 100) <= 30 and s.hpLow == False:
        s.hpLow = True
        snd.play(f"hp_low")
        logger.addLog(f"{s.lightName} 님의 체력이 부족합니다! {s.colors['R']}(현재 체력 : {s.hp}){s.colors['end']}")
    elif int((s.hp / s.Mhp) * 100) > 30: s.hpLow = False

cursor.hide()

mainSettings.init()
grp.clear()
p.set()

mnl.addListener()
while s.main == 1:
    grp.clear()
    # SN        = f"{s.colors['G']}지 상{s.colors['end']}" if s.stage == 0 else f"{s.colors['R']}{s.stage} 번 째   나 락{s.colors['end']}"
    if l.jpsf == 0: SN = "지금 꺼져있다고 개새끼들아"
    else: SN = f"{s.colors['G']}지 상{s.colors['end']}" if s.stage == 0 else f"{s.colors['R']}{s.stage} 번 째   나 락{s.colors['end']}"
    s.Dungeon = dgm.DungeonMaker()
    options.showMap()

    p.start(4, 4, 6, 6)
    system.roomChecker.placeRandomOrbs()
    grp.showStage(f"{s.colors['R']}- {s.stage}{s.colors['end']}", stageName=SN)

    s.stage += 1
    l.jpsf = 1
    while q.quest() == 0:
        if s.hp <= 0 or s.hunger <= 0 or s.main != 1: break
        if l.jpsf == 1:
            playerChecker()
            dbf.write(grp.fieldPrint(s.Dungeon[s.Dy][s.Dx]['room'])); dbf.render()
            system.roomChecker.main()
            if s.frame > 0: time.sleep(1/s.frame)
    gameChecker()

#으허허 나 개발하기 너무 귀ㅣ찮아ㅏㅏ 손이 녹아내리고잇ㅅ어ㅓㅓㅓㅓ
# ㅡ화ㅡ아ㅏㅇㅇ난;ㅐㅑㅓ해ㅑㅓㅁ;ㅐㅑㅓㄹ;중ㄹ