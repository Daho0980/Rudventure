import time
import random
from   Packages.lib.data                    import status
from   Packages.lib.modules                 import cSelector, logger, Textbox
from   Packages.lib.system.globalFunc       import graphic,   system
from   Packages.lib.system.globalFunc.sound import play

s, t = status,  Textbox
grp  = graphic
cc   = s.cColors

def init(stdscr):
    play("smash")
    a, b = [f"{cc['bg'][i]}   " for i in list(cc['bg'].keys())[:8]], [f"{cc['bg'][i]}   " for i in list(cc["bg"].keys())[8:16]]

    system.cinp(
        stdscr,
        "색이 잘 보이는지 확인해주세요:\n"+f"{cc['end']}\n".join(
            [''.join(a), ''.join(b)]
            )+f"{cc['end']}\n\n{cc['fg']['L']}@ 확인{cc['end']}"
        )
    
    play("select")
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
        s.frame = [1, 30, 60, 0][selectFrame-1]; play("smash")

    play("crack")
    grp.addstrMiddle(stdscr, s.LOGO); stdscr.refresh()

    time.sleep(1.5)
    play("crack")
    system.cinp(
        stdscr,
        f"      [ PRESS ENTER ]",
        echo     =False,
        useMiddle=False
        )

    play("select")
    stdscr.clear(); stdscr.refresh()
    grp.addstrMiddle(
        stdscr, 
        t.TextBox(
            f"""TextBox.Middle_{s.cMarkdown(1)}게임 설명{cc['end']}
TextBox.Line
↑, ←, ↓, →  -  화살표 키를 눌러 이동합니다.

{s.p1}  -  당신입니다.
{s.e}  -  방을 돌아다니는 몬스터입니다.
{s.item}  -  아이템 상자입니다. 상호작용 시 구슬 중 하나를 랜덤하게 떨굽니다.
{s.wall}  -  방의 기본 벽입니다. 벽에 부딪히면 방어력 또는 체력이 깎입니다.
{s.floor}  -  바닥입니다. 자유롭게 드나들 수 있습니다.
{s.goal}  -  다음 레벨로 이동하는 곳입니다. 상호작용 시 다음 층으로 갈 수 있습니다.
{s.R}  -  방을 드나들 수 있는 문입니다. 상호작용 시 다른 방으로 갈 수 있습니다.\n
{cc['fg']['R']}hp{cc['end']}      -  체력이 얼마나 남았는지 알려줍니다. 체력 구슬({s.orbs['type']['hp'][0]}, {s.orbs['type']['hp'][1]})을 얻어 회복할 수 있습니다.
{cc['fg']['B1']}def{cc['end']}     -  방어력이 얼마나 남았는지 알려줍니다. 방어력 구슬({s.orbs['type']['def'][0]}, {s.orbs['type']['def'][1]})을 얻어 회복할 수 있습니다.
{cc['fg']['L']}atk{cc['end']}     -  공격력을 표시합니다. 공격력 구슬({s.orbs['type']['atk'][0]}, {s.orbs['type']['atk'][1]})을 얻어 강화할 수 있습니다.
{cc['fg']['Y']}hunger{cc['end']}  -  허기가 얼마나 남았는지 알려줍니다. 허기 구슬({s.orbs['type']['hunger'][0]}, {s.orbs['type']['hunger'][1]})을 얻어 회복할 수 있습니다.
{cc['fg']['F']}curse{cc['end']}   - 당신이 여태까지 받은 저주를 표시합니다. 저주 구슬({s.orbs['type']['exp'][0]}, {s.orbs['type']['exp'][1]})을 얻거나 몬스터를 처치하여 모을 수 있습니다.""",
            Type        ="left",
            fillChar    =" ",
            outDistance =1,
            AMLS        =True,
            endLineBreak=True
            )+"[ PRESS ENTER ]"
        ); stdscr.refresh()
    system.cinp(stdscr, "", echo=False); stdscr.clear(); stdscr.refresh()

    nameChangeCount = 0
    reTryCount      = 0
    while 1:
        play("select")
        if nameChangeCount == 5:
            temporaryName = "이름도 못 정하는 멍청이"
            cSelector.selector.main(
                t.TextBox(
                    f"뇌 빼고 엔터만 치고 계신 것 같으니 특별히\n{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}\n(으)로 정해드리겠습니다. 어때요, 좋죠?",
                    Type        ="middle",
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    addWidth    =3
                    ),
                ["네", "네"],
                [1,0,255,10],
                '@'
            )
            break

        temporaryName = system.cinp(
            stdscr,
            t.TextBox(
                "이름을 입력해주세요",
                Type        ="middle",
                outDistance =1,
                AMLS        =True,
                endLineBreak=True,
                addWidth    =3
                )+f"\n>>>",
                end   =f"{cc['fg']['Y']} ",
                cursor=True
            )
        stdscr.addstr(cc['end']); play("select")
        stdscr.clear(); stdscr.refresh()

        if len(temporaryName) == 0 or len(temporaryName.split()) == 0:
            cSelector.selector.main(
                t.TextBox(
                    f"이름이 {cc['fg']['R']}{s.cMarkdown([2, 3])}없거나{cc['end']} {cc['fg']['R']}{s.cMarkdown([2, 3])}공백 밖에{cc['end']} 없으면\n말하기 곤란해지실게요",
                    Type        ="middle",
                    outDistance =1,
                    AMLS        =True,
                    endLineBreak=True,
                    addWidth    =3
                    ),
                ["네..."],
                [1,0,255,10],
                '@'
            )
            nameChangeCount += 1
            continue

        if len(temporaryName) > 25: temporaryName = temporaryName[:25]+"..."
        
        match cSelector.selector.main(
            t.TextBox(
                f"{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}\n\n이 이름이 맞습니까?",
                Type        ="middle",
                outDistance =1,
                AMLS        =True, 
                endLineBreak=True,
                addWidth    =3
                ),
            ["네", "아니오", "", "그냥 정해주세요..."] if reTryCount >= 3 else ["네", "아니오"],
            [1,0,255,10],
            '@'
        ):
            case 1: break
            case 2: reTryCount += 1; continue
            case 3:
                temporaryName = f"선택장애 {reTryCount-2}호"
                nameSuggestions = cSelector.selector.main(
                    t.TextBox(
                        f"좋습니다. 그럼...\n{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}\n은 어떠신가요?",
                        Type        ="middle",
                        outDistance =1,
                        AMLS        =True,
                        endLineBreak=True,
                        addWidth    =3
                        ),
                    ["네", "그냥 제가 할게요;"],
                    [1,0,255,10],
                    '@'
                )
                if   nameSuggestions == 1: break
                elif nameSuggestions == 2: reTryCount += 1; continue

    s.name, s.lightName = temporaryName, f"{cc['fg']['Y']}{temporaryName}{cc['end']}"
    s.welcomeMessage    = [f"나락에 오신 걸 환영합니다, {s.lightName}님.", 
                        f"오실 때 {cc['fg']['R']}{s.cMarkdown(1)}피자{cc['end']}는 가져오셨죠? 장난입니다, {s.lightName}님.",
                        f"기다리느라 목 빠지는 줄 알았습니다, {s.lightName}님."
                        ]

    logger.addLog(s.welcomeMessage[random.randrange(0, len(s.welcomeMessage))])
    