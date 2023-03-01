# -*- coding: utf-8 -*-
import os, sys, time, random
if os.name == 'nt': s = '\\'
else:               s = '/'
# s = '/' if os.name == "posix" else "\\"
TFP = f'{os.getcwd()}{s}'
try:    exec(open(f'{TFP}Packages{s}downloadModules.py').read())
except: exec(open(f'{TFP}Packages{s}downloadModules.py').read())
from   pynput.keyboard              import Key, Listener
import Packages.options             as     options
import Packages.globalFunctions     as     globalFunctions
from   Packages.modules             import player, rooms, status, stages, quests, selector, Textbox, logger, makeNewListener
from   Packages.globalFunctions     import clear

p, r, s, S, S1, gbf, t, mnl= player.player, rooms, status, stages.stages, stages, globalFunctions, Textbox, makeNewListener
s.s    = gbf.slash()
clear()
p.set()


def gameChecker():
    if int((s.hp / s.Mhp) * 100) <= 30 and s.hpLow == False: s.hpLow = True; gbf.play(f"{s.TFP}sounds{s.s}hp_low.wav")
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


try: gbf.play(f'{os.getcwd()}{s.s}Packages{s.s}sounds{s.s}smash.wav')
except: s.TFP = f'{s.s}'; gbf.play(f'{os.getcwd()}{s.s}Packages{s.s}sounds{s.s}smash.wav')
if s.frame == 0:
    selectFrame = selector.selector.Dropdown(f'{s.LOGO}를 시작하기 전에, 프레임을 설정해주세요', {'1프레임':'컨트롤을 포기하겠다는 의지가 느껴집니다.', '30프레임 (권장)':'위쪽 터미널 바가 덜 깜빡거립니다.', '60프레임':'위쪽 터미널 바가 더 깜빡거립니다.'}, [1,0,255,10], '@')
    frames = [1, 30, 60]; s.frame = frames[selectFrame-1]; gbf.play(f'{s.TFP}sounds{s.s}smash.wav')
# gbf.play(f'{s.TFP}sounds{s.s}INTRO_short.wav')
gbf.play(f'{s.TFP}sounds{s.s}crack.wav')
print(s.LOGO)
time.sleep(3.4)
gbf.play(f'{s.TFP}sounds{s.s}crack.wav')
input(f"      __PRESS ENTER__"); gbf.play(f'{s.TFP}sounds{s.s}select.wav'); clear()
input(t.TextBox(f"{s.markdown(1)}게임 설명{s.colors['end']}\nTextBox.Line\n\n↑, ←, ↓, →  -  화살표 키를 눌러 이동합니다.\n\n{s.p1}  -  당신입니다.\n{s.e}  -  방을 돌아다니는 몬스터입니다.\n{s.item}  -  아이템 상자입니다. 허기를 채워주고 체력을 1 또는 2를 회복시켜줍니다.\n{s.wall}  -  방의 기본 벽입니다. 벽에 부딪히면 방어력 또는 체력이 깎입니다.\n{s.floor}  -  빈 공간입니다. 자유롭게 드나들 수 있습니다.\n{s.goal}  -  다음 레벨로 이동하는 곳입니다. 도착 시 다음 레벨로 갈 수 있습니다.\n{s.R}  -  방을 드나들 수 있는 문입니다. 이동시 다른 방으로 갈 수 있습니다.\n\n{s.colors['R']}hp{s.colors['end']}  -  현재 당신의 체력입니다. 스테이지를 깰 때 마다 확률적으로 1씩 회복되며, 최대 체력을 늘릴 수도 있습니다.\n{s.colors['B']}def{s.colors['end']}  -  현재 당신의 방어력입니다. 스테이지를 깰 때 마다 1씩 회복되며, 최대 방어력을 늘릴 수도 있습니다.\n{s.colors['G']}atk{s.colors['end']}  -  당신의 공격력입니다. 스테이지를 깰 때 마다 공격력을 늘릴 수 있습니다.\n{s.colors['lY']}hunger{s.colors['end']}  -  얼마나 움직일 수 있는지 알려줍니다. 아이템 상자를 통해 회복할 수 있습니다.", Type="middle", fillChar=" ", outDistance=1, AMLS=True, endLineBreak=True)+"PRESS ENTER__")
gbf.play(f'{s.TFP}sounds{s.s}select.wav'); clear()

mnl.addListener()

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
