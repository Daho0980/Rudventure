import os
import math
import psutil

from Assets.data         import status, lockers
from Assets.data.color   import cColors        as cc
from Game.utils.advanced import DungeonMaker   as dgm
from Game.utils.modules  import Textbox

from Game.utils.graphics import (
    escapeAnsi,
    addstrMiddle,
    checkActualLen
    )


s, l = status, lockers

def statusBar(
        status:int,
        statusName:str    ="",
        maxStatus:int     =0,
        color:str         ="",
        emptyCellColor:str="",
        barType:str       ="Normal",
        frontTag:str      ="",
        backTag:str       ="",
        space:int         =0,
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
    color          = color          or cc['fg']['R']
    emptyCellColor = emptyCellColor or cc['fg']['G1']

    barTypes:dict[str,list[str]] = {
        "Normal" :     ["[", "]"],
        "Cursed" :     ["<", ">"],
        "OverCursed" : ["{", "}"],
        "Curved" :     ["(", ")"]
    }

    maxStatus = maxStatus or status

    Display:list         = []
    spaceLen:str         = " "*space
    statusForDisplay:int = 0

    Display.append(f"{f'{statusName} ' if len(statusName)>0 else ''} {spaceLen}{frontTag} {cc['fg']['G1']}{barTypes[barType][0]}{color}")
    if usePercentage:
        status, maxStatus = round((status/maxStatus)*10), 10
    elif not usePercentage: statusForDisplay = maxStatus if status > maxStatus else status
    
    Display.append(f"{'|'*statusForDisplay+emptyCellColor+'|'*((maxStatus-statusForDisplay) if showEmptyCell else 0)}{cc['fg']['G1']}{barTypes[barType][1]}{cc['end']}")
    if status - maxStatus > 0: Display.append(f" {color}+{status-maxStatus}{cc['end']}")
    Display.append(f"{',' if len(backTag)>0 and showComma else ''} {backTag}"+("\n"if end else ""))

    return ''.join(Display)

def render(stdscr, grid: list):
    """
    메인 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨.
    """
    y, x    = stdscr.getmaxyx()
    Display = []
    buffer  = ""
    GFD     = [' '.join([d["block"] for d in row]) for row in grid]

    # Map
    if s.showDungeonMap:
        buffer = Textbox.TextBox(
            dgm.gridMapReturn(
                s.Dungeon,
                blank =1,
                center=True
            ),
            Type         ='middle',
            AMLS         =True,
            endLineBreak =True,
            LineType     ='double',
            sideText     ="던전 지도",
            sideTextPos  =["under", "middle"],
            coverSideText=True
        )
        Display.append(addstrMiddle(stdscr, buffer, y=2, x=x-checkActualLen(max(buffer.split("\n"))), returnStr=True))

    # Stage
    buffer = "\n".join(GFD)
    Display.append(addstrMiddle(
        stdscr,
        buffer,
        y        =round(y/2)-round(len([len(escapeAnsi(l)) for l in buffer.split("\n")])/2)-(s.y-6) if s.dynamicCameraMoving else round(y/2)-round(len([len(escapeAnsi(l)) for l in buffer.split("\n")])/2),
        x        =round(x/2)-(round(max([len(escapeAnsi(l)) for l in GFD])/2)+1)-(s.x-6)            if s.dynamicCameraMoving else round(x/2)-(round(max([len(escapeAnsi(l)) for l in GFD])/2)+1),
        returnStr=True
    ))

    # Status
    statusText = ""
    if not s.statusDesign:
        statusText = Textbox.TextBox(
f"""체력 : {cc['fg']['R']}{s.hp}/{s.Mhp}{cc['end']} | 방어력 : {cc['fg']['B1']}{s.df}/{s.Mdf}{cc['end']}
허기 : {cc['fg']['Y']}{s.hunger if s.hunger<=100 else f'{round(s.hunger/10)}%'}{cc['end']} | 공격력 : {cc['fg']['L']}{s.atk}{cc['end']}
TextBox.Line_\nTextBox.Left_잿조각  {cc['fg']['G1']}{s.ashChip}{cc['end']}
TextBox.Line_\n"""+statusBar(
            int((s.xp/s.Mxp)*10),
            maxStatus=10,
            end      =False,
            color    =cc['fg']['F'],
            barType  ="Cursed",
            frontTag =f"{cc['fg']['F']}{s.lvl}{cc['end']}",
            backTag  =f"{cc['fg']['F']}{s.lvl+1}{cc['end']}",
            space    =0,  # normal = 5
            showComma=False
        ),
        Type         ="middle",
        AMLS         =True,
        LineType     ='double',
        sideText     ="상태",
        sideTextPos  =["under", "left"],
        coverSideText=True
    )
    elif s.statusDesign == 1:
        statusText = Textbox.TextBox(
            ''.join([
                statusBar(s.hp, statusName="체  력", maxStatus=s.Mhp),
                statusBar(s.df, statusName="방어력", maxStatus=s.Mdf, color=cc['fg']['B1']),
                statusBar(s.atk, statusName="공격력", maxStatus=10, color=cc['fg']['L'], showEmptyCell=False),
                statusBar(math.ceil(s.hunger/100), statusName="허  기", maxStatus=10, color=cc['fg']['Y'],
                          backTag=f"{cc['fg']['Y']}{s.hunger if s.hunger<=100 else f'{round(s.hunger/10)}%'}{cc['end']}"),
                f"TextBox.Line_\n잿조각  {cc['fg']['G1']}{s.ashChip}{cc['end']}\n"
                "TextBox.Line_\nTextBox.Middle_"+statusBar(
                    int((s.xp/s.Mxp)*10),
                    maxStatus=10,
                    end      =False,
                    color    =cc['fg']['F'],
                    barType  ="Cursed",
                    frontTag =f"{cc['fg']['F']}{s.lvl}{cc['end']}",
                    backTag  =f"{cc['fg']['F']}{s.lvl+1}{cc['end']}",
                    showComma=False
                )
            ]),
            AMLS         =True,
            LineType     ='double',
            sideText     ="상태",
            sideTextPos  =["under", "left"],
            coverSideText=True
        )
    Display.append(addstrMiddle(stdscr, statusText, y=2, x=1, returnStr=True))

    # Log
    logText = Textbox.TextBox(
        "\n".join(s.onDisplay),
        maxLine        =x-3,
        LineType       ='double',
        alwaysReturnBox=False,
        sideText       ="로그",
        sideTextPos    =["over", "middle"],
        coverSideText  =True
    )
    Display.append(addstrMiddle(stdscr, logText, y=y-(1 if not len(s.onDisplay) else len(s.onDisplay)), x=0, returnStr=True))

    # Debug Mode
    if s.debugConsole:
        by, bx, debugText = Textbox.TextBox(
            f"""Python version : {s.pythonVersion.major}.{s.pythonVersion.minor}.{s.pythonVersion.micro}
Window size : {stdscr.getmaxyx()}
Memory usage : {psutil.Process().memory_info().rss/2**20: .2f} MB
CPU count : {psutil.cpu_count()}
Number of threads : {psutil.Process().num_threads()}

Dx : {s.Dx}, Dy : {s.Dy}, x : {s.x}, y : {s.y}
Number of entities : {s.entityCount}
Number of total entities : {s.totalEntityCount}""",
            Type         ="right",
            AMLS         =True,
            LineType     ="bold",
            returnSizeyx =True,
            sideText     ="디버그 콘솔",
            sideTextPos  =["over", "right"],
            coverSideText=True
        )
        Display.append(addstrMiddle(stdscr, debugText, y=int((y/2)-(by/2)), x=x-bx, returnStr=True)) # type:ignore

    # Pause
    if l.pause: Display.append(addstrMiddle(stdscr, s.pauseBox, returnStr=True))

    stdscr.erase()
    stdscr.addstr(''.join(Display))