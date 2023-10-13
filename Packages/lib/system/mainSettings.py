import time
import random
from   Packages.lib.data              import status
from   Packages.lib.modules           import cSelector, logger, Textbox
from   Packages.lib.system.globalFunc import graphic,   sound,  system

s, t     = status,  Textbox
grp, snd = graphic, sound

def init(stdscr):
    snd.play("smash")
    stdscr.addstr("색이 잘 보이는지 확인해주세요:\n")
    for i in list(s.cColors['bg'].keys())[:8]: stdscr.addstr(f"{s.cColors['bg'][i]}   {s.cColors['end']}")
    stdscr.addstr("\n")
    for i in list(s.cColors["bg"].keys())[8:16]: stdscr.addstr(f"{s.cColors['bg'][i]}   {s.cColors['end']}")
    system.cinp(stdscr, f"\n\n{s.cColors['fg']['L']}@ 확인{s.cColors['end']}", echo=False)
    snd.play("select")
    stdscr.clear(); stdscr.refresh()
    
    if s.frame == 0:
        selectFrame = cSelector.selector.main(
            f"{s.LOGO}를 시작하기 전에, 프레임을 설정해주세요",
            {
                "1프레임"         : "컨트롤을 포기하겠다는 의지가 느껴집니다.",
                "30프레임 (권장)" : "위쪽 터미널 바가 덜 깜빡거립니다.",
                "60프레임"        : "30프레임과 큰 차이는 없지만 억까가 줄어들 가능성이 있습니다.",
                "MAX"             : "최대한 빠르게 새로고침합니다. 화면이 [심하게] 깜빡거릴 수 있습니다."
            },
            [1,0,255,10],
            '@'
        )
        s.frame = [1, 30, 60, 0][selectFrame-1]; snd.play("smash")
    snd.play("crack")
    stdscr.addstr(s.LOGO); stdscr.refresh()
    time.sleep(1.5); snd.play("crack")
    system.cinp(stdscr, f"      [ PRESS ENTER ]", echo=False)
    snd.play("select"); stdscr.clear(); stdscr.refresh()
    stdscr.addstr(
        t.TextBox(
            f"{s.cMarkdown(1)}게임 설명{s.cColors['end']}\nTextBox.Line\n\n↑, ←, ↓, →  -  화살표 키를 눌러 이동합니다.\n\n{s.p1}  -  당신입니다.\n{s.e}  -  방을 돌아다니는 몬스터입니다.\n{s.item}  -  아이템 상자입니다. 허기를 채워주고 체력을 1 또는 2를 회복시켜줍니다.\n{s.wall}  -  방의 기본 벽입니다. 벽에 부딪히면 방어력 또는 체력이 깎입니다.\n{s.floor}  -  빈 공간입니다. 자유롭게 드나들 수 있습니다.\n{s.goal}  -  다음 레벨로 이동하는 곳입니다. 도착 시 다음 레벨로 갈 수 있습니다.\n{s.R}  -  방을 드나들 수 있는 문입니다. 이동시 다른 방으로 갈 수 있습니다.\n\n   {s.cColors['fg']['R']}hp{s.cColors['end']}  -  현재 당신의 체력입니다. 스테이지를 깰 때 마다 확률적으로 1씩 회복되며, 최대 체력을 늘릴 수도 있습니다.   \n{s.cColors['fg']['B1']}def{s.cColors['end']}  -  현재 당신의 방어력입니다. 스테이지를 깰 때 마다 1씩 회복되며, 최대 방어력을 늘릴 수도 있습니다.\n{s.cColors['fg']['L']}atk{s.cColors['end']}  -  당신의 공격력입니다. 스테이지를 깰 때 마다 공격력을 늘릴 수 있습니다.\n{s.cColors['fg']['Y']}hunger{s.cColors['end']}  -  얼마나 움직일 수 있는지 알려줍니다. 아이템 상자를 통해 회복할 수 있습니다.",
            Type="middle",
            fillChar=" ",
            outDistance=1,
            AMLS=True,
            endLineBreak=True
            )
        ); stdscr.refresh()
    system.cinp(stdscr, "[ PRESS ENTER ]", echo=False); stdscr.clear(); stdscr.refresh()

    nameChangeCount = 0
    reTryCount      = 0
    while True:
        snd.play("select")
        if nameChangeCount == 5:
            temporaryName = "이름도 못 정하는 멍청이"
            cSelector.selector.main(
                t.TextBox(
                    f"   뇌 빼고 엔터만 치고 계신 것 같으니 특별히   \n{s.cColors['fg']['Y']}<< {temporaryName} >>{s.cColors['end']}\n(으)로 정해드리겠습니다. 어때요, 좋죠?",
                    Type="middle",
                    outDistance=1,
                    AMLS=True,
                    endLineBreak=True
                    ),
                ["네", "네"],
                [1,0,255,10],
                '@'
            )
            break
        temporaryName = system.cinp(stdscr, t.TextBox("   이름을 입력해주세요   ", Type="middle", outDistance=1, AMLS=True, endLineBreak=True)+f"\n>>>", end=f"{s.cColors['fg']['Y']} ", cursor=True); stdscr.addstr(s.cColors['end']); snd.play("select")
        stdscr.clear(); stdscr.refresh()
        if len(temporaryName) == 0 or len(temporaryName.split()) == 0:
            cSelector.selector.main(
                t.TextBox(
                    f"   이름이 {s.cColors['fg']['R']}{s.cMarkdown([2, 3])}없거나{s.cColors['end']} {s.cColors['fg']['R']}{s.cMarkdown([2, 3])}공백 밖에{s.cColors['end']} 없으면   \n말하기 곤란해지실게요",
                    Type="middle",
                    outDistance=1,
                    AMLS=True,
                    endLineBreak=True
                    ),
                ["네..."],
                [1,0,255,10],
                '@'
            )
            nameChangeCount += 1
            continue

        changeNameResolution = cSelector.selector.main(
            t.TextBox(
                f"{s.cColors['fg']['Y']}   << {temporaryName} >>   {s.cColors['end']}\n\n   이 이름이 맞습니까?   ",
                Type="middle",
                outDistance=1,
                AMLS=True, 
                endLineBreak=True
                ),
            ["네", "아니오", "", "그냥 정해주세요..."] if reTryCount >= 3 else ["네", "아니오"],
            [1,0,255,10],
            '@'
        )
        # if changeNameResolution == 2:
        #     reTryName += 1
        #     continue
        match changeNameResolution:
            case 1: break
            case 2: reTryCount += 1; continue
            case 3:
                temporaryName = f"선택장애 {reTryCount-2}호"
                nameSuggestions = cSelector.selector.main(
                    t.TextBox(
                        f"   좋습니다. 그럼...   \n{s.cColors['fg']['Y']}   << {temporaryName} >>   {s.cColors['end']}\n은 어떠신가요?",
                        Type="middle",
                        outDistance=1,
                        AMLS=True,
                        endLineBreak=True
                        ),
                    ["네", "그냥 제가 할게요;"],
                    [1,0,255,10],
                    '@'
                )
                if nameSuggestions == 1: break
                elif nameSuggestions == 2: reTryCount += 1; continue

    s.name, s.lightName = temporaryName, f"{s.cColors['fg']['Y']}{temporaryName}{s.cColors['end']}"
    s.welcomeMessage = [f"나락에 오신 걸 환영합니다, {s.lightName}님.", 
                        f"오실 때 {s.cColors['fg']['R']}{s.cMarkdown(1)}피자{s.cColors['end']}는 가져오셨죠? 장난입니다, {s.lightName}님.",
                        f"기다리느라 목 빠지는 줄 알았습니다, {s.lightName}님."
                        ]

    logger.addLog(s.welcomeMessage[random.randrange(0, len(s.welcomeMessage))])
    