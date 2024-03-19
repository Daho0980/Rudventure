import os
import curses
import socket

from Assets.data                       import status, color
from Game.core.system                 import configs
from Game.scenes                      import checkColor
from Game.utils.modules               import cSelector, Textbox
from Game.utils.advanced.Rudconverter import load


s, cc  = status, color.cColors
clc, t = cSelector, Textbox

def setData(data):
    data = data['status']

    s.name           = data['name']
    s.lightName      = f"{cc['fg']['L']}{data['name']}{cc['end']}"
    s.welcomeMessage = data['welcomeMessage']

    s.hp             = data['hp']
    s.df             = data['df']
    s.atk            = data['atk']
    s.hunger         = data['hunger']
    s.xp             = data['xp']
    s.lvl            = data['lvl']
    s.critDMG        = data['critDMG']
    s.critRate       = data['critRate']

    s.Mhp            = data['Mhp']
    s.Mdf            = data['Mdf']
    s.Mxp            = data['Mxp']

    s.stage          = data['stage']
    s.killCount      = data['killCount']

    s.cowardMode     = data['cowardMode']
    s.ezMode         = data["exMode"]
    s.publicMode     = data['publicMode']

def main(stdscr) -> None:
    configs.load()
    
    checkColor.main(stdscr)
    while 1:
        mainMenu:int = clc.main(
            s.LOGO,
            {
                "나락 입장" : "건투를 빕니다.",
                "운명 인식" : "운명에 갇힌 육신을 선택해 빙의합니다.",
                "설정..."   : "게임에 관련된 설정입니다.",
                "조작법"    : "드... 드리겠습니다!!",
                ""          : "",
                "게임 종료" : "게임을 종료합니다."
            },
            [1,0,255,10],
            '@'
        )
        match mainMenu:
            case 1: break
            case 2:
                while 1:
                    try:
                        saveDatas = [d for d in os.listdir(f"{s.TFP}saveData") if d.endswith(".rud")]
                        clcDict   = {}
                        for data in saveDatas:
                            name = data.rstrip(".rud")
                            clcDict[name] = f"{name}의 봉인된 육신입니다."

                        if clcDict:
                            loadSavedData = clc.main(
                                "<< 운명 인식 >>",
                                clcDict,
                                [1,0,255,10],
                                '@'
                            ); selectedFile = saveDatas[loadSavedData-1]

                            match clc.main(
                                t.TextBox(
                                    f"정말로 이 {cc['fg']['R']}육신{cc['end']}을 선택하시겠습니까?\n\n{cc['fg']['L']}<< {selectedFile.rstrip('.rud')} >>{cc['end']}",
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
                                    setData(load(selectedFile.rstrip(".rud")))
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
                if s.name != "": break
            case 3: 
                while 1:
                    mainSettings:int = clc.main(
                        "<< 설정 >>",
                        {
                            "UI 설정..."    : "게임에 표시될 UI를 설정합니다.",
                            "프레임 설정...": "게임 화면의 새로고침 빈도를 설정합니다.",
                            "게임 모드..."  : "활성화할 게임 모드를 관리합니다.",
                            ""              : "",
                            "완료"          : ""
                        },
                        [1,0,255,10],
                        '@'
                    )
                    match mainSettings:
                        case 1:
                            while 1:
                                UISettings:int = clc.main(
                                    "<< UI 설정 >>",
                                    {
                                        f"현재 스탯 UI : {['콤팩트', '코지'][s.statusDesign]}" : "좌상단에 표시될 스탯의 디자인을 변경합니다.\n인게임에서 Shift + s 키로 변경할 수 있습니다.",
                                        f"디버그 모드  : {s.debugScreen}"                      : "우중단에 표시될 디버그 스크린 표시 여부입니다.\n인게임에서 Shift + d 키로 변경할 수 있습니다.",
                                        f"맵 표시      : {bool(s.showDungeonMap)}"             : "우상단에 표시될 던전 맵 표시 여부입니다.\n인게임에서 Tab키로 변경할 수 있습니다.",
                                        ""                                                     : "",
                                        "완료"                                                 : ""
                                    },
                                    [1,0,255,10],
                                    '@'
                                )
                                match UISettings:
                                    case 1: s.statusDesign = 0     if s.statusDesign   else 1
                                    case 2: s.debugScreen  = False if s.debugScreen    else True
                                    case 3: s.showDungeonMap = 0   if s.showDungeonMap else 1
                                    case 4:
                                        configs.save()
                                        break
                        case 2:
                            while 1:
                                frameSettings = clc.main(
                                    f"<< 프레임 설정 >>\n\n현재 프레임 : {'MAX' if not s.frameRate else '설정되지 않음' if s.frameRate==-1 else s.frameRate}",
                                    {
                                        "1프레임"         : "정말로요...?",
                                        "30프레임 (권장)" : "표준 설정입니다.",
                                        "60프레임"        : "더 쾌적하게 플레이할 수 있습니다.\n하지만 안타깝게도 눈에 띄는 변화는 찾아볼 수 없겠군요 :(",
                                        "MAX"             : "최대한 빠르게 새로고침합니다.\n화면이 [심하게] 깜빡거릴 수 있습니다.",
                                        ""                : "",
                                        "완료"            : ""
                                    },
                                    [1,0,255,10],
                                    '@',
                                    maxLine=3
                                )
                                match frameSettings:
                                    case 1|2|3|4:
                                        s.frameRate = [0,1,30,60,0][frameSettings]
                                        s.frame     = 1/s.frameRate if s.frameRate else 0
                                    case 5:
                                        configs.save()
                                        break
                        case 3:
                            while 1:
                                modeSettings:int = clc.main(
                                    "<< 게임 모드 >>",
                                    {
                                        f"겁쟁이 모드 : {s.cowardMode}" : [
                                            "활성화 시 스테이지를 클리어할 때마다\n세이브 데이터가 저장됩니다.",
                                            "게임에서마저도 죽는 게 두려운가 봐요?"][s.cowardMode],
                                        f"정 말쉬운모 드 : {s.ezMode}" : [
                                            "활성화 시 모든 편린의 체력이 2 낮아집니다.\n또한 확률적으로 편린의 공격을 회피합니다.\n심지어 저주 제외 모든 스탯이 100% 상승합니다!\n거기에다가 공격력은 특별히 400% 상승합니다!!",
                                            "\"갓 난 뉴비 활성화.\""
                                        ][s.ezMode],
                                        f"\"일 반 인\" 모드 : {s.publicMode}" : [
                                            "활성화 시 모든 편린의 쿨타임이 절반으로 줄어듭니다!",
                                            f"일반인의 세계에 오신 것을 환영합니다,\n{socket.gethostname()}."
                                        ][s.publicMode],
                                        ""     : "",
                                        "완료" : ""
                                    },
                                    [1,0,255,10],
                                    '@'
                                )
                                match modeSettings:
                                    case 1: s.cowardMode = False if s.cowardMode else True
                                    case 2: s.ezMode     = False if s.ezMode     else True
                                    case 3: s.publicMode = False if s.publicMode else True
                                    case 4: break
                        case 4: break
            case 4: clc.main("제작중", ["화긴"], [1,0,255,10], '@')
            case 5:
                s.main = 0
                curses.endwin()
                exit(1)