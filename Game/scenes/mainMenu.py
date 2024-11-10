import os
import curses
from   random import choice

from Game.core.system                 import configs
from Game.core.system.dataLoader      import elm
from Game.scenes                      import checkColor, checkTerminalSize
from Game.utils.advanced.Rudconverter import load
from Game.utils.graphics              import animation, anchor

from Assets.data import (
    totalGameStatus as s,
    UIPreset        as UIP,
    comments        as c,

    color
)
from Game.utils.modules import (
    cSelector as clc,
    Textbox   as t
    )

cc = color.cColors


def setData(data):
    statusData  = data['status']
    commentData = data['comments']

    s.name      = statusData['name']
    s.lightName = f"{cc['fg']['L']}{statusData['name']}{cc['end']}"

    s.hp       = statusData['hp']
    s.df       = statusData['df']
    s.atk      = statusData['atk']
    s.hunger   = statusData['hunger']
    s.xp       = statusData['xp']
    s.lvl      = statusData['lvl']
    s.critDMG  = statusData['critDMG']
    s.critRate = statusData['critRate']
    s.ashChip  = statusData['ashChip']

    s.Mhp  = statusData['Mhp']
    s.Mdf  = statusData['Mdf']
    s.Mxp  = statusData['Mxp']
    s.Mlvl = statusData['Mlvl']

    s.stage     = statusData['stage']
    s.killCount = statusData['killCount']

    s.bodyPreservationMode = statusData['bodyPreservationMode']
    s.ezMode     = statusData["ezMode"]
    s.sanjibaMode = statusData['sanjibaMode']

    s.ids[300]         = statusData['playerIcon']
    s.playerDamageIcon = statusData['playerDamageIcon']
    s.playerColor      = statusData['playerColor']
    s.playerVoice      = statusData['playerVoice']

    s.entityDataMaintained = statusData['entityDataMaintained']
    
    c.lowHpComments               = commentData['lowHpComments']
    c.treasureRoomComments        = commentData['treasureRoomComments']
    c.defeatComments              = commentData['defeatComments']
    c.victoryComments             = commentData['victoryComments']
    c.TIOTAComments               = commentData['TIOTAComments']
    c.collideComments             = commentData['collideComments']
    c.clayModelAnswerComments     = commentData['clayModelAnswerComments']
    c.startComments               = commentData['startComments']
    c.startCommentsWithCowardmode = commentData['startCommentsWithCowardmode']
    c.loadsaveStartComments       = commentData['loadsaveStartComments']
    c.soliloquyComments           = commentData['soliloquyComments']
    c.enterinBattleComments       = commentData['enterinBattleComments']

def main(stdscr) -> None:
    configs.load()
    configs.save()
    s.version = elm(f"{s.TFP}config{s.s}version.json", "version", "string")\
                or "version file is missing!"

    checkColor.main(stdscr)
    checkTerminalSize.main(stdscr)
    y, x = stdscr.getmaxyx()
    animation.Box.forward(stdscr, y-3, x-2, "double")
    while 1:
        mainMenu:int = clc.main(
            UIP.LOGO,
            {
                "나락 입장" : "건투를 빕니다.",
                "운명 인식" : "운명에 갇힌 육신을 선택해 빙의합니다.",
                "설정..."   : "게임에 관련된 설정입니다.",
                "조작법"    : "드... 드리겠습니다!!",
                ""          : "",
                "게임 종료" : "게임을 종료합니다."
            },
            [1,0,255,10],
            '@',
            background=['[fullSizeBox]', '[version]']
        )
        match mainMenu:
            case 1: break
            case 2:
                while 1:
                    try:
                        saveDatas = [d for d in os.listdir(f"{s.TFP}saveData") if d.endswith(".rud")]
                        clcDict   = {}
                        for data in saveDatas:
                            name = data.removesuffix(".rud")
                            clcDict[name] = f"{name}의 봉인된 육신입니다."

                        if clcDict:
                            loadSaveData = clc.main(
                                "<< 운명 인식 >>",
                                clcDict,
                                [1,0,255,10],
                                '@'
                            ); selectedFile = saveDatas[loadSaveData-1]

                            match clc.main(
                                t.TextBox(
                                    f"정말로 이 {cc['fg']['R']}육신{cc['end']}을 선택하시겠습니까?\n\n{cc['fg']['L']}<< {selectedFile.removesuffix('.rud')} >>{cc['end']}",
                                    Type        ="middle",
                                    outDistance =1,
                                    AMLS        =True,
                                    endLineBreak=True,
                                    addWidth    =3
                                ),
                                ["네", "아니오"],
                                [1,0,255,10],
                                '@'
                            ):
                                case 1:
                                    setData(load(selectedFile.removesuffix(".rud")))
                                    s.isLoadfromBody = True
                                    break
                                case 2: continue
                        else:
                            clc.main(
                                t.TextBox(
                                    f"준비된 {cc['fg']['R']}육신{cc['end']}이 없네요 :/",
                                    Type        ="middle",
                                    outDistance =1,
                                    AMLS        =True,
                                    endLineBreak=True,
                                    addWidth    =3
                                ),
                                {"저런..." : "아이고 이런..."},
                                [1,0,255,10],
                                '@'
                            ); break
                    except: break
                if s.name: break
            case 3: 
                while 1:
                    mainSettings:int = clc.main(
                        "<< 설정 >>",
                        {
                            "그래픽 설정...": "전반적인 그래픽을 설정합니다.",
                            "게임 모드..."  : "활성화할 게임 모드를 관리합니다.",
                            "음량 설정..."  : "게임의 음량을 설정합니다.",
                            ""              : "",
                            "완료"          : ""
                        },
                        [1,0,255,10],
                        '@',
                        background=['[fullSizeBox]', '[version]']
                    )
                    match mainSettings:
                        case 1:
                            while 1:
                                graphicSettings = clc.main(
                                    "<< 그래픽 설정 >>",
                                    {
                                        "UI 설정..."     : "게임에 표시될 UI를 설정합니다.",
                                        "프레임 설정..." : "게임 화면의 새로고침 빈도를 설정합니다.",
                                        "터미널 설정..." : "터미널 창의 설정을 관리합니다.",
                                        ""                    : "",
                                        "완료"                : ""
                                    },
                                    [1,0,255,10],
                                    '@',
                                    background=['[fullSizeBox]', '[version]']
                                )
                                match graphicSettings:
                                    case 1:
                                        UISAP = [0, 0]
                                        while 1:
                                            UISettings, UISAP = clc.main(
                                                "<< UI 설정 >>",
                                                {
                                                    f"현재 스탯 UI : {['콤팩트', '코지'][s.statusDesign]}" : "좌상단에 표시될 스탯의 디자인을\n변경합니다.",
                                                    f"디버그 콘솔  : {s.debugConsole}"                      : "우중단에 표시될 디버그 콘솔\n표시 여부입니다.",
                                                    f"맵 표시      : {bool(s.showDungeonMap)}"             : "우상단에 표시될 맵\n표시 여부입니다.",
                                                    ""                                                     : "",
                                                    "완료"                                                 : ""
                                                },
                                                [1,0,255,10],
                                                '@',
                                                setArrowPos   =UISAP,
                                                returnArrowPos=True,
                                                background=[
                                                    anchor(
                                                        stdscr,
                                                        UIP.dungeonMap[s.showDungeonMap],
                                                        x        =stdscr.getmaxyx()[1]-(21 if s.showDungeonMap else 29),
                                                        y        =2,
                                                        returnStr=True
                                                    ),
                                                    anchor(
                                                        stdscr,
                                                        UIP.dungeonMap["introduction"],
                                                        x        =stdscr.getmaxyx()[1]-55,
                                                        y        =13 if s.showDungeonMap else 3,
                                                        returnStr=True
                                                    ),
                                                    anchor(
                                                        stdscr,
                                                        "".join([UIP.status[s.statusDesign],UIP.status["introduction"]]),
                                                        x        =0,
                                                        y        =1,
                                                        addOnyx=[1,0],
                                                        returnStr=True
                                                    ),
                                                    anchor(
                                                        stdscr,
                                                        UIP.debugConsole[s.debugConsole],
                                                        x        =stdscr.getmaxyx()[1]-(34 if s.debugConsole else 38),
                                                        y        =round(stdscr.getmaxyx()[0]/2)-(8 if s.debugConsole else 0),
                                                        returnStr=True
                                                    ),
                                                    anchor(
                                                        stdscr,
                                                        UIP.debugConsole["introduction"],
                                                        x        =stdscr.getmaxyx()[1]-63,
                                                        y        =round(stdscr.getmaxyx()[0]/2)+(7 if s.debugConsole else 1),
                                                        returnStr=True
                                                    ),
                                                    '[version]'
                                                ]
                                            )
                                            match UISettings:
                                                case 1: s.statusDesign   = 0     if s.statusDesign   else 1
                                                case 2: s.debugConsole   = False if s.debugConsole   else True
                                                case 3: s.showDungeonMap = 0     if s.showDungeonMap else 1
                                                case 4:
                                                    configs.save()
                                                    break
                                    case 2:
                                        frameSAP = [0, 0]
                                        while 1:
                                            frameSettings, frameSAP = clc.main(
                                                f"<< 프레임 설정 >>\n\n현재 프레임 : {'MAX' if not s.frameRate else '설정되지 않음' if s.frameRate==-1 else s.frameRate}",
                                                {
                                                    "1프레임"         : "정말로요...?",
                                                    "30프레임 (권장)" : "표준 설정입니다.",
                                                    ""                : "",
                                                    "완료"            : "",
                                                    "60프레임"        : "더 쾌적하게 플레이할 수 있습니다.\n하지만 안타깝게도 눈에 띄는 변화는 찾아볼 수 없겠군요 :(",
                                                    "MAX"             : "최대한 빠르게 새로고침합니다.\n화면이 [심하게] 깜빡거릴 수 있습니다."
                                                },
                                                [1,0,255,10],
                                                '@',
                                                maxLine       =4,
                                                setArrowPos   =frameSAP,
                                                background    =['[fullSizeBox]', '[version]'],
                                                returnArrowPos=True
                                            )
                                            match frameSettings:
                                                case 1|2|4|5:
                                                    s.frameRate = [0,1,30,0,60,0][frameSettings]
                                                    s.frame     = 1/s.frameRate if s.frameRate else 0
                                                case 3:
                                                    configs.save()
                                                    break
                                    case 3:
                                        terminalSAP = [0, 0]
                                        while 1:
                                            terminalScreenSettings, terminalSAP = clc.main(
                                                "<< 터미널 설정 >>",
                                                {
                                                    "터미널 화면 조정..."                           : "게임을 가장 이상적으로 즐기기 위해 \n터미널의 크기를 재조정합니다.",
                                                    f"터미널 크기 확인 : {s.checkTerminalSize}"     : "게임 시작 직후 터미널의 크기를 확인해\n경고 문구를 출력합니다.",
                                                    f"터미널 크기 자동 조정 : {s.autoTerminalSize}" : "게임 시작 시 터미널 크기가 최소 기준보다\n작다면 자동으로 최소 기준으로 설정합니다.",
                                                    ""                                              : "",
                                                    "완료"                                          : ""
                                                },
                                                [1,0,255,10],
                                                '@',
                                                setArrowPos   =terminalSAP,
                                                background    =['[fullSizeBox]', '[version]'],
                                                returnArrowPos=True
                                            )
                                            match terminalScreenSettings:
                                                case 1:
                                                    while 1:
                                                        y, x       = stdscr.getmaxyx()
                                                        screenType = 0 if y<s.sss['minimum'][0] or x<s.sss['minimum'][1] else 1 if s.sss['minimum'][0]<=y<s.sss['recommended'][0] and s.sss['minimum'][1]<=x<s.sss['recommended'][1] else 2
                                                        baseColor  = [cc['fg']['R'], cc['fg']['Y'], cc['fg']['L']][screenType]

                                                        animation.Box.forward(stdscr, y-3, x-2, "double", boxColor=baseColor)
                                                        terminalSizeSettings = clc.main(
                                                            f"""
{[cc['fg']['R']+'터미널 크기의', cc['fg']['Y']+'최소 조건이 충족되었습니다.', cc['fg']['L']+'현재 가장 이상적인 조건을'][screenType]}
{['최소 조건이 충족되지 않았습니다!', '하지만 권장 조건을 충족하려면 여기서 더 늘려야 합니다.', '사용하고 있습니다!'][screenType]}


<< 터미널 화면 조정 >>""",
                                                            [f"{baseColor}완료{cc['end']}", "", f"{baseColor}다시 측정하기{cc['end']}"],
                                                            baseColor,
                                                            '@',
                                                            background=[f"[fullSizeBox]{{'lineType':'double', 'boxColor':'{baseColor}'}}"]
                                                        )
                                                        match terminalSizeSettings:
                                                            case 1: break
                                                            case 2: continue
                                                case 2: s.checkTerminalSize = False if s.checkTerminalSize else True
                                                case 3: s.autoTerminalSize  = False if s.autoTerminalSize  else True
                                                case 4:
                                                    configs.save()
                                                    break
                                    case 4: break
                        case 2:
                            modSAP = [0, 0]
                            while 1:
                                modSettings, modSAP = clc.main(
                                    "<< 게임 모드 >>",
                                    {
                                        f"육신 보존 모드 : {s.bodyPreservationMode}" : [
                                            "활성화 시 스테이지를 클리어할 때마다\n육신 보관소에 육신이 보존됩니다.",
                                            "괜찮아요. 좀만 하다 보면 곧 익숙해질 겁니다."if s.bodyPreservationMode and s.ezMode else"게임에서마저도 죽는 게 두려운가 봐요?"
                                            ][s.bodyPreservationMode],
                                        f"쫄보 모드 : {s.ezMode}" : [
"""활성화 시 모든 편린의 체력이 2 낮아집니다.
또한 확률적으로 편린의 공격을 회피합니다.
심지어 저주 제외 모든 스탯이 100% 상승합니다!
거기에다가 공격력은 특별히 400% 상승합니다!!""",
                                            "이거 완전 쌩 뉴비를 위한 설정이네요.\n이 게임이 처음이신가 봐요?"if s.bodyPreservationMode and s.ezMode else choice(
                                                [
                                                    "\"쫄보 활성화.\"",
                                                    "쫄?",         "아.. 쫄?",
                                                    "큼... 쫄?",   "씁... 쫄?",
                                                    "어으... 쫄?", "어음... 쫄?"
                                                ]
                                            )
                                        ][s.ezMode],
                                        f"산지바 모드 : {s.sanjibaMode}" : [
                                            "활성화 시 모든 나락에서의 편린의 속도가 강화됩니다!",
                                            f"등활지옥에 당도하신 것을 환영합니다, 글라가트로프여."
                                        ][s.sanjibaMode],
                                        ""     : "",
                                        "완료" : ""
                                    },
                                    [1,0,255,10],
                                    '@',
                                    setArrowPos   =modSAP,
                                    background=['[fullSizeBox]', '[version]'],
                                    returnArrowPos=True
                                )
                                match modSettings:
                                    case 1: s.bodyPreservationMode = False if s.bodyPreservationMode else True
                                    case 2: s.ezMode     = False if s.ezMode     else True
                                    case 3: s.sanjibaMode = False if s.sanjibaMode else True
                                    case 4: break
                        case 3:
                            volumeSAP = [0, 0]
                            volumeRate = 1
                            while 1:
                                volumeSettings, volumeSAP = clc.main(
                                    f"<< 음량 설정 >>\n\n현재 음량 : {s.volume}%",
                                    ["+", "", "", "-", "", "", "완료", "", f"음량 변화량 : {volumeRate}"],
                                    [1,0,255,10],
                                    '@',
                                    maxLine       =3,
                                    setArrowPos   =volumeSAP,
                                    background    =['[fullSizeBox]', '[version]'],
                                    returnArrowPos=True,
                                )
                                match volumeSettings:
                                    case 1:
                                        s.volume += volumeRate
                                        if s.volume > 100: s.volume = 100
                                    case 2:
                                        s.volume -= volumeRate
                                        if s.volume < 0: s.volume = 0
                                    case 3:
                                        configs.save()
                                        break
                                    case 4:
                                        volumeRate += 1 if volumeRate < 50 else 0
                        case 4: break
            case 4: clc.main(
                "제작중",
                ["화긴"],
                [1,0,255,10],
                '@',
                background=['[fullSizeBox]', '[version]'],
                )
            case 5:
                animation.Box.reverse(stdscr, y-3, x-2, "double")
                s.main = 0
                curses.endwin()
                exit(1)