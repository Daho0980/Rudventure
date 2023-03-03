# -*- coding: utf-8 -*-
import os, sys, time
from   Packages.lib.data import rooms, status
from   Packages.lib      import quests
s = '\\' if os.name == "nt" else "/"
TFP = f'{os.getcwd()}{s}'
exec(open(f"{TFP}Packages{s}downloadModules.py").read())
from Packages                   import globalFunctions
from Packages.lib               import player, stages
from Packages.lib.system        import mainSettings
from Packages.lib.modules       import Textbox, makeNewListener, logger
from   Packages.globalFunctions import clear

p, r, s, S, S1, gbf, t, mnl= player.player, rooms, status, stages.stages, stages, globalFunctions, Textbox, makeNewListener
s.s    = gbf.slash()
clear()
p.set()


def gameChecker():
    if int((s.hp / s.Mhp) * 100) <= 30 and s.hpLow == False:
        s.hpLow = True
        gbf.play(f"{s.TFP}sounds{s.s}hp_low.wav"); logger.addLog(f"{s.colors['lY']}{s.name}{s.colors['end']} 님의 체력이 부족합니다! {s.colors['R']}(현재 체력 : {s.hp}){s.colors['end']}")
    elif int((s.hp / s.Mhp) * 100) > 30: s.hpLow = False

    victory = quests.quest(s.stage)
    if victory == 1:
        s.room[s.y][s.x] = s.floor
        clear()
        s.jpsf = False
        if s.stage == 0:
            print("T U T O R I A L   C L E A R !")
        else:
            print(f"S T A G E   {s.stage}   C L E A R !")
        gbf.play(f'{s.TFP}sounds{s.s}clear.wav')
        time.sleep(1)
        s.yctuoh = True
        clear()
        mainSettings.upgradeStatus()
        s.yctuoh = False
        clear()
        s.stage += 1
    elif s.hp <= 0 or s.hunger <= 0:
        clear()
        print(f"G A M E   O V E R")
        s.jpsf = False
        s.main = -1
        gbf.play(f'{s.TFP}sounds{s.s}defeat.wav')
        time.sleep(1)
        s.main = 0
        sys.exit()


mainSettings.init()

while s.main > 0:
    S.stage(s.stage)
    time.sleep(1)
    if s.stage == 0: print(t.TextBox(f"{s.markdown(1)}   T U T O R I A L   {s.colors['end']}\n\n{s.markdown(3)}{s.stageName}{s.colors['end']}", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double"))
    else: print(t.TextBox(f"{s.markdown(1)}   S T A G E   {s.stage}{s.colors['end']}   \n\n{s.markdown(3)}{s.stageName}{s.colors['end']}", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double"))
    gbf.play(f"{s.TFP}sounds{s.s}smash.wav")
    time.sleep(2)
    gbf.play(f"{s.TFP}sounds{s.s}smash.wav")
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
