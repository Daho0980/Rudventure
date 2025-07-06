import math
import time
import psutil
from   random import randrange, choices, choice

from Assets.data.color           import cColors as cc
from Game.entities.player        import statusEffect
from Game.utils.modules          import Textbox
from Game.utils.advanced         import DungeonMaker as dgm
from Game.utils.RSExt.libtext    import measure

from . import (
    escapeAnsi,
    anchor
)
from Assets.data import (
    totalGameStatus as s,
    percentage      as p,
    UIPreset        as UIP,
    flags           as f
)
from Game.utils.graphics.UI import (
    statusBar,
    inventory
)
from Game.utils.dataStructures.conveyor import (
    Conveyor
)


noiseBuffer = ""

logCache:Conveyor = Conveyor(1, True)

s.startTime = time.perf_counter()

def curseNoise(stdscr) -> str:
    output = ""

    y, x = map(lambda i: i-3, stdscr.getmaxyx())

    for _ in range((s.lvl-int(s.Mlvl/2))*3):
        output += anchor(
            stdscr,
            f"{cc['fg']['F']}{choice(
                s.noisePool[choices(
                    ['pattern', 'character'],
                    weights=[40,70],
                    k      =1)[0]]
                )
            }{cc['end']}",
            y        =randrange(1,y+1),
            x        =randrange(1,x+1),
            returnStr=True
        )

    return output

def percent(cr, mx) -> int:
    if mx == 0: return 0

    return ((cr*( (100<<16)//mx )) + (1<<15)) >> 16


# region Render
def render(stdscr):
    """
    메인 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨.
    """
    global noiseBuffer

    grid    = s.Dungeon[s.Dy][s.Dx]['room']
    y, x    = stdscr.getmaxyx()
    Display = []

    buffer = ""
    GFD    = [''.join([d['block']for d in row])for row in grid]

    # Stage
    buffer = '\n'.join(GFD)
    dcmy   = int(y/2)-int(s.roomData['maxHeight']   /2)-(s.y-int(s.roomData['maxHeight']/2))
    dcmx   = int(x/2)-int(s.roomData['maxCharWidth']/2)-(s.x-int(s.roomData['maxWidth'] /2))

    Display.append(anchor(
        stdscr, buffer,
        (
            2
                if dcmy<2
            else (y+2)-s.roomData['maxHeight'] 
                if dcmy+s.roomData['maxHeight']>(y+2)
            else dcmy
        ) if s.dynamicCameraMoving
        else int(y/2)-int(s.roomData['maxHeight']/2),

        (
            0
                if dcmx<0
            else x-s.roomData['maxCharWidth']
                if dcmx+s.roomData['maxCharWidth']>x
            else dcmx
        ) if s.dynamicCameraMoving
        else int(x/2)-int(s.roomData['maxCharWidth']/2),

        returnStr=True
    ))

    # Map
    if s.showDungeonMap:
        buffer = Textbox.TextBox(
            dgm.getMap(s.Dungeon, blank=1),

            Type         ='middle',
            AMLS         =True,
            LineType     ='double',
            sideText     ="지도",
            sideTextPos  =('under', 'middle'),
            coverSideText=True
        )
        Display.append(anchor(stdscr, buffer, y=2, x=x-measure(buffer.split("\n")[-1]), returnStr=True))

    # Status
    statusText = ""        
    if s.statusDesign:
        statusText += Textbox.TextBox(
            '\n'.join([
                statusBar.get(s.hp,  color=cc['fg']['R'] , statusName="체  력", maxStatus=s.Mhp                  ),
                statusBar.get(s.df,  color=cc['fg']['B1'], statusName="방어력", maxStatus=s.Mdf                  ),
                statusBar.get(s.atk, color=cc['fg']['L'] , statusName="공격력", maxStatus=10, showEmptyCell=False),
                statusBar.get(
                    math.ceil(s.hgr/200),

                    color     =cc['fg']['Y'],
                    statusName="허  기",
                    maxStatus =10,
                    backTag   =f"{cc['fg']['Y']}{s.hgr if s.hgr<=(s.Mhgr*0.01) else f'{percent(s.hgr, s.Mhgr)}%'}{cc['end']}"
                ),
                '\n'+statusBar.get(
                    s.exaltation,

                    color     =cc['fg']['A'],
                    statusName   ="고양감",
                    maxStatus    =s.MExaltation,
                    barType      ="Exaltation",
                    backTag      =f"{cc['fg']['A']}{s.exaltation}{cc['end']}",
                    showComma    =False,
                    usePercentage=True
                ),
                        
                f"TextBox.Line_\n잿조각  {cc['fg']['G1']}{s.ashChip}{cc['end']}",
                f"TextBox.Line_\nTextBox.Middle_{statusBar.get(
                    s.xp,

                    maxStatus    =s.Mxp,
                    color        =cc['fg']['F'],
                    barType      ="Cursed",
                    frontTag     =f"{cc['fg']['F']}{s.lvl}{cc['end']}",
                    backTag      =f"{cc['fg']['F']}{s.lvl+1}{cc['end']}",
                    showComma    =False,
                    usePercentage=True
                )}"
            ]),
            AMLS         =True,
            LineType     ='double',
            sideText     ="상태",
            sideTextPos  =('under', 'left'),
            coverSideText=True
        )

    else:
        statusText += Textbox.TextBox(
f"""체력 : {cc['fg']['R']}{s.hp}/{s.Mhp}{cc['end']} | 방어력 : {cc['fg']['B1']}{s.df}/{s.Mdf}{cc['end']}
허기 : {cc['fg']['Y']}{s.hgr if s.hgr<=(s.Mhgr*0.01) else f'{percent(s.hgr, s.Mhgr)}%'}{cc['end']} | 공격력 : {cc['fg']['L']}{s.atk}{cc['end']}

고양감 : {cc['fg']['A']}{s.exaltation}/{s.MExaltation}{cc['end']}

TextBox.Line_\nTextBox.Left_잿조각  {cc['fg']['G1']}{s.ashChip}{cc['end']}
TextBox.Line_\n저주 : {cc['fg']['F']}{s.lvl}{cc['end']}, {cc['fg']['F']}{int((s.xp/s.Mxp)*100)}%{cc['end']}""",
        Type         ="middle",
        AMLS         =True,
        LineType     ='double',
        sideText     ="상태",
        sideTextPos  =('under', 'left'),
        coverSideText=True
    )

    # Status effect
    statusText += f"\n\n{statusEffect.render()}"

    # Inventory
    statusText += f"\n\n{inventory.get()}"

    Display.append(anchor(stdscr, statusText, y=2, x=1, returnStr=True))

    # Log
    if (logHash:=hash('0'.join(s.onDisplay)+f"{y}{x}")) == logCache.key()[0]:
        logText = logCache[logHash]
    else:
        logText = Textbox.TextBox(
            "\n".join(s.onDisplay),
            maxLine      =x-3,
            LineType     ='double',
            safeBox      =False,
            sideText     ="로그",
            sideTextPos  =('over', 'middle'),
            coverSideText=True
        )
        logCache[logHash] = logText

    Display.append(anchor(stdscr, logText, y=y-(1 if not len(s.onDisplay)else len(s.onDisplay)), returnStr=True))

    # Info window (observe mode)
    if s.infoWindow['time']:
        maxLen         = max(map(lambda l: measure(escapeAnsi(l)), s.infoWindow['text'].split('\n')))
        sideTextSpace  = 6 if maxLen>6 else 0; maxLen -= sideTextSpace
        timeGauge      = int((s.infoWindow['time']/s.infoWindow['setTime'])*maxLen)
        infoWindowText = Textbox.TextBox(
            s.infoWindow['text'],

            AMLS         =True,
            LineType     ='double',
            safeBox      =False,
            sideText     =f"{cc['fg']['Y']}{'━'*(timeGauge)}{cc['fg']['G1']}{'━'*(maxLen-timeGauge)}{cc['end']}",
            sideTextPos  =('under', 'middle'),
            coverSideText=True,
            coverColor   =cc['end']
        ).split('\n')

        Display.append(anchor(stdscr, '\n'.join(infoWindowText), y=2, x=int(x/2)-int(len(infoWindowText[0])/2), returnStr=True))

    # Debug Mode
    if s.debug:
        by, bx, debugText = Textbox.TextBox(
            f"""Python version : {s.pythonVersion.major}.{s.pythonVersion.minor}.{s.pythonVersion.micro}
Window size : {stdscr.getmaxyx()}
Memory usage : {psutil.Process().memory_info().rss/2**20: .2f} MB
Number of threads : {psutil.Process().num_threads()}
Port : {s.port}

Dx : {s.Dx}, Dy : {s.Dy}
x : {s.x}, y : {s.y}
{'\n'.join(map(lambda d:f"{d[0]} : {d[1]}",s.roomData.items()))}

Number of entities : {s.entityCount}
Number of enemies : {s.enemyCount}
Number of total entities : {s.totalEntityCount}
monologue : ({s.monologueCount},{s.monologueRange},{p.monologue['min']},{p.monologue['max']})

Elapsed time : {s.elapsedTime:.2f}
FPS : {s.currentFrameCount}""",

            Type         ="right",
            AMLS         =True,
            LineType     ="bold",
            returnSizeyx =True,
            sideText     ="디버그 콘솔",
            sideTextPos  =('over', 'right'),
            coverSideText=True
        )

        Display.append(anchor(stdscr, debugText, y=int((y/2)-(by/2)), x=x-bx, returnStr=True)) # type:ignore

    # curse corrosion
    if s.lvl >= (s.Mlvl/2):
        if not f.pause:
            if not s.currentCurseNoiseFrequency:
                s.currentCurseNoiseFrequency = s.curseNoiseFrequency
                noiseBuffer                  = curseNoise(stdscr)

            s.currentCurseNoiseFrequency -= 1

        Display.append(noiseBuffer)

    # Pause
    if f.pause: Display.append(anchor(stdscr, UIP.pauseBox, returnStr=True))
    else      : s.elapsedTime = time.perf_counter()-s.startTime

    stdscr.erase()
    stdscr.addstr(''.join(Display))
    s.elapsedFrameCount += 1