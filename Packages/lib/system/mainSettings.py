import os, time, random
from   Packages.lib.data              import status
from   Packages.lib.modules           import logger, selector, Textbox, makeNewListener
from   Packages.lib.system.globalFunc import sound, graphic

s, t, mnl = status, Textbox, makeNewListener
snd, grp = sound, graphic

def init():
    snd.play("smash")

    if s.frame == 0:
        selectFrame = selector.selector.Dropdown(f'{s.LOGO}를 시작하기 전에, 프레임을 설정해주세요', {"1프레임":"컨트롤을 포기하겠다는 의지가 느껴집니다.", "30프레임 (권장)":"위쪽 터미널 바가 덜 깜빡거립니다.", "60프레임":"30프레임과 큰 차이는 없지만 억까가 줄어들 가능성이 있습니다.", "MAX":"최대한 빠르게 새로고침합니다. 화면이 [심하게] 깜빡거릴 수 있습니다."}, [1,0,255,10], '@')
        frames = [1, 30, 60, 0]; s.frame = frames[selectFrame-1]; snd.play("smash")
    # ----- <LOGO> -----
    snd.play("crack")
    print(s.LOGO)
    time.sleep(1.5)
    snd.play("crack")
    input(f"      __PRESS ENTER__"); snd.play("select"); grp.clear()
    # ----- </LOGO> -----
    print(t.TextBox(f"{s.markdown(1)}게임 설명{s.colors['end']}\nTextBox.Line\n\n↑, ←, ↓, →  -  화살표 키를 눌러 이동합니다.\n\n{s.p1}  -  당신입니다.\n{s.e}  -  방을 돌아다니는 몬스터입니다.\n{s.item}  -  아이템 상자입니다. 허기를 채워주고 체력을 1 또는 2를 회복시켜줍니다.\n{s.wall}  -  방의 기본 벽입니다. 벽에 부딪히면 방어력 또는 체력이 깎입니다.\n{s.floor}  -  빈 공간입니다. 자유롭게 드나들 수 있습니다.\n{s.goal}  -  다음 레벨로 이동하는 곳입니다. 도착 시 다음 레벨로 갈 수 있습니다.\n{s.R}  -  방을 드나들 수 있는 문입니다. 이동시 다른 방으로 갈 수 있습니다.\n\n   {s.colors['R']}hp{s.colors['end']}  -  현재 당신의 체력입니다. 스테이지를 깰 때 마다 확률적으로 1씩 회복되며, 최대 체력을 늘릴 수도 있습니다.   \n{s.colors['B']}def{s.colors['end']}  -  현재 당신의 방어력입니다. 스테이지를 깰 때 마다 1씩 회복되며, 최대 방어력을 늘릴 수도 있습니다.\n{s.colors['G']}atk{s.colors['end']}  -  당신의 공격력입니다. 스테이지를 깰 때 마다 공격력을 늘릴 수 있습니다.\n{s.colors['lY']}hunger{s.colors['end']}  -  얼마나 움직일 수 있는지 알려줍니다. 아이템 상자를 통해 회복할 수 있습니다.", Type="middle", fillChar=" ", outDistance=1, AMLS=True, endLineBreak=True))
    input("PRESS ENTER__"); grp.clear()

    while True:
        snd.play("select")
        temporaryName = input(t.TextBox("   이름을 입력해주세요   ", Type="middle", outDistance=1, AMLS=True, endLineBreak=True)+f"\n>>> {s.colors['lY']}"); snd.play("select"); print(s.colors['end']); grp.clear()
        if len(temporaryName) == 0 or len(temporaryName.split()) == 0: selector.selector.Dropdown(t.TextBox(f"   이름이 {s.colors['R']}{s.markdown([3, 4])}없거나{s.colors['end']} {s.colors['R']}{s.markdown([3, 4])}공백 밖에{s.colors['end']} 없으면   \n말하기 곤란해지실게요", Type="middle", outDistance=1, AMLS=True, endLineBreak=True), ["네..."], [1,0,255,10], '@'); continue
        elif selector.selector.Dropdown(t.TextBox(f"{s.colors['lY']}   << {temporaryName} >>   {s.colors['end']}\n\n   이 이름이 맞습니까?   ", Type="middle", outDistance=1, AMLS=True, endLineBreak=True), ["네", "아니오"], [1,0,255,10], '@') == 2: continue
        break

    s.name, s.lightName = temporaryName, f"{s.colors['lY']}{temporaryName}{s.colors['end']}"
    s.welcomeMessage = [f"나락에 오신 걸 환영합니다, {s.lightName}님.", 
                        f"오실 때 {s.colors['R']}{s.markdown([1, 3])}피자{s.colors['end']}는 가져오셨죠? 장난입니다, {s.lightName}님.",
                        f"기다리느라 목 빠지는 줄 알았습니다, {s.lightName}님."
                        ]
    snd.play("select"); grp.clear()

    logger.addLog(s.welcomeMessage[random.randrange(0, len(s.welcomeMessage))])
    mnl.addListener()
    