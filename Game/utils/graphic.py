"""
Global Functions 중 Graphic 옵션

    ``clear``               : 화면을 모두 정리함, OS에 따라 달라짐
    ``slowLogoPrint``(dead) : 로고를 천천히 출력하기 위해 만든 함수, 현재는 사용하지 않음
    ``endPrint``            : print() 끝에 end 붙이는거 귀찮아서 만듦
    ``statusBar``           : status, maxStatus 매개변수를 주로 활용해 게이지 바를 만들어줌
    ``fieldPrint``          : 인게임 디스플레이 출력 함수
"""
import re
import sys
import math, time
from   Assets.data         import status
from   Assets.data         import lockers
from   Game.utils.modules  import Textbox
from   Game.utils.advanced import DungeonMaker as dgm
from   Game.utils.sound    import play

s, l = status, lockers
cc   = s.cColors

escapeAnsi = lambda line: re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('', line)

def addstrMiddle(
        stdscr,
        string:str,
        y:int               =0,
        x:int               =0,
        addOnCoordinate:list=[0,0],
        returnEndyx:bool    =False,
        returnStr:bool      =False
        ):
    lines = list(map(lambda l: len(escapeAnsi(l)), string.split("\n")))
    y, x  = (y, x) if y+x else map(
        lambda c:c[0]-round([len(lines)/2,max(lines)/2][c[1]]),
        list(zip(map(lambda n: round(n/2), list(stdscr.getmaxyx())),[0,1]))
        )
    y, x = y+addOnCoordinate[0], x+addOnCoordinate[1]
    output = ''.join(
        [
            escc for line in zip(
                [f"\033[{x};{_}H" for _ in range(y-1, y+(len(lines)))],
                string.split("\n")
                ) for escc in line
            ]
        )
    if not returnStr: stdscr.addstr(output)

    if       returnEndyx and     returnStr: return output, y+len(string.split("\n")), x
    elif not returnEndyx and     returnStr: return output
    elif     returnEndyx and not returnStr: return y+len(string.split("\n")), x

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
            f"\nS T A G E   {stageNum}\n",
            Type        ="middle",
            outDistance =3,
            AMLS        =True, 
            endLineBreak=True,
            LineType    ="double",
            addWidth    =3
            )
        ); stdscr.refresh()
    time.sleep(1.6)
    stdscr.clear(); stdscr.refresh()
    play(sound)
    addstrMiddle(
        stdscr,
        Textbox.TextBox(
            f"\nS T A G E   {stageNum}\n\n{stageName}\n",
            Type        ="middle",
            outDistance =3,
            AMLS        =True,
            endLineBreak=True,
            LineType    ="double",
            addWidth    =3
            )
        ); stdscr.refresh()
    time.sleep(1.6)
    stdscr.clear(); stdscr.refresh()
    play(sound)

def statusBar(
        status:int,
        statusName:str    ="",
        maxStatus:int     =0,
        color:str         =cc['fg']['R'],
        frontTag:str      ="",
        backTag:str       ="",
        space:int         =1,
        end:bool          =True,
        showComma:bool    =True,
        usePercentage:bool=False, 
        showEmptyCell:bool=True,
    ):
    """
    status, maxStatus 매개변수를 주로 활용해 게이지 바를 만들어줌\n\n

        `status`(int)                               : 현재 status\n
        `statusName`(str)                           : 게이지 바의 이름이 될 문자열\n
        `maxStatus`(int)                            : `status`의 최대치, 기본적으로 `0`으로 설정되어 있음\n
        `color`(cc['fg' 또는 'bg'][색('str')]: 현재 `status`의 색을 채워줄 매개변수, 기본적으로 `cc['fg']['R']`로 설정되어 있음\n
        `backTag`(str)                              : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음\n
        `frontTag`(str)                             : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음\n
        `space`(int)                                : 이름과 게이지 바 사이에 존재하는 공백, 기본적으로 `1`로 설정되어 있음\n
        `end`(bool)                                 : 맨 끝에 \\n을 하나 더 추가해줌. 기본적으로 `True`로 설정되어 있음\n
        `showComma`(bool)                           : backTag가 붙을 때 쉼표를 보여줄지에 대한 여부, 기본적으로 `True`로 설정되어 있음
    """
    Display   = ""
    spaceLen  = " "*space
    maxStatus = status if maxStatus == 0 else maxStatus

    Display += f"{statusName} :{spaceLen}{frontTag} [{color}" if len(statusName) > 0 else f"{spaceLen}{frontTag} [{color}"
    if usePercentage:
        status    = round((status/maxStatus)*10)
        maxStatus = 10
    elif not usePercentage: statusForDisplay = maxStatus if status > maxStatus else status
    
    Display += ('|'*statusForDisplay + cc['fg']['G1'] + '|'*((maxStatus-statusForDisplay) if showEmptyCell else 0) + f"{cc['end']}]")
    if status - maxStatus > 0: Display += f" {color}+{status-maxStatus}{cc['end']}"
    Display += f"{',' if len(backTag)>0 and showComma else ''} {backTag}"
    if end: Display += "\n"

    return Display

def fieldPrint(stdscr, grid:list):
    """
    인게임 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨, 무조건 기입해야 함
    """
    y, x    = stdscr.getmaxyx()
    Display = ""
    buffer  = ""
    GFD     = list(map(lambda x: ' '.join(map(lambda d: d["block"], x)), grid))
    

    # Map
    if s.showDungeonMap:
        buffer = Textbox.TextBox(
            dgm.gridMapReturn(
                s.Dungeon,
                blank =1,
                center=True
                ),
            Type        ='middle',
            AMLS        =True,
            endLineBreak=True,
            LineType    ='double'
            )
        Display += addstrMiddle(stdscr, buffer, y=2, x=x-len(max(buffer.split("\n"))), returnStr=True)

    # Stage
    buffer = "\n".join(GFD)
    Display += addstrMiddle(
        stdscr,
        buffer,
        y=round(y/2)-round(len(list(map(lambda l: len(escapeAnsi(l)), buffer.split("\n"))))/2),
        x=round(x/2)-(round(max(list(map(lambda l: len(escapeAnsi(l)), GFD)))/2)+1),
        returnStr=True
        )

    # Status
    match s.showStateDesign:
        case 1:
            buffer = f"""
hp : {cc['fg']['R']}{s.hp}/{s.Mhp}{cc['end']} | def : {cc['fg']['B1']}{s.df}/{s.Mdf}{cc['end']}
hunger : {cc['fg']['Y']}{round(s.hunger/10)}%{cc['end']} | atk : {cc['fg']['L']}{s.atk}{cc['end']}

"""
        case 2:
            buffer = Textbox.TextBox(
                ''.join([
                    statusBar(s.hp, statusName="hp", maxStatus=s.Mhp, space=5),
                    statusBar(s.df, statusName="def", maxStatus=s.Mdf, color=cc['fg']['B1'], space=4),
                    statusBar(
                        s.atk,
                        statusName   ="atk",
                        maxStatus    =10,
                        color        =cc['fg']['L'],
                        space        =4,
                        showEmptyCell=False
                        ),
                    statusBar(
                        math.ceil(s.hunger/100),
                        statusName="hunger",
                        maxStatus =10,
                        # end       =False,
                        color     =cc['fg']['Y'],
                        backTag   =f"{cc['fg']['Y']}{s.hunger}{cc['end']}" if s.hunger <= 100 else f"{cc['fg']['Y']}{round(s.hunger/10)}%{cc['end']}",
                        ),
                    "TextBox.Line\nTextBox.Middle_"+statusBar(
                        int((s.xp/s.Mxp)*10),
                        maxStatus=10,
                        end      =False, # test code
                        color    =cc['fg']['F'],
                        frontTag =f"{cc['fg']['F']}{s.lvl}{cc['end']}",
                        backTag  =f"{cc['fg']['F']}{s.lvl+1}{cc['end']}",
                        space    =0, # normal = 5
                        showComma=False
                        )
                    ]),
                AMLS     =True,
                LineType ='double'
            )
    Display += addstrMiddle(stdscr, buffer, y=2, x=1, returnStr=True)

    # Log
    Display += addstrMiddle(
        stdscr,
        Textbox.TextBox(
            "\n".join(s.onDisplay),
            AMLS    =True,
            LineType='double'
        ),
        y        =list(stdscr.getmaxyx())[0]-(1 if not len(s.onDisplay) else len(s.onDisplay)),
        x        =0,
        returnStr=True
    )

    if s.debugScreen:
        y, x = stdscr.getmaxyx()
        by, bx, buffer = Textbox.TextBox(
                f"""Python version : {cc['fg']['L']}{sys.version}{cc['end']}
Window size : {cc['fg']['L']}{stdscr.getmaxyx()}{cc['end']}""",
                Type        ="right",
                AMLS        =True,
                LineType    ="bold",
                returnSizeyx=True
            )
        Display += addstrMiddle(
            stdscr,
            buffer,
            y        =y-by,
            x        =x-bx,
            returnStr=True
        )

    if l.pause:
        Display += addstrMiddle(
            stdscr,
            Textbox.TextBox(
                s.pauseText,
                Type    ="middle",
                AMLS    =True,
                LineType="double",
                addWidth=10
                ),
            returnStr=True
            )

    stdscr.erase(); stdscr.addstr(Display)