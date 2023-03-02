# -*- coding: utf-8 -*-
import os, sys, time, random
if os.name == 'nt': s = '\\'
else:               s = '/'
# s = '/' if os.name == "posix" else "\\"
TFP = f'{os.getcwd()}{s}'
try:    exec(open(f'{TFP}Packages{s}downloadModules.py').read())
except: exec(open(f'{TFP}Packages{s}downloadModules.py').read())
import Packages.globalFunctions     as     globalFunctions
from   Packages.modules             import player, rooms, status, stages, quests, selector, Textbox, logger, makeNewListener, mainSettings
from   Packages.globalFunctions     import clear

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
        print(f"{s.markdown([2, 3])}Enter를 한 번 눌러주세요{s.colors['end']}")
        selectStat = selector.selector.Dropdown("올릴 스탯을 선택해주세요", {"체력 증가":"체력의 최대치가 1 증가합니다.", "방어력 증가":"방어력의 최대치가 1 증가합니다.","공격력 증가":"공격력이 1 상승합니다."}, [1,0,255,10], '@')
        if selectStat == 1: s.Mhp += 1
        elif selectStat == 2: s.Mdf += 1
        else: s.atk += 1
        if s.df < s.Mdf: s.df += 1
        if random.randrange(1,4) == 3:
            if s.hp < s.Mhp and s.Mhp - s.hp == 1: s.hp += 1
            elif s.hp < s.Mhp and s.Mhp - s.hp >= 2: s.hp += random.randrange(1,3)
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
