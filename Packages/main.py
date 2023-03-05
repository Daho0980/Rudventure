# -*- coding: utf-8 -*-
import os, sys, time
s = '\\' if os.name == "nt" else "/"
TFP = f'{os.getcwd()}{s}'
exec(open(f"{TFP}Packages{s}lib{s}system{s}downloadModules.py", encoding='utf8').read())
from Packages.lib.system                   import globalFunctions
from Packages.lib               import player, stages, quests
from Packages.lib.data          import rooms, status
from Packages.lib.system        import mainSettings
from Packages.lib.modules       import Textbox, makeNewListener, logger
from Packages.lib.system.globalFunctions   import clear

p, r, s, S, S1, gbf, t, mnl= player.player, rooms, status, stages.stages, stages, globalFunctions, Textbox, makeNewListener
s.s                        = gbf.slash()
s.TFP                      = TFP
clear()
p.set()


def gameChecker():
    if int((s.hp / s.Mhp) * 100) <= 30 and s.hpLow == False:
        s.hpLow = True
        gbf.play(f"{s.TFP}Packages{s.s}sounds{s.s}hp_low.wav"); logger.addLog(f"{s.colors['lY']}{s.name}{s.colors['end']} 님의 체력이 부족합니다! {s.colors['R']}(현재 체력 : {s.hp}){s.colors['end']}")
    elif int((s.hp / s.Mhp) * 100) > 30: s.hpLow = False

    victory = quests.quest(s.stage)
    if victory == 1:
        s.room[s.y][s.x] = s.floor
        s.jpsf = False
        clear(); gbf.play(f'{s.TFP}Packages{s.s}sounds{s.s}clear.wav')
        print(s.colors['G']+s.markdown(1)); t.TextBox(f"   T U T O R I A L   C L E A R !   " if s.stage == 0 else f"   S T A G E   {s.stage}   C L E A R !   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold", animation=["blind", 0.2]); print(s.colors['end'])
        time.sleep(1)
        s.yctuoh = True
        clear()

        mainSettings.upgradeStatus()
        s.yctuoh = False
        clear()
        s.stage += 1
    elif s.hp <= 0 or s.hunger <= 0:
        s.jpsf = False
        clear(); gbf.play(f'{s.TFP}Packages{s.s}sounds{s.s}defeat.wav')
        print(s.colors['R']+s.markdown(1)); t.TextBox(f"   G A M E   O V E R   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold", animation=["blind", 0.2, ]); print(s.colors['end'])
        time.sleep(1)
        s.main = 0
        sys.exit()


mainSettings.init()

while s.main > 0:
    S.stage(s.stage)
    time.sleep(1)
    clear()
    if s.stage == 0:
        gbf.play(f"{s.TFP}Packages{s.s}sounds{s.s}smash.wav")
        t.TextBox(f"{s.markdown(1)}   T U T O R I A L   {s.colors['end']}\n\n", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
        time.sleep(1)
        clear()
        gbf.play(f"{s.TFP}Packages{s.s}sounds{s.s}smash.wav")
        t.TextBox(f"{s.markdown(1)}   T U T O R I A L   {s.colors['end']}\n\n{s.markdown(3)}{s.stageName}{s.colors['end']}", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
    else:
        gbf.play(f"{s.TFP}Packages{s.s}sounds{s.s}smash.wav")
        t.TextBox(f"{s.markdown(1)}   S T A G E   {s.stage}{s.colors['end']}   \n\n", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
        time.sleep(1)
        clear()
        gbf.play(f"{s.TFP}Packages{s.s}sounds{s.s}smash.wav")
        t.TextBox(f"{s.markdown(1)}   S T A G E   {s.stage}{s.colors['end']}   \n\n{s.markdown(3)}{s.stageName}{s.colors['end']}", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
    time.sleep(2)
    gbf.play(f"{s.TFP}Packages{s.s}sounds{s.s}smash.wav")
    clear()
    s.jpsf = True

    while True:
        if s.jpsf:
            gameChecker()
            if s.nowStage < s.stage:
                s.nowStage += 1
                break
            elif s.main <= 0: break
            gbf.fieldPrint()
            time.sleep(1/s.frame)
            clear()
