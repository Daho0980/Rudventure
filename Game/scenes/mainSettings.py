import random

from Assets.data             import status            as s
from Assets.data.color       import cColors           as cc
from Game.core.system        import logger
from Game.utils              import system
from Game.utils.modules      import cSelector, Textbox
from Game.utils.system.sound import play


t = Textbox

def setIconColor() -> None:
    s.ids[4]   = f"{cc['fg']['Y']}É{cc['end']}"
    s.ids[5]   = f"{cc['fg']['R']}F{cc['end']}"
    s.ids[7]   = f"{cc['fg']['R']}X{cc['end']}"
    s.ids[8]   = f"{cc['fg']['B1']}{s.cMarkdown(1)}O{cc['end']}"
    s.ids[9]   = f"{cc['fg']['B1']}{s.cMarkdown(1)}o{cc['end']}"
    s.ids[10]  = f"{cc['fg']['R']}o{cc['end']}"
    s.ids[11]  = f"{cc['fg']['B1']}q{cc['end']}"
    s.ids[12]  = f"{cc['fg']['L']}v{cc['end']}"
    s.ids[13]  = f"{cc['fg']['Y']}o{cc['end']}"
    s.ids[14]  = f"{cc['fg']['F']}ø{cc['end']}"
    s.ids[15]  = f"{cc['fg']['R']}O{cc['end']}"
    s.ids[16]  = f"{cc['fg']['B1']}Q{cc['end']}"
    s.ids[17]  = f"{cc['fg']['L']}V{cc['end']}"
    s.ids[18]  = f"{cc['fg']['Y']}O{cc['end']}"
    s.ids[19]  = f"{cc['fg']['F']}Ø{cc['end']}"
    s.ids[21]  = f"{cc['fg']['O']}☲{cc['end']}"
    s.ids[300] = f"{cc['fg']['L']}@{cc['end']}"
    s.ids[301] = f"{cc['fg']['L']}&{cc['end']}"
    s.ids[400] = f"{cc['fg']['A']}Y{cc['end']}"
    s.ids[401] = f"{cc['fg']['F']}Y{cc['end']}"
    s.ids[900] = f"{cc['fg']['G1']};{cc['end']}"

def main(stdscr) -> None:
    if s.frame == -1:
        frameSettings = cSelector.main(
            f"{s.LOGO}\n를 시작하기 전에, 프레임을 설정해주세요",
            {
                "1프레임"         : "정말로요...?",
                "30프레임 (권장)" : "표준 설정입니다.",
                "60프레임"        : "더 쾌적하게 플레이할 수 있습니다.\n하지만 안타깝게도 눈에 띄는 변화는 찾아볼 수 없겠군요 :(",
                "MAX"             : "최대한 빠르게 새로고침합니다.\n화면이 [심하게] 깜빡거릴 수 있습니다."
            },
            [1,0,255,10],
            '@',
            maxLine=2
        )
        s.frameRate = [0,1,30,60,0][frameSettings]
        s.frame     = 1/s.frameRate if s.frameRate else 0

    stdscr.clear()
#     grp.addstrMiddle(
#         stdscr, 
#         t.TextBox(
#             f"""TextBox.Middle_{s.cMarkdown(1)}게임 설명{cc['end']}
# TextBox.Line
# ↑, ←, ↓, →  -  화살표 키를 눌러 이동합니다.

# {s.p1}  -  당신입니다.
# {s.e}  -  방을 돌아다니는 몬스터입니다.
# {s.item}  -  아이템 상자입니다. 상호작용 시 구슬 중 하나를 랜덤하게 떨굽니다.
# {s.wall}  -  방의 기본 벽입니다. 벽에 부딪히면 방어력 또는 체력이 깎입니다.
# {s.floor}  -  바닥입니다. 자유롭게 드나들 수 있습니다.
# {s.goal}  -  다음 레벨로 이동하는 곳입니다. 상호작용 시 다음 층으로 갈 수 있습니다.
# {s.R}  -  방을 드나들 수 있는 문입니다. 상호작용 시 다른 방으로 갈 수 있습니다.\n
# {cc['fg']['R']}hp{cc['end']}      -  체력이 얼마나 남았는지 알려줍니다. 체력 구슬({s.orbs['type']['hp'][0]}, {s.orbs['type']['hp'][1]})을 얻어 회복할 수 있습니다.
# {cc['fg']['B1']}def{cc['end']}     -  방어력이 얼마나 남았는지 알려줍니다. 방어력 구슬({s.orbs['type']['def'][0]}, {s.orbs['type']['def'][1]})을 얻어 회복할 수 있습니다.
# {cc['fg']['L']}atk{cc['end']}     -  공격력을 표시합니다. 공격력 구슬({s.orbs['type']['atk'][0]}, {s.orbs['type']['atk'][1]})을 얻어 강화할 수 있습니다.
# {cc['fg']['Y']}hunger{cc['end']}  -  허기가 얼마나 남았는지 알려줍니다. 허기 구슬({s.orbs['type']['hunger'][0]}, {s.orbs['type']['hunger'][1]})을 얻어 회복할 수 있습니다.
# {cc['fg']['F']}curse{cc['end']}   - 당신이 여태까지 받은 저주를 표시합니다. 저주 구슬({s.orbs['type']['exp'][0]}, {s.orbs['type']['exp'][1]})을 얻거나 몬스터를 처치하여 모을 수 있습니다.""",
#             Type        ="left",
#             fillChar    =" ",
#             outDistance =1,
#             AMLS        =True,
#             endLineBreak=True
#             )+"[ PRESS ENTER ]"
#         ); stdscr.refresh()
#     system.cinp(stdscr, "", echo=False); stdscr.clear(); stdscr.refresh()

    nameChangeCount:int = 0
    reTryCount:int      = 0
    temporaryName:str   = ""
    while 1:
        if nameChangeCount == 5:
            temporaryName = "이름도 못 정하는 멍청이"
            cSelector.main(
                t.TextBox(
                    f"뇌 빼고 엔터만 치고 계신 것 같으니 특별히\n{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}\n(으)로 정해드리겠습니다. 어때요, 좋죠?",
                    Type        ="middle",
                    outDistance =1,
                    AMLS        =True,
                    addWidth    =3
                    ),
                ["네", "네 히히"],
                [1,0,255,10],
                '@',
            )
            break

        y,x = map(lambda n:n,stdscr.getmaxyx())
        y,x = (y-2,x-3)
        stdscr.clear()
        temporaryName = system.cinp(
            stdscr,
            """┌─────────────────────────┐
│   이름을 입력해주세요   │
└─────────────────────────┘

>>>""",
                end    =f"{cc['fg']['Y']} ",
                cursor =True
            )
        stdscr.addstr(cc['end'])
        play("system", "selector", "select")
        stdscr.clear(); stdscr.refresh()

        if len(temporaryName) == 0 or len(temporaryName.split()) == 0:
            cSelector.main(
                t.TextBox(
                    f"이름이 {cc['fg']['R']}{s.cMarkdown([2, 3])}없거나{cc['end']} {cc['fg']['R']}{s.cMarkdown([2, 3])}공백 밖에 없으면{cc['end']}\n말하기 {cc['fg']['R']}{s.cMarkdown([2, 3])}곤란{cc['end']}해지실게요",
                    Type        ="middle",
                    outDistance =1,
                    AMLS        =True,
                    addWidth    =3
                    ),
                ["네..."],
                [1,0,255,10],
                '@',
            )
            nameChangeCount += 1
            continue

        if len(temporaryName) > 25: temporaryName = temporaryName[:25]+"..."
        
        match cSelector.main(
            t.TextBox(
                f"{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}\n\n이 이름이 맞습니까?",
                Type        ="middle",
                outDistance =1,
                AMLS        =True,
                addWidth    =3
                ),
            ["네", "아니오", "", "그냥 정해주세요..."] if reTryCount >= 3 else ["네", "아니오"],
            [1,0,255,10],
            '@',
        ):
            case 1: break
            case 2: reTryCount += 1; continue
            case 3:
                temporaryName = f"선택장애 {reTryCount-2}호"
                nameSuggestions = cSelector.main(
                    t.TextBox(
                        f"좋습니다. 그럼...\n{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}\n는 어떠신가요?",
                        Type        ="middle",
                        outDistance =1,
                        AMLS        =True,
                        addWidth    =3
                        ),
                    ["네", "그냥 제가 할게요;"],
                    [1,0,255,10],
                    '@',
                )
                if   nameSuggestions == 1: break
                elif nameSuggestions == 2: reTryCount += 1; continue

    s.name, s.lightName = temporaryName, f"{cc['fg']['L']}{temporaryName}{cc['end']}"
    s.welcomeMessage    = [
        f"우쭈쭈, 우리 {s.cMarkdown(2)}겁. 쟁. 이.{cc['end']} {s.lightName}님 오셨군요?",
        f"ㅋ, ㅋㅋㅎ, ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅎㅋㅋㅋㅋㅋㅎㅋㅎㅋ",
        f"전 {cc['fg']['L']}당ㅋ신{cc['end']}이 아ㅋ주 자랑ㅋ스럽습ㅋ니다. {cc['fg']['R']}정말ㅋ로요.{cc['end']}"
    ]if s.ezMode else [
        f"나락에 오신 걸 환영합니다, {s.lightName}님.", 
        f"오실 때 {cc['fg']['R']}{s.cMarkdown(1)}피자{cc['end']}는 가져오셨죠? 장난입니다, {s.lightName}님.",
        f"기다리느라 목 빠지는 줄 알았습니다, {s.lightName}님."
    ]
    setIconColor()
    logger.addLog(random.choice(s.welcomeMessage))

def presetted(stdscr) -> None:
    if s.frame == -1:
        frameSettings = cSelector.main(
            f"{s.LOGO}\n를 시작하기 전에, 프레임을 설정해주세요",
            {
                "1프레임"         : "정말로요...?",
                "30프레임 (권장)" : "표준 설정입니다.",
                "60프레임"        : "더 쾌적하게 플레이할 수 있습니다.\n하지만 안타깝게도 눈에 띄는 변화는 찾아볼 수 없겠군요 :(",
                "MAX"             : "최대한 빠르게 새로고침합니다.\n화면이 [심하게] 깜빡거릴 수 있습니다."
            },
            [1,0,255,10],
            '@',
            maxLine=2,
        )
        s.frameRate = [0,1,30,60,0][frameSettings]
        s.frame     = 1/s.frameRate if s.frameRate else 0
    setIconColor()
    logger.addLog(random.choice(s.welcomeMessage))