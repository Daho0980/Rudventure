import math
import time
import psutil
from   random import randrange, choices, choice

from Assets.data.color           import cColors as cc
from Game.core.system.structures import Conveyor
from Game.utils.advanced         import DungeonMaker as dgm
from Game.utils.modules          import Textbox

from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    UIPreset        as UIP,
    lockers         as l
)
from . import (
    escapeAnsi,
    actualLen,
    anchor
)


noiseBuffer = ""

logCache:Conveyor = Conveyor(1, True)

s.startTime         = time.perf_counter()

def statusBar(status:int,
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
              showEmptyCell:bool=True,    ):
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
        "FairWind" :   ["{", "}"],
        "Curved" :     ["(", ")"]
    }

    maxStatus = maxStatus or status

    Display:list         = []
    spaceLen:str         = " "*space
    statusForDisplay:int = 0

    Display.append(f"{f'{statusName} ' if len(statusName)>0 else ''} {spaceLen}{frontTag} {cc['fg']['G1']}{barTypes[barType][0]}{color}")
    if usePercentage:
        status, maxStatus = round((status/maxStatus)*10), 10
    elif not usePercentage: statusForDisplay = maxStatus if status>maxStatus else status
    
    Display.append(f"{'|'*statusForDisplay+emptyCellColor+'|'*((maxStatus-statusForDisplay) if showEmptyCell else 0)}{cc['fg']['G1']}{barTypes[barType][1]}{cc['end']}")
    if status-maxStatus > 0: Display.append(f" {color}+{status-maxStatus}{cc['end']}")
    Display.append(f"{',' if len(backTag)>0 and showComma else ''} {backTag}"+("\n"if end else ""))

    return ''.join(Display)

def inventory():
    step   = [[0, 3], [1, 4], [2, 5]]
    output = []

    for cellColumn in step:
        lines = []
        for cellIndex in cellColumn:
            if cellIndex<len(s.inventory['cells']):
                cell = Textbox.TextBox(
                    ' ' if not s.inventory['cells'][cellIndex]['item'] else s.inventory['cells'][cellIndex]['block'],
                    maxLine    =3,
                    Type       ="middle",
                    LineType   ="bold",
                    sideText   =str(cellIndex+1),
                    sideTextPos=["over", "middle"],
                    coverColor =cc['fg']['Y'] if s.inventory['pointer'] == cellIndex else cc['fg']['G1'] if s.inventory['cells'][cellIndex]['disabled'] else ''
                )
                lines.extend(cell.split("\n"))
        if len(lines)>3:
            lines = [
                f"{lines[0]}{lines[3]}",
                f"{lines[1]}{lines[4]}",
                f"{lines[2]}{lines[5]}"
                ]
        if lines: output.append(f"{lines[0]}\n{lines[1]}\n{lines[2]}\n")
        
    return "".join(output)

def curseNoise(stdscr) -> str:
    output = ""

    y, x = map(lambda i: i-3, stdscr.getmaxyx())

    for _ in range((s.lvl-int(s.Mlvl/2))*3):
        output += anchor(
            stdscr,
            f"{cc['fg']['F']}{choice(UIP.noisePool[choices(['pattern','character'],weights=[40,70],k=1)[0]])}{cc['end']}",
            y        =randrange(1,y+1),
            x        =randrange(1,x+1),
            returnStr=True
        )

    return output

def render(stdscr, grid:list):
    """
    메인 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨.
    """
    global noiseBuffer
    global elapsedTime

    y, x    = stdscr.getmaxyx()
    Display = []
    buffer  = ""
    GFD     = [' '.join([d['block']for d in row])for row in grid]

    # Stage
    buffer = '\n'.join(GFD)
    dcmy   = int(y/2)-int(len([len(escapeAnsi(l)) for l in buffer.split("\n")])/2)-(s.y-int(len(s.Dungeon[s.Dy][s.Dx]['room'])/2))
    dcmx   = int(x/2)-(int(max([len(escapeAnsi(l)) for l in GFD])/2)+1)-(s.x-int(len(s.Dungeon[s.Dy][s.Dx]['room'][0])/2))
    Display.append(anchor(
        stdscr,
        buffer,
        y        =(2 if dcmy<2 else y   if dcmy+len(s.Dungeon[s.Dy][s.Dx]['room'])>y else dcmy) if s.dynamicCameraMoving else int(y/2)-int(len([len(escapeAnsi(l))  for l in buffer.split("\n")])/2),
        x        =(0 if dcmx<0 else x-2 if dcmx>=x-1                                 else dcmx) if s.dynamicCameraMoving else int(x/2)-(int(max([len(escapeAnsi(l)) for l in GFD])/2)+1),
        returnStr=True
    ))

    # Map
    if s.showDungeonMap:
        buffer = Textbox.TextBox(
            dgm.centerGridMapReturn(
                s.Dungeon,
                blank =1
            ),
            Type         ='middle',
            AMLS         =True,
            LineType     ='double',
            sideText     ="미궁 지도",
            sideTextPos  =["under", "middle"],
            coverSideText=True
        )
        Display.append(anchor(stdscr, buffer, y=2, x=x-actualLen(buffer.split("\n")[-1]), returnStr=True))

    # Status
    statusText = ""
    if not s.statusDesign:
        statusText += Textbox.TextBox(
f"""체력 : {cc['fg']['R']}{s.hp}/{s.Mhp}{cc['end']} | 방어력 : {cc['fg']['B1']}{s.df}/{s.Mdf}{cc['end']}
허기 : {cc['fg']['Y']}{s.hunger if s.hunger<=200 else f'{round(s.hunger/20)}%'}{cc['end']} | 공격력 : {cc['fg']['L']}{s.atk}{cc['end']}

풍력 : {cc['fg']['A']}{s.fairWind}/{s.MFairWind}{cc['end']}

TextBox.Line_\nTextBox.Left_잿조각  {cc['fg']['G1']}{s.ashChip}{cc['end']}
TextBox.Line_\n저주 : {cc['fg']['F']}{s.lvl}{cc['end']}, {cc['fg']['F']}{int((s.xp/s.Mxp)*100)}%{cc['end']}""",
        Type         ="middle",
        AMLS         =True,
        LineType     ='double',
        sideText     ="상태",
        sideTextPos  =["under", "left"],
        coverSideText=True
    )
    elif s.statusDesign == 1:
        statusText += Textbox.TextBox(
            ''.join([
                statusBar(s.hp, statusName="체  력", maxStatus=s.Mhp),
                statusBar(s.df, statusName="방어력", maxStatus=s.Mdf, color=cc['fg']['B1']),
                statusBar(s.atk, statusName="공격력", maxStatus=10, color=cc['fg']['L'], showEmptyCell=False),

                statusBar(math.ceil(s.hunger/200), statusName="허  기", maxStatus=10, color=cc['fg']['Y'],
                        backTag=f"{cc['fg']['Y']}{s.hunger if s.hunger<=200 else f'{round(s.hunger/20)}%'}{cc['end']}"),

                "\n"+statusBar(int((s.fairWind/s.MFairWind)*10), statusName="풍  력", maxStatus=10, color=cc['fg']['A'],
                        barType="FairWind", backTag=f"{cc['fg']['A']}{s.fairWind}{cc['end']}", showComma=False),
                        
                f"TextBox.Line_\n잿조각  {cc['fg']['G1']}{s.ashChip}{cc['end']}\n",
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
    statusText += f"\n\n{inventory()}"
    Display.append(anchor(stdscr, statusText, y=2, x=1, returnStr=True))

    # Log
    logHash = hash('0'.join(s.onDisplay)+f"{y}{x}")
    if logHash == logCache.key()[0]:
        logText = logCache[logHash]
    else:
        logText = Textbox.TextBox(
            "\n".join(s.onDisplay),
            maxLine        =x-3,
            LineType       ='double',
            alwaysReturnBox=False,
            sideText       ="로그",
            sideTextPos    =["over", "middle"],
            coverSideText  =True
        )
        logCache[logHash] = logText
    Display.append(anchor(stdscr, logText, y=y-(1 if not len(s.onDisplay)else len(s.onDisplay)), returnStr=True))

    # Info window(when use observe mode)
    if s.infoWindow['time']:
        maxLen        = max(map(lambda l: actualLen(escapeAnsi(l)), s.infoWindow['text'].split('\n')))
        sideTextSpace = 6 if maxLen>6 else 0; maxLen -= sideTextSpace
        timeGauge     = int((s.infoWindow['time']/s.infoWindow['setTime'])*maxLen)
        infoWindowText = Textbox.TextBox(
            s.infoWindow['text'],
            AMLS           =True,
            LineType       ='double',
            alwaysReturnBox=False,
            sideText       =f"{cc['fg']['Y']}{'━'*(timeGauge)}{cc['fg']['G1']}{'━'*(maxLen-timeGauge)}{cc['end']}",
            sideTextPos    =["under", "middle"],
            coverSideText  =True
        ).split('\n')
        Display.append(anchor(stdscr, '\n'.join(infoWindowText), y=2, x=int(x/2)-int(len(infoWindowText[0])/2), returnStr=True))

    # Debug Mode
    if s.debugConsole:
        by, bx, debugText = Textbox.TextBox(
            f"""Python version : {s.pythonVersion.major}.{s.pythonVersion.minor}.{s.pythonVersion.micro}
Window size : {stdscr.getmaxyx()}
Memory usage : {psutil.Process().memory_info().rss/2**20: .2f} MB
Number of threads : {psutil.Process().num_threads()}
Port : {s.port}

Dx : {s.Dx}, Dy : {s.Dy}, x : {s.x}, y : {s.y}
Number of entities : {s.entityCount}
Number of enemies : {s.enemyCount}
Number of total entities : {s.totalEntityCount}
soliloquy : ({s.soliloquyCount}, {s.soliloquyRange}, {p.soliloquy['min']}, {p.soliloquy['max']})

Elapsed time : {s.elapsedTime:.2f}""",
            Type         ="right",
            AMLS         =True,
            LineType     ="bold",
            returnSizeyx =True,
            sideText     ="디버그 콘솔",
            sideTextPos  =["over", "right"],
            coverSideText=True
        )
        Display.append(anchor(stdscr, debugText, y=int((y/2)-(by/2)), x=x-bx, returnStr=True)) # type:ignore

    # curse corrosion
    if s.lvl >= (s.Mlvl/2):
        if not l.pause:
            if not s.currentCurseNoiseFrequency:
                s.currentCurseNoiseFrequency = s.curseNoiseFrequency
                noiseBuffer                  = curseNoise(stdscr)
            s.currentCurseNoiseFrequency -= 1
        Display.append(noiseBuffer)

    # Pause
    if l.pause: Display.append(anchor(stdscr, UIP.pauseBox, returnStr=True))
    else:       s.elapsedTime = time.perf_counter()-s.startTime

    stdscr.erase()
    stdscr.addstr(''.join(Display))