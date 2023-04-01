"""
곧 버려질 불쌍한 코드입니다. 대신해서 울어주세요 ㅠㅠ
"""

# -*- coding: utf-8 -*-
import os, sys, time
player = '\\' if os.name == "nt" else "/"
TFP = f'{os.getcwd()}{player}'
exec(open(f"{TFP}Packages{player}lib{player}system{player}downloadModules.py", encoding='utf8').read())
from Packages.lib.system                   import globalFunctions
from Packages.lib               import player, stages, quests
from Packages.lib.data          import rooms, status
from Packages.lib.system        import mainSettings, DungeonMaker
from Packages.lib.modules       import Textbox, logger, makeNewListener
from Packages.lib.system.globalFunc.graphic   import clear

p, r, player, S, S1, gbf, t, mnl, dgm = player.player, rooms, status, stages.stages, stages, globalFunctions, Textbox, makeNewListener, DungeonMaker
player.s                        = gbf.slash()
player.TFP                      = TFP
clear()
p.set()


def gameChecker():
    if int((player.hp / player.Mhp) * 100) <= 30 and player.hpLow == False:
        player.hpLow = True
        gbf.play(f"{player.TFP}Packages{player.s}sounds{player.s}hp_low.wav"); logger.addLog(f"{player.colors['lY']}{player.name}{player.colors['end']} 님의 체력이 부족합니다! {player.colors['R']}(현재 체력 : {player.hp}){player.colors['end']}")
    elif int((player.hp / player.Mhp) * 100) > 30: player.hpLow = False

    victory = quests.quest(player.stage)
    victory = 0
    if victory == 1:
        player.room[player.y][player.x] = player.floor
        player.jpsf = False
        clear(); gbf.play(f'{player.TFP}Packages{player.s}sounds{player.s}clear.wav')
        print(player.colors['G']+player.markdown(1)); t.TextBox(f"   T U T O R I A L   C L E A R !   " if player.stage == 0 else f"   S T A G E   {player.stage}   C L E A R !   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold", animation=["blind", 0.2]); print(player.colors['end'])
        time.sleep(1)
        player.yctuoh = True
        clear()

        mainSettings.upgradeStatus()
        player.yctuoh = False
        clear()
        player.stage += 1
    elif player.hp <= 0 or player.hunger <= 0:
        player.jpsf = False
        clear(); gbf.play(f'{player.TFP}Packages{player.s}sounds{player.s}defeat.wav')
        print(player.colors['R']+player.markdown(1)); t.TextBox(f"   G A M E   O V E R   ", Type="middle", inDistance=1, outDistance=1, AMLS=True, endLineBreak=True, LineType="bold", animation=["blind", 0.2, ]); print(player.colors['end'])
        time.sleep(1)
        player.main = 0
        sys.exit()


mainSettings.init()

while player.main > 0:
    # S.stage(s.stage)
    player.Dungeon = dgm.DungeonMaker()
    time.sleep(1)
    clear()
    if player.stage == 0:
        gbf.play(f"{player.TFP}Packages{player.s}sounds{player.s}smash.wav")
        t.TextBox(f"{player.markdown(1)}   T U T O R I A L   {player.colors['end']}\n\n", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
        time.sleep(1)
        clear()
        gbf.play(f"{player.TFP}Packages{player.s}sounds{player.s}smash.wav")
        t.TextBox(f"{player.markdown(1)}   T U T O R I A L   {player.colors['end']}\n\n{player.markdown(3)}{player.stageName}{player.colors['end']}", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
    else:
        gbf.play(f"{player.TFP}Packages{player.s}sounds{player.s}smash.wav")
        t.TextBox(f"{player.markdown(1)}   S T A G E   {player.stage}{player.colors['end']}   \n\n", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
        time.sleep(1)
        clear()
        gbf.play(f"{player.TFP}Packages{player.s}sounds{player.s}smash.wav")
        t.TextBox(f"{player.markdown(1)}   S T A G E   {player.stage}{player.colors['end']}   \n\n{player.markdown(3)}{player.stageName}{player.colors['end']}", Type="middle", inDistance=1, outDistance=5, AMLS=True, endLineBreak=True, LineType="double")
    time.sleep(2)
    gbf.play(f"{player.TFP}Packages{player.s}sounds{player.s}smash.wav")
    clear()
    player.jpsf = True

    while True:
        if player.jpsf:
            # gameChecker()
            if player.nowStage < player.stage:
                player.nowStage += 1
                break
            elif player.main <= 0: break
            gbf.fieldPrint(player.room)
            time.sleep(1/player.frame)
            clear()
