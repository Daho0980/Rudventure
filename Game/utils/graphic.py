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
import psutil

from Assets.data         import status, lockers
from Assets.data.color   import cColors        as cc
from Game.utils.advanced import DungeonMaker   as dgm
from Game.utils.modules  import Textbox

s, l = status, lockers

escapeAnsi=lambda l:re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('',l)

def addstrMiddle(
        stdscr,
        string:str,
        y:int                    =0,
        x:int                    =0,
        addOnCoordinate:list[int]=[0,0],
        returnEndyx:bool         =False,
        returnStr:bool           =False
        ) -> str: # type: ignore
    lines:list[int] = list(map(lambda l: len(escapeAnsi(l)), string.split("\n")))
    y, x = (y,x)if y+x else map(
        lambda c:c[0]-round([len(lines)/2,max(lines)/2][c[1]]),
        list(zip(map(lambda n:round(n/2),list(stdscr.getmaxyx())),[0,1]))
        )
    y, x = y+addOnCoordinate[0], x+addOnCoordinate[1]
    output:str = ''.join(
        [
            escc for line in zip(
                [f"\033[{x};{_}H" for _ in range(y-1, y+(len(lines)))],
                string.split("\n")
                ) for escc in line
            ]
        )
    if not returnStr: stdscr.addstr(output)

    if       returnEndyx and     returnStr: return output, y+len(string.split("\n")), x # type: ignore
    elif not returnEndyx and     returnStr: return output
    elif     returnEndyx and not returnStr: return y+len(string.split("\n")), x # type: ignore

def showStage(stdscr, stageNum:str, stageName:str):
    """
    `stage`(str)    : 현재 스테이지의 숫자\n
    `stageName`(str): 현재 스테이지의 이름\n
    `sound`(str)    : 스테이지 출력 시 같이 출력될 사운드, 기본적으로 `"smash"`로 설정되어 있음
    """
    addstrMiddle(
        stdscr,
        Textbox.TextBox(
            f"S T A G E   {cc['fg']['R']}{stageNum}{cc['end']}",
            Type        ="middle",
            inDistance  =1,
            outDistance =3,
            AMLS        =True, 
            endLineBreak=True,
            LineType    ="double",
            addWidth    =3
            )
        ); stdscr.refresh()
    time.sleep(1.6)
    stdscr.clear()

    addstrMiddle(
        stdscr,
        Textbox.TextBox(
            f"S T A G E   {cc['fg']['R']}{stageNum}{cc['end']}\n\n{cc['fg']['R']}{stageName}{cc['end']}",
            Type        ="middle",
            inDistance  =1,
            outDistance =3,
            AMLS        =True,
            endLineBreak=True,
            LineType    ="double",
            addWidth    =3
            )
        ); stdscr.refresh()
    time.sleep(1.6)
    stdscr.clear(); stdscr.refresh()

def statusBar(
        status:int,
        statusName:str    ="",
        maxStatus:int     =0,
        color:str         ="",
        emptyCellColor:str="",
        barType:str       ="Normal",
        frontTag:str      ="",
        backTag:str       ="",
        space:int         =1,
        end:bool          =True,
        showComma:bool    =True,
        usePercentage:bool=False, 
        showEmptyCell:bool=True,
    ):
    """
    게이지 바를 생성하는 함수\n\n

        `status`       : 게이지 바에 표시할 스탯\n
        `statusName`   : 게이지 바의 이름이 될 문자열\n
        `maxStatus`    : `status`의 최대치, 기본적으로 `0`으로 설정되어 있음\n
        `color`        : 현재 `status`의 색을 채워줄 매개변수, 기본적으로 `cc['fg']['R']`로 설정되어 있음\n
        `backTag`      : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음\n
        `frontTag`     : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음\n
        `space`        : 이름과 게이지 바 사이에 존재하는 공백, 기본적으로 `1`로 설정되어 있음\n
        `end`          : 맨 끝에 \\n을 하나 더 추가해줌. 기본적으로 `True`로 설정되어 있음\n
        `showComma`    : backTag가 붙을 때 쉼표를 보여줄지에 대한 여부, 기본적으로 `True`로 설정되어 있음\n
        `usePrecentage`: 퍼센테이지를 표시함. 기본적으로 `False`로 설정되어 있음\n
        `showEmptyCell`: 게이지 바 내 비어있는 셀을 출력할지에 대한 여부, 기본적으로 `True`로 설정되어 있음
    """
    color          = cc['fg']['R']  if not color          else color
    emptyCellColor = cc['fg']['G1'] if not emptyCellColor else emptyCellColor

    barTypes:dict[str,list[str]] = {
        "Normal"     : ["[", "]"],
        "Cursed"     : ["<", ">"],
        "OverCursed" : ["{", "}"],
        "Curved"     : ["(", ")"]
    }

    maxStatus = status if not maxStatus else maxStatus

    Display:str          = ""
    spaceLen:str         = " "*space
    statusForDisplay:int = 0

    Display += f"{statusName} :{spaceLen}{frontTag} {barTypes[barType][0]}{color}" if len(statusName) > 0 else f"{spaceLen}{frontTag} {barTypes[barType][0]}{color}"
    if usePercentage:
        status, maxStatus = round((status/maxStatus)*10), 10
    elif not usePercentage: statusForDisplay = maxStatus if status > maxStatus else status
    
    Display += ('|'*statusForDisplay+emptyCellColor+'|'*((maxStatus-statusForDisplay) if showEmptyCell else 0)+f"{cc['end']}{barTypes[barType][1]}")
    if status - maxStatus > 0: Display += f" {color}+{status-maxStatus}{cc['end']}"
    Display += f"{',' if len(backTag)>0 and showComma else ''} {backTag}"+("\n"if end else "")

    return Display

def fieldPrint(stdscr, grid:list):
    """
    메인 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨.
    """
    y, x        = stdscr.getmaxyx()
    Display:str = ""
    buffer:str  = ""
    GFD:list    = list(map(lambda x: ' '.join(map(lambda d: d["block"], x)), grid))
    

    # Map
    if s.showDungeonMap:
        buffer = Textbox.TextBox(
            dgm.gridMapReturn(
                s.Dungeon,
                blank =1,
                center=True
                ),
            Type          ='middle',
            AMLS          =True,
            endLineBreak  =True,
            LineType      ='double',
            sideText      ="Dungeon Map",
            sideTextPos  =["under", "middle"],
            coverSideText=True
            )
        Display += addstrMiddle(stdscr, buffer, y=2, x=x-len(max(buffer.split("\n"))), returnStr=True)

    # Stage
    buffer   = "\n".join(GFD)
    Display += addstrMiddle(
        stdscr,
        buffer,
        y=round(y/2)-round(len(list(map(lambda l: len(escapeAnsi(l)), buffer.split("\n"))))/2),
        x=round(x/2)-(round(max(list(map(lambda l: len(escapeAnsi(l)), GFD)))/2)+1),
        returnStr=True
        )

    # Status
    match s.statusDesign:
        case 0:
            buffer = Textbox.TextBox(
f"""hp : {cc['fg']['R']}{s.hp}/{s.Mhp}{cc['end']} | def : {cc['fg']['B1']}{s.df}/{s.Mdf}{cc['end']}
hunger : {cc['fg']['Y']}{round(s.hunger/10)}%{cc['end']} | atk : {cc['fg']['L']}{s.atk}{cc['end']}
TextBox.Line\n"""+statusBar(
                        int((s.xp/s.Mxp)*10),
                        maxStatus=10,
                        end      =False, # test code
                        color    =cc['fg']['F'],
                        barType  ="Cursed",
                        frontTag =f"{cc['fg']['F']}{s.lvl}{cc['end']}",
                        backTag  =f"{cc['fg']['F']}{s.lvl+1}{cc['end']}",
                        space    =0, # normal = 5
                        showComma=False
                        ),
                Type         ="middle",
                AMLS         =True,
                LineType     ='double',
                sideText     ="Status",
                sideTextPos  =["under", "left"],
                coverSideText=True
            )
        case 1:
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
                        showEmptyCell=False,
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
                        barType  ="Cursed",
                        frontTag =f"{cc['fg']['F']}{s.lvl}{cc['end']}",
                        backTag  =f"{cc['fg']['F']}{s.lvl+1}{cc['end']}",
                        space    =0, # normal = 5
                        showComma=False
                        )
                    ]),
                AMLS         =True,
                LineType     ='double',
                sideText     ="Status",
                sideTextPos  =["under", "left"],
                coverSideText=True
            )
    Display += addstrMiddle(stdscr, buffer, y=2, x=1, returnStr=True)

    # Log
    Display += addstrMiddle(
        stdscr,
        Textbox.TextBox(
            "\n".join(s.onDisplay),
            maxLine        =x-3,
            LineType       ='double',
            alwaysReturnBox=False,
            sideText       ="Log",
            sideTextPos    =["over", "middle"],
            coverSideText  =True
        ),
        y        =y-(1 if not len(s.onDisplay) else len(s.onDisplay)),
        x        =0,
        returnStr=True
    )

    # Debug Mode
    if s.debugScreen:
        by, bx, buffer = Textbox.TextBox(
                f"""Python version : {s.pythonVersion.major}.{s.pythonVersion.minor}.{s.pythonVersion.micro}
Window size : {stdscr.getmaxyx()}
Memory usage : {psutil.Process().memory_info().rss/2**20: .5f} MB
Number of threads : {psutil.Process().num_threads()}

Dx : {s.Dx}, Dy : {s.Dy}, x : {s.x}, y : {s.y}
Number of entities : {s.entityCount}
Number of total entities : {s.totalEntityCount}""",
                Type         ="right",
                AMLS         =True,
                LineType     ="bold",
                returnSizeyx =True,
                sideText     ="Debug",
                sideTextPos  =["over", "right"],
                coverSideText=True
            )
        Display += addstrMiddle(
            stdscr,
            buffer,
            y        =int((y/2)-(by/2)), # type: ignore
            x        =x-bx,
            returnStr=True
        )

    # Pause
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
