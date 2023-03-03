import os, time, random
from   Packages             import globalFunctions                            as gbf
from Packages.lib.data      import status
from   Packages.lib.modules import selector, Textbox, logger, makeNewListener

s, t, mnl = status, Textbox, makeNewListener

def init():
    try: gbf.play(f'{os.getcwd()}{s.s}Packages{s.s}sounds{s.s}smash.wav')
    except: s.TFP = f'{s.s}'; gbf.play(f'{os.getcwd()}{s.s}Packages{s.s}sounds{s.s}smash.wav')
    if s.frame == 0:
        selectFrame = selector.selector.Dropdown(f'{s.LOGO}를 시작하기 전에, 프레임을 설정해주세요', {'1프레임':'컨트롤을 포기하겠다는 의지가 느껴집니다.', '30프레임 (권장)':'위쪽 터미널 바가 덜 깜빡거립니다.', '60프레임':'위쪽 터미널 바가 더 깜빡거립니다.'}, [1,0,255,10], '@')
        frames = [1, 30, 60]; s.frame = frames[selectFrame-1]; gbf.play(f'{s.TFP}sounds{s.s}smash.wav')
    gbf.play(f'{s.TFP}sounds{s.s}crack.wav')
    print(s.LOGO)
    time.sleep(1.5)
    gbf.play(f'{s.TFP}sounds{s.s}crack.wav')
    input(f"      __PRESS ENTER__"); gbf.play(f'{s.TFP}sounds{s.s}select.wav'); gbf.clear()
    input(t.TextBox(f"{s.markdown(1)}게임 설명{s.colors['end']}\nTextBox.Line\n\n↑, ←, ↓, →  -  화살표 키를 눌러 이동합니다.\n\n{s.p1}  -  당신입니다.\n{s.e}  -  방을 돌아다니는 몬스터입니다.\n{s.item}  -  아이템 상자입니다. 허기를 채워주고 체력을 1 또는 2를 회복시켜줍니다.\n{s.wall}  -  방의 기본 벽입니다. 벽에 부딪히면 방어력 또는 체력이 깎입니다.\n{s.floor}  -  빈 공간입니다. 자유롭게 드나들 수 있습니다.\n{s.goal}  -  다음 레벨로 이동하는 곳입니다. 도착 시 다음 레벨로 갈 수 있습니다.\n{s.R}  -  방을 드나들 수 있는 문입니다. 이동시 다른 방으로 갈 수 있습니다.\n\n{s.colors['R']}hp{s.colors['end']}  -  현재 당신의 체력입니다. 스테이지를 깰 때 마다 확률적으로 1씩 회복되며, 최대 체력을 늘릴 수도 있습니다.\n{s.colors['B']}def{s.colors['end']}  -  현재 당신의 방어력입니다. 스테이지를 깰 때 마다 1씩 회복되며, 최대 방어력을 늘릴 수도 있습니다.\n{s.colors['G']}atk{s.colors['end']}  -  당신의 공격력입니다. 스테이지를 깰 때 마다 공격력을 늘릴 수 있습니다.\n{s.colors['lY']}hunger{s.colors['end']}  -  얼마나 움직일 수 있는지 알려줍니다. 아이템 상자를 통해 회복할 수 있습니다.", Type="middle", fillChar=" ", outDistance=1, AMLS=True, endLineBreak=True)+"PRESS ENTER__"); gbf.clear()
    while True:
        gbf.play(f'{s.TFP}sounds{s.s}select.wav')
        temporaryName = input(t.TextBox("   이름을 입력해주세요   ", Type="middle", outDistance=1, AMLS=True, endLineBreak=True)+f"\n>>> {s.colors['lY']}"); gbf.play(f'{s.TFP}sounds{s.s}select.wav'); print(s.colors['end']); gbf.clear()
        if selector.selector.Dropdown(t.TextBox(f"{s.colors['lY']}<< {temporaryName} >>{s.colors['end']}\n   이 이름이 맞습니까?   ", Type="middle", outDistance=1, AMLS=True, endLineBreak=True), ["네", "아니오"], [1,0,255,10], '@') == 2: continue
        break
    s.name, s.lightName = temporaryName, f"{s.colors['lY']}{temporaryName}{s.colors['end']}"
    s.welcomeMessage = [f"나락에 오신 걸 환영합니다, {s.lightName}.", f"오실 때 {s.colors['R']}{s.markdown([1, 3])}피자{s.colors['end']}는 가져오셨죠? 장난입니다, {s.lightName}."]
    gbf.play(f'{s.TFP}sounds{s.s}select.wav'); gbf.clear()

    if random.randrange(0, 4) == 1: logger.addLog(s.welcomeMessage[1], 8)
    else: logger.addLog(s.welcomeMessage[0], 8)
    mnl.addListener()

def upgradeStatus():
    print(f"{s.markdown([2, 3])}Enter를 한 번 눌러주세요{s.colors['end']}")
    selectStat = selector.selector.Dropdown("올릴 스탯을 선택해주세요", {"체력 증가":"체력의 최대치가 1 증가합니다.", "방어력 증가":"방어력의 최대치가 1 증가합니다.","공격력 증가":"공격력이 1 상승합니다."}, [1,0,255,10], '@')
    if selectStat == 1:
        s.Mhp += 1
        if s.Mhp < s.hp: s.hp += 1
    elif selectStat == 2:
        s.Mdf += 1
        if s.Mdf < s.df: s.df += 1
    else: s.atk += 1
    
    if random.randrange(1,4) == 3:
        if s.hp < s.Mhp and s.Mhp - s.hp == 1: s.hp += 1
        elif s.hp < s.Mhp and s.Mhp - s.hp >= 2: s.hp += random.randrange(1,3)

    if s.Mdf < s.df: s.df += 1