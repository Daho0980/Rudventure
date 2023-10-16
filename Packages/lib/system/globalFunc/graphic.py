"""
Global Functions 중 Graphic 옵션

    ``clear``               : 화면을 모두 정리함, OS에 따라 달라짐
    ``slowLogoPrint``(dead) : 로고를 천천히 출력하기 위해 만든 함수, 현재는 사용하지 않음
    ``endPrint``            : print() 끝에 end 붙이는거 귀찮아서 만듦
    ``statusBar``           : status, maxStatus 매개변수를 주로 활용해 게이지 바를 만들어줌
    ``fieldPrint``          : 인게임 디스플레이 출력 함수
"""
import re
import math, time
from   Packages.lib.data                    import status       as s
from   Packages.lib.modules                 import Textbox
from   Packages.lib.system                  import DungeonMaker as dgm
from   Packages.lib.system.globalFunc.sound import play

def escapeAnsi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def addstrMiddle(stdscr, string:str, y=0, x=0, returnEndyx=False):
    lines = list(map(lambda l: len(escapeAnsi(l)), string.split("\n")))
    if y+x: y, x = y, x
    else:
        y, x = map(lambda n: round(n/2), list(stdscr.getmaxyx()))
        y, x = y-round(len(lines)/2), x-round(max(lines)/2)
    stdscr.addstr(''.join([escc for line in zip([f"\033[{x};{_}H" for _ in range(y-1, y+(len(lines)))], string.split("\n")) for escc in line]))

    if returnEndyx: return y+len(string.split("\n")), x

def showStage(stdscr, stageNum:str, stageName:str, sound:str="smash"):
    """
    `stage`(str)    : 현재 스테이지의 숫자\n
    `stageName`(str): 현재 스테이지의 이름\n
    `sound`(str)    : 스테이지 출력 시 같이 출력될 사운드, 기본적으로 `"smash"`로 설정되어 있음
    """
    play(sound)
    addstrMiddle(
        stdscr,
        Textbox.TextBox(
            f"   S T A G E   {stageNum}   ",
            Type="middle",
            inDistance=1,
            outDistance=3,
            AMLS=True, 
            endLineBreak=True,
            LineType="double"
            )
        ); stdscr.refresh()
    time.sleep(1.6)
    stdscr.clear(); stdscr.refresh(); play(sound)
    addstrMiddle(
        stdscr,
        Textbox.TextBox(
            f"   S T A G E   {stageNum}   \n\n   {stageName}   ",
            Type="middle",
            inDistance=1,
            outDistance=3,
            AMLS=True,
            endLineBreak=True,
            LineType="double"
            )
        ); stdscr.refresh()
    time.sleep(1.6)
    stdscr.clear(); stdscr.refresh(); play(sound)

def statusBar(status:int, statusName:str="", maxStatus:int=0, color=s.cColors['fg']['R'], frontTag:str="", backTag:str="", space:int=1, end=False, showComma=True, usePercentage=False):
    """
    status, maxStatus 매개변수를 주로 활용해 게이지 바를 만들어줌\n

        `status`(int)                               : 현재 status\n
        `statusName`(str)                           : 게이지 바의 이름이 될 문자열\n
        `maxStatus`(int)                            : `status`의 최대치, 기본적으로 `0`으로 설정되어 있음\n
        `color`(s.cColors['fg' 또는 'bg'][색('str')]: 현재 `status`의 색을 채워줄 매개변수, 기본적으로 `s.cColors['fg']['R']`로 설정되어 있음\n
        `backTag`(str)                              : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음\n
        `frontTag`(str)                             : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음\n
        `space`(int)                                : 이름과 게이지 바 사이에 존재하는 공백, 기본적으로 `1`로 설정되어 있음\n
        `end`(bool)                                 : 맨 끝에 \\n을 하나 더 추가해줌. 기본적으로 `False`로 설정되어 있음\n
        `showComma`(bool)                           : backTag가 붙을 때 쉼표를 보여줄지에 대한 여부, 기본적으로 `True`로 설정되어 있음
    """
    Display  = ""
    spaceLen = " "*space
    Display += f"{statusName} :{spaceLen}{frontTag} [{color}" if len(statusName) > 0 else f"{spaceLen}{frontTag} [{color}"
    maxStatus = status if maxStatus == 0 else maxStatus
    if usePercentage == True:
        status = round((status/maxStatus)*10)
        maxStatus = 10
    elif usePercentage == False:
        statusForDisplay = maxStatus if status > maxStatus else status
    
    Display += ("|"*statusForDisplay + s.cColors['fg']['G1'] + "|"*(maxStatus-statusForDisplay) + f"{s.cColors['end']}]")
    if status - maxStatus > 0: Display += f" +{color}{status-maxStatus}{s.cColors['end']}"
    Display += f"{',' if len(backTag)>0 and showComma==True else ''} {backTag}\n"
    if end == True: Display += "\n"

    return Display

def fieldPrint(stdscr, grid:list):
    """
    인게임 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨, 무조건 기입해야 함
    """
    Display = ""
    GFD = list(map(lambda x: ' '.join(x), grid))

    def asciiPrint():
        bars = [
            statusBar(s.hp, statusName="hp", maxStatus=s.Mhp, space=5),
            statusBar(s.df, statusName="def", maxStatus=s.Mdf, color=s.cColors['fg']['B1'], space=4),
            statusBar(math.ceil(s.hunger/50), statusName="hunger",  color=s.cColors['fg']['Y'], backTag=f"{s.cColors['fg']['Y']}{str(s.hunger)}{s.cColors['end']}" if s.hunger <= 50 else f"{s.cColors['fg']['Y']}{round(s.hunger/5)}%{s.cColors['end']}"),
            statusBar(s.atk, statusName="atk", color=s.cColors['fg']['L'], space=4, end=True)
        ]
        return ''.join(bars)
    
    if s.showDungeonMap == 1:
        dungeonMap = Textbox.TextBox(dgm.gridMapReturn(s.Dungeon, blank=1, center=True), Type='middle', fillChar='^', AMLS=True, endLineBreak=True, LineType='double')+"\n\n"
        Display += dungeonMap

    match s.showStateDesign:
        case 1:
            Display += f"hp : {s.cColors['fg']['R']}{s.hp}/{s.Mhp}{s.cColors['end']} | def : {s.cColors['fg']['B1']}{s.df}/{s.Mdf}{s.cColors['end']}\n"
            Display += f"hunger : {s.cColors['fg']['Y']}{(s.hunger/500)*100:0.0f}%{s.cColors['end']} | atk : {s.cColors['fg']['L']}{s.atk}{s.cColors['end']}\n\n"
        case 2: Display += asciiPrint()
        # XP point
    Display += statusBar(
                int((s.xp/s.Mxp)*10),
                maxStatus=10,
                color=s.cColors['fg']['F'],
                frontTag= f"{s.cColors['fg']['F']}{s.lvl}{s.cColors['end']}",
                backTag=f"{s.cColors['fg']['F']}{s.lvl+1}{s.cColors['end']}",
                space=5,
                showComma=False
                )
    Display += "\n".join(GFD)+"\n"
    y, x = map(lambda n: round(n/2), list(stdscr.getmaxyx()))
    y    = y-round(len(list(map(lambda l: len(escapeAnsi(l)), Display.split("\n"))))/2)
    x    = x-round(max(list(map(lambda l: len(escapeAnsi(l)), GFD)))/2)

    for i in s.onDisplay     : Display += f"{i}\n"

    addstrMiddle(stdscr, Display, y=y, x=x)