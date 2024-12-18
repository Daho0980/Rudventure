# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! row는 가로, column은 세로입니다 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import copy ; import curses
from   cusser import Cusser

from .                       import macros as m
from Game.utils.system.sound import play

from Assets.data.color import (
    cColors as cc,

    customColor
    )
from Game.utils.graphics import (
    escapeAnsi,
    actualLen,
    anchor
    )


def main(title:str,
         subtitle:list[str]|dict[str,str]={'Why did you do...' : 'WHY...'},
         color:int|list[int]             =0,
         icon:str                        ='>',
         maxLine:int|str                 ="max",
         lineSpace:int                   =1,
         tag:str                         ="",
         frontTag:str                    ="",
         setPos:list[int|bool]           =[-1,-1],
         getPos:bool                     = False,
         background:list[str]            = [""],
         useClear:bool                   = False                           ):
    """
    `title`(str, list)                     : 메뉴바의 타이틀이 될 문자열, 리스트 형태로 기입 시 타이틀과 메뉴의 공백이 제거됨. 무조건 기입해야 함\n
    `stdscr`(func)                         : 해당 모듈 외부에 있는 stdscr 사용 시 기입하는 매개변수, 기본적으로 빈 문자열로 지정되어 있음\n
    `subtitle`(list(1d))                   : 메뉴바의 메뉴가 될 리스트, 아무것도 지정하지 않을 시
        ```py
        {'Why did you do...' : 'WHY...'}
        ```
        와 같은 이스터에그가 생성됨\n
    `color`(int, list)                     : 선택된 메뉴의 하이라이트를 채울 색. 리스트 형식은 각각 RGB 순서의 int형으로 기입해야 함. 기본적으로 `0`으로 지정되어 있음\n
    `icon`(char)                            : 현재 타겟된 메뉴를 표시하는 문자열, 기본적으로 `'>'`로 지정되어 있음\n
    `maxLine`(int)                         : 메뉴가 1개 이상일 때 적용할 수 있는 column 방향의 최대 나열 갯수, 기본적으로 `'max'`로 지정되어 있음\n
    `lineSpace`(int)                       : 열이 한 개 이상일 때 적용되는 공백의 길이, 기본적으로 `1`로 지정되어 있음\n
    `tag`(str)                             : 상시로 메뉴 맨 아래에 생기는 문자열, 기본적으로 빈 문자열로 지정되어 있음\n
    `frontTag`(str)                        : 상시로 메뉴 맨 위에 생기는 문자열, 기본적으로 빈 문자열로 지정되어 있음\n\n
    예시 :
        ```py
    cSelector.main(
        title=f'이것은 타이틀입니다!',
        subtitle={
            "Option 1" : "1을 반환합니다.",
            "Option 2" : "2를 반환합니다.",
            "Option 3" : "3을 반환합니다."
        },
        color=[1,0,255,10],
        icon='@',
        maxLine=1,
        lineSpace=2,
        tag="이것은 태그입니다!",
        frontTag="이것은 윗 태그입니다!"
    )
        ```
    """

    return curses.wrapper(system,
                          title, subtitle,
                          color, icon,
                          maxLine, lineSpace,
                          tag, frontTag,
                          setPos, getPos,
                          background,
                          useClear           )

def Change2D(subtitle, maxLine:int): # 1차원 subtitle을 2차원으로 재배열
    """
    `subtitle`(list(1d)) : 리스트의 메뉴, 무조건 기입해야 함\n
    `maxLine`(int)       : 메뉴가 1개 이상일 때 적용할 수 있는 column 방향의 최대 나열 갯수, 무조건 기입해야 함
    """
    newSubtitle               = [] # 2차원 배열로 변환될 subtitle
    subListRow, subListColumn = -1, -1 # 가로, 세로
    
    while 1:
        if subListColumn >= len(subtitle)-1: break
        else:
            newSubtitle.append([]) # 새로운 세로 배열셋 추가
            subListRow += 1 # 가로 추가
        for _ in range(maxLine):
            subListColumn += 1 # 세로 추가
            newSubtitle[subListRow].append('' if subListColumn>=len(subtitle)else subtitle[subListColumn])
    return newSubtitle

def returnDisplay(stdscr,
                  title:str,
                  subtitle:list,
                  subtitleValues:list,
                  arrow:list,
                  maxLine:int,
                  lineSpace:int,
                  nowSelectColumn:int,
                  nowSelectRow:int,
                  tag:str,
                  frontTag:str        ):
    """
    `title`(str, list)                     : 메뉴바의 타이틀이 될 문자열, 리스트 형태로 기입 시 타이틀과 메뉴의 공백이 제거됨, 무조건 기입해야 함\n
    `subtitle`(list(1d))                   : 메뉴바의 메뉴가 될 리스트, 무조건 기입해야 함\n
    `arrow`(str)                           :  현재 타겟된 메뉴를 표시하는 문자열, 무조건 기입해야 함\n
    `Enter`(str)                           : 타이틀과 메뉴의 공백, 무조건 기입해야 함\n
    `maxLine`(int)                         : 메뉴가 1개 이상일 때 적용할 수 있는 column 방향의 최대 나열 갯수, 무조건 기입해야 함\n
    `lineSpace`(int)                       : column이 한 개 이상일 때 적용되는 공백의 길이, 무조건 기입해야 함\n
    `subtitleValues`(list)                 : 각 메뉴의 타입이
        `{subtitle:values}` <-- 이와 같이 나올 경우 각 key에 할당된 value값들만 모아둔 리스트, 무조건 기입해야 함\n
    `nowSelectColumn`, `nowSelectRow`(int) : 현재 타겟된 메뉴의 위치, 무조건 기입해야 함\n
    `tag`(str)                             : 상시로 메뉴 맨 아래에 생기는 문자열, 무조건 기입해야 함\n
    `frontTag`(str)                        : 상시로 메뉴 맨 위에 생기는 문자열, 무조건 기입해야 함
    """
    positionOutput = lambda subtitle, row, column:(0,column+1)if(row==(len(subtitle)-1))else(row+1,column)
        
    def lenConverter(subtitle:list) -> list:
        output = []
        for i, row in enumerate(subtitle):
            output.append([])
            for menu in row: output[i].append(actualLen(menu))
        return output

    subtitleLen = lenConverter(subtitle)

    Display  = ""
    Display += f"{cc['fg']['G1']}{frontTag}{cc['end']}\n{title}\n\n"

    row, column = -1, 0

    for _ in range(maxLine):
        subtitleLine = ""
        for _ in range(len(subtitle)):
            row, column   = positionOutput(subtitle, row, column)
            subtitleLine += f"{arrow[row][column]} {subtitle[row][column]}{' '*(max(subtitleLen[row])-subtitleLen[row][column])}{' '*lineSpace}"
        Display += f"{subtitleLine}\n"
    y, x = map(lambda n: round(n/2), list(stdscr.getmaxyx()))
    y    = y-round(len(list(map(lambda l:len(escapeAnsi(l)), Display.split("\n"))))/2)
    x    = x-round(max(list(map(lambda l:len(escapeAnsi(l)), Display.split("\n"))))/2)
    if subtitleValues: Display+=f"{cc['fg']['G1']}\n{subtitleValues[(maxLine*nowSelectRow)+nowSelectColumn]}{cc['end']}"
    Display+=f"\n\n{cc['fg']['G1']}{tag}{cc['end']}\n\n"
    return Display, y, x

def system(stdscr,
           title, subtitle,
           color, icon,
           maxLine, lineSpace,
           tag, frontTag,
           setPos, getPos,
           background,
           useClear           ):
    if not isinstance(stdscr, Cusser): stdscr=Cusser(stdscr)

    subtitleKeys, subtitleValues = [], []

    if maxLine == 'max':        maxLine = len(subtitle)
    if maxLine > len(subtitle): raise Exception('최대 세로 배열수는 subtitle 개수보다 많을 수 없습니다!')
    if isinstance(subtitle, dict):
        subtitleKeys:(list|dict) = list(subtitle.keys())
        subtitleValues:list      = list(subtitle.values())
    else: subtitleKeys = subtitle

    arrowColor = customColor(color[1], color[2], color[3], color[0]) if isinstance(color, list)else color
    
    subtitleKeys = Change2D(subtitleKeys, maxLine)
    if sum(setPos) >= 0:
        nowSelectColumn:int = setPos[0]
        nowSelectRow:int    = setPos[1]

    else:
        growtRate:int = 0
        while 1:
            if not subtitleKeys[growtRate]:
                if growtRate == len(subtitleKeys) - 1:
                    growtRate = 0
                    break

                else: growtRate += 1

            else: break
        nowSelectColumn:int = growtRate
        nowSelectRow:int    = 0

    arrow:list = [[' ']*maxLine for _ in range(len(subtitleKeys))]

    while 1:
        stdscr.clear()
        arrow[nowSelectRow][nowSelectColumn] = f'{arrowColor}{icon}'

        if nowSelectRow < len(subtitleKeys)-1              : arrow[nowSelectRow+1][nowSelectColumn] = f"{cc['end']} " # 이 라인 포함 인접한 세 라인 모두 색 전염 방지용
        if nowSelectRow > 0 and nowSelectColumn < maxLine-1: arrow[0][nowSelectColumn+1]            = f"{cc['end']} "
        if nowSelectColumn + 1 < maxLine                   : arrow[nowSelectRow][nowSelectColumn+1] = f"{cc['end']} "
        display, y, x = returnDisplay(stdscr,
                                     title,
                                     subtitleKeys, subtitleValues,
                                     arrow,
                                     maxLine, lineSpace,
                                     nowSelectColumn, nowSelectRow,
                                     tag, frontTag                 )
        backgroundBuffer = copy.deepcopy(background)
        for count, textData in enumerate(backgroundBuffer):
            if   textData == '[version]': backgroundBuffer[count] = m.showversion(stdscr)
            elif textData.startswith('[fullSizeBox]'):
                if len(textData) > 13:
                    data = eval(textData[13:])
                    backgroundBuffer[count] = m.fullSizedBox(stdscr, lineType=data['lineType'], boxColor=data['boxColor'])

                else: backgroundBuffer[count] = m.fullSizedBox(stdscr)
        stdscr.addstr(''.join(backgroundBuffer))
        anchor(stdscr, display, y=y, x=x)
        stdscr.refresh()

        sound                                = ("")
        SNum, SNum1                          = 1, 0 # column&&row conversion degree
        arrow[nowSelectRow][nowSelectColumn] = ' '
        key                                  = stdscr.getch()

        if key == curses.KEY_UP:
            sound = ("system", "selector", "move")
            while 1:
                if nowSelectColumn==0 and nowSelectRow==0:
                    SNum, SNum1 = 0, 0
                    sound       = ("system", "selector", "block")
                    break
                if nowSelectColumn-SNum < 0 and nowSelectRow > 0:
                    nowSelectColumn = maxLine - 1
                    SNum                      = 0
                    nowSelectRow             -= 1
                if not subtitleKeys[nowSelectRow - SNum1][nowSelectColumn - SNum]:
                    if nowSelectColumn - (SNum+1)<0:
                        if nowSelectRow - (SNum1+1)<0:
                            SNum, SNum1 = 0, 0
                            sound       = ("system", "selector", "block")
                            break
                        else:
                            SNum   = 0
                            SNum1 += 1
                    else: SNum += 1
                else: break
            nowSelectRow    -= SNum1
            nowSelectColumn -= SNum

        elif key == curses.KEY_DOWN:
            sound = ("system", "selector", "move")
            while 1:
                if nowSelectColumn==(maxLine-1) and nowSelectRow==(len(subtitleKeys)-1):
                    SNum, SNum1 = 0, 0
                    sound       = ("system", "selector", "block")
                    break
                if (nowSelectColumn+SNum)>(maxLine-1):
                    nowSelectColumn = 0
                    SNum            = 0
                    nowSelectRow   += 1
                if not subtitleKeys[nowSelectRow+SNum1][nowSelectColumn+SNum]:
                    if (nowSelectColumn+SNum+1)>(maxLine-1):
                        if (nowSelectRow+SNum1+1)>(len(subtitleKeys)-1):
                            SNum, SNum1 = 0, 0
                            sound       = ("system", "selector", "block")
                            break
                        else:
                            SNum   = 0
                            SNum1 += 1
                    else: SNum += 1
                else: break
            nowSelectRow    += SNum1
            nowSelectColumn += SNum

        elif key == curses.KEY_LEFT:
            sound = ("system", "selector", "move")
            SNum1 = 1
            while 1:
                if nowSelectRow == 0:
                    SNum1 = 0
                    sound = ("system", "selector", "block")
                    break
                if not subtitleKeys[nowSelectRow-SNum1][nowSelectColumn]:
                    if nowSelectRow-SNum1 <= 0:
                        SNum1 = 0
                        sound = ("system", "selector", "block")
                        break
                    else: SNum1 += 1
                else: break
            nowSelectRow -= SNum1

        elif key == curses.KEY_RIGHT:
            sound = ("system", "selector", "move")
            SNum1 = 1
            while 1:
                if nowSelectRow == len(subtitleKeys)-1:
                    SNum1 = 0
                    sound = ("system", "selector", "block")
                    break
                if not subtitleKeys[nowSelectRow+SNum1][nowSelectColumn]:
                    if nowSelectRow+SNum1 >= len(subtitleKeys)-1:
                        SNum1 = 0
                        sound = ("system", "selector", "block")
                        break
                    else: SNum1 += 1
                else: break
            nowSelectRow += SNum1

        elif key == 10:
            play("system", "selector", "select")
            break

        play(*sound)
    if useClear: stdscr.clear(); stdscr.refresh()
    blankD = 0
    for i in range(0, nowSelectRow+1):
        blankD += subtitleKeys[i][:nowSelectColumn+1].count('') if i==nowSelectRow else subtitleKeys[i].count('')
    
    # 최대 라인 * 현재 가로줄 위치 + 현재 세로줄 위치 + 1 - 공백 개수
    if getPos: return (maxLine*nowSelectRow)+nowSelectColumn+1-blankD, [nowSelectColumn, nowSelectRow]
    else:              return (maxLine*nowSelectRow)+nowSelectColumn+1-blankD
