import time
from   random import choice

from Assets.data.color       import cColors as cc
from Game.core.system.logger import addLog
from Game.utils              import system
from Game.utils.system       import sound

from Assets.data import (
    totalGameStatus as s,
    UIPreset        as UIP,
    markdown        as md
)
from Game.utils.modules import (
    Textbox as t,

    cSelector
)
from Game.entities.player.statusEffect import (
    addEffect
)


def setIconColor() -> None:
    s.ids[4]   = f"{cc['fg']['Y']}É{cc['end']}"
    s.ids[5]   = f"{cc['fg']['R']}F{cc['end']}"
    s.ids[7]   = f"{cc['fg']['R']}X{cc['end']}"
    s.ids[8]   = f"{cc['fg']['B1']}{md.cMarkdown(1)}O{cc['end']}"
    s.ids[9]   = f"{cc['fg']['B1']}{md.cMarkdown(1)}o{cc['end']}"
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

    s.ids[21] = f"{cc['fg']['O']}☷{cc['end']}"

    s.ids[26] = f"{cc['fg']['M']}X{cc['end']}"
    s.ids[27] = f"{cc['bg']['R']}░{cc['end']}"

    s.ids[300] = f"{cc['fg']['L']}@{cc['end']}" if s.ids[300]=='@'else s.ids[300]
    s.ids[301] = f"{cc['fg']['L']}&{cc['end']}"

    s.ids[400] = f"{cc['fg']['A']}Y{cc['end']}"
    s.ids[401] = f"{cc['fg']['F']}Y{cc['end']}"

    s.ids[501] = f"{cc['fg']['R']}H{cc['end']}"
    s.ids[502] = f"{cc['fg']['B1']}U{cc['end']}"

    s.ids[900] = f"{cc['fg']['G1']};{cc['end']}"

    s.bloodIcon = {
        5 : f"{cc['fg']['R']}██{cc['end']}",
        4 : f"{cc['fg']['R']}█▓{cc['end']}",
        3 : f"{cc['fg']['R']}▓▒{cc['end']}",
        2 : f"{cc['fg']['R']}▒░{cc['end']}",
        1 : f"{cc['fg']['R']}░{cc['end']}" ,
    }

def _setFrame():
    s.frameRate = [1,30,60,120][
        cSelector.main(
        f"{UIP.LOGO}\n를 시작하기 전에, 프레임을 설정해주세요",
        {
            (cc['fg']['R'], "1프레임")  : "도전자를 위한 설정입니다.\n당신의 예측 기술을 뽐내보세요!"             ,
            "30프레임"                  : "권장 수준보다 더 낮은 프레임 설정입니다.\n이전에 표준 설정이기도 했죠.",
            "60프레임"                  : "권장 수준보다 낮은 프레임 설정입니다."                                 ,
            "120프레임(권장)"           : "러드벤처를 플레이하기 위한 권장 설정입니다."
        },
        [1,0,255,10],
        '@)',
        maxLine=2,
        setPos =[1, 1]
        )-1
    ]

def main(stdscr) -> None:
    if not s.frameRate:
        _setFrame()

    s.frame     = (1/s.frameRate)-(0.0017/(s.frameRate//60 or 1))
    s.currFrame = s.frame

    stdscr.clear()
    nameChangeCount = 0
    reTryCount      = 0
    temporaryName   = ""

    while 1:
        if nameChangeCount == 5:
            temporaryName = "이름도 못 정하는 멍청이"
            cSelector.main(
                t.TextBox(
f"""뇌 빼고 엔터만 치고 계신 것 같으니 특별히
{cc['fg']['Y']}<< {temporaryName} >>{cc['end']}
(으)로 정해드리겠습니다. 어때요, 좋죠?""",
                    Type        ="middle",
                    outDistance =1,
                    AMLS        =True,
                    addWidth    =3
                    ),
                ["네", "네 히히"],
                [1,0,255,10],
                '@)',
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
        sound.play   ("system", "selector", "select")
        stdscr.clear (); stdscr.refresh()

        if len(temporaryName) == 0 or len(temporaryName.split()) == 0:
            cSelector.main(
                t.TextBox(
f"이름이 {cc['fg']['R']}{md.cMarkdown([2, 4])}없거나{cc['end']} \
{cc['fg']['R']}{md.cMarkdown([2, 4])}공백 밖에 없으면{cc['end']}\n\
말하기 {cc['fg']['R']}{md.cMarkdown([2, 4])}곤란{cc['end']}해지실게요",
                    Type        ="middle",
                    outDistance =1,
                    AMLS        =True,
                    addWidth    =3
                    ),
                ["네..."],
                [1,0,255,10],
                '@)',
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
            ["네", "아니오", "", "그냥 정해주세요..."]if reTryCount>=3 else["네", "아니오"],
            [1,0,255,10],
            '@)',
            useClear =True,
            killSound=[False, True]
        ):
            case 1:
                match temporaryName.lower():
                    case "레포"|"repo":
                        from Game.pages.character import repo

                        match len(temporaryName):
                            case 2:
                                s.lightName = f"{s.playerColor[0]}{temporaryName[0]}\033[;38;5;220m{temporaryName[1]}{cc['end']}"
                            case 4:
                                s.lightName = f"{s.playerColor[0]}{temporaryName[:2]}\033[;38;5;214m{temporaryName[2]}\033[;38;5;220m{temporaryName[3]}{cc['end']}"

                    case "업로드"|"upload":
                        from Game.pages.character import upload

                        match len(temporaryName):
                            case 3:
                                s.lightName = f"{cc['fg']['W']}{temporaryName[0]}{s.playerColor[0]}{temporaryName[1:]}{cc['end']}"
                            case 6:
                                s.lightName = f"{cc['fg']['W']}{temporaryName[:2]}\033[;38;5;253m{temporaryName[2]}{s.playerColor[0]}{temporaryName[3:]}{cc['end']}"
                    
                    case _: addEffect('0', "∞", merge=False)

                break
            
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
                    '@)',
                )

                if   nameSuggestions == 1: break
                elif nameSuggestions == 2: reTryCount += 1; continue

    s.name      = temporaryName
    s.lightName = s.lightName  or f"{s.playerColor[0]}{temporaryName}{cc['end']}"

    if s.bodyPreservationMode:
        addLog(
            choice([
            f"우쭈쭈, 우리 {md.cMarkdown(2)}겁. 쟁. 이.{cc['end']} {s.lightName}님 오셨군요?",
            f"ㅋ, ㅋㅋㅎ, ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅎㅋㅋㅋㅋㅋㅎㅋㅎㅋ",
            f"전 {cc['fg']['L']}당ㅋ신{cc['end']}이 아ㅋ주 자랑ㅋ스럽습ㅋ니다. {cc['fg']['R']}정말ㅋ로요.{cc['end']}",
            "이런... 티타임이라도 즐기면서 하시려구요?",
            f"{cc['fg']['R']}매{cc['fg']['Y']}니{cc['fg']['B1']}큐{cc['fg']['L']}어{cc['end']}라도 바르고 오시지 그랬어요. {cc['fg']['R']}당신에게 딱{cc['end']}일 텐데 말이죠.",
            f"아, 하하하! 최근에 {cc['fg']['Y']}웃을 일{cc['end']}이 없었는데, 특별히 {cc['fg']['R']}광대가 되어줘서 고맙다{cc['end']}는 말을 해주고 싶네요."
            ]),
            colorKey='Y'
        )

    setIconColor()
    sound.play("soundEffects", "fall", block=True)
    if s.name.lower() in ["레포", "repo"]:
        sound.play("soundEffects", "repo", "vineBoom")
        time.sleep(0.3)
        sound.echo("soundEffects", "repo", "scream", feedback=55)
        time.sleep(2.8)

def presetted() -> None:
    if not s.frameRate:
        _setFrame()

    s.frame     = (1/s.frameRate)-(0.0017/(s.frameRate//60 or 1))
    s.currFrame = s.frame

    setIconColor()
    addLog(
        choice([
            "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
            f"아, 당신이군요ㅋㅋㅋ {cc['fg']['L']}자신감{cc['end']}이 {cc['fg']['R']}너무 없어서{cc['end']} 돌아오신 줄도 몰랐네요.",
            f"그래도 육신을 불러오는 방법은 아시는 것 같아 다행이네요. {cc['fg']['L']}겁쟁이 씨{cc['end']}.",
            f"육신 관리소에 몇 구나 들어차 있는지는 모르겠다만, 그게 {cc['fg']['Y']}마지막{cc['end']}이라면 좋겠네요 ;)",
            f"아, 벌써 죽어서 돌아오신 건가요? 잠깐 잠이나 자려고 했는데... 이렇게나 {cc['fg']['A']}{md.cMarkdown([2, 4])}빠르게{cc['end']} 오실 줄은 몰랐네요."
        ]),
        colorKey='Y'
    )