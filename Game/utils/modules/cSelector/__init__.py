# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! row는 가로, column은 세로입니다 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import copy ; import curses
from   cusser import Cusser

from .                       import macros as m
from Game.utils.system.sound import play
from Game.utils.graphics     import escapeAnsi, anchor
from Game.utils.CExt.libtext import actualLen

from Assets.data.color import (
    cColors as cc,

    customColor
    )


def main(title     :str,
         menu      :list[str|tuple]|dict[str|tuple,str]={'Why did you do...' : 'WHY...'},
         color     :int|list[int]                      =0                               ,
         icon      :str                                ='>'                             ,
         maxLine   :int|str                            ="max"                           ,
         lineSpace :int                                =1                               ,
         tag       :str                                =""                              ,
         frontTag  :str                                =""                              ,
         setPos    :list[int|bool]                     =[-1,-1]                         ,
         getPos    :bool                               = False                          ,
         background:list[str]                          = [""]                           ,
         useClear  :bool                               = False                          ,
         killSound :list[bool]                         = [False, False]                  ):
    """
    `title`(str, list)                     : 메뉴바의 타이틀이 될 문자열, 리스트 형태로 기입 시 타이틀과 메뉴의 공백이 제거됨. 무조건 기입해야 함\n
    `stdscr`(func)                         : 해당 모듈 외부에 있는 stdscr 사용 시 기입하는 매개변수, 기본적으로 빈 문자열로 지정되어 있음\n
    `menu`(list(1d))                   : 메뉴바의 메뉴가 될 리스트, 아무것도 지정하지 않을 시
        ```
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
        ```
    cSelector.main(
        title=f'이것은 타이틀입니다!',
        menu={
            "Option 1" : "1을 반환합니다.",
            "Option 2" : "2를 반환합니다.",
            "Option 3" : "3을 반환합니다."
        },
        color=[1,0,255,10],
        icon='@)',
        maxLine=1,
        lineSpace=2,
        tag="이것은 태그입니다!",
        frontTag="이것은 윗 태그입니다!"
    )
        ```
    """

    return curses.wrapper(_system,
                          title, menu,
                          color, icon,
                          maxLine, lineSpace,
                          tag, frontTag,
                          setPos, getPos,
                          background,
                          useClear, killSound)

def _convert(menu, maxLine:int): # 1차원 메뉴를 2차원으로 재배열
    menu = list(map(lambda m:(None,m)if isinstance(m,str)else(customColor(*m[0][1:],m[0][0]),m[1])if isinstance(m[0],(tuple,list))else m,menu)) # type: ignore

    newmenu       = [] # 2차원 배열로 변환될 menu
    subListColumn = -1 # 가로
    subListRow    = -1 # 세로
    
    while 1:
        if subListColumn >= len(menu)-1: break
        else:
            newmenu.append([])
            subListRow += 1

        for _ in range(maxLine):
            subListColumn += 1
            newmenu[subListRow].append((None,'') if subListColumn>=len(menu)else menu[subListColumn])
            
    return newmenu

def _display(stdscr               ,
             title           :str ,
             menu            :list,
             menuValues      :list,
             arrow           :list,
             maxLine         :int ,
             lineSpace       :int ,
             currSelectColumn:int ,
             currSelectRow   :int ,
             tag             :str ,
             frontTag        :str  ):
    """
    `title`(str, list)                       : 메뉴바의 타이틀이 될 문자열, 리스트 형태로 기입 시 타이틀과 메뉴의 공백이 제거됨, 무조건 기입해야 함\n
    `menu`(list(1d))                         : 메뉴바의 메뉴가 될 리스트, 무조건 기입해야 함\n
    `arrow`(str)                             :  현재 타겟된 메뉴를 표시하는 문자열, 무조건 기입해야 함\n
    `Enter`(str)                             : 타이틀과 메뉴의 공백, 무조건 기입해야 함\n
    `maxLine`(int)                           : 메뉴가 1개 이상일 때 적용할 수 있는 column 방향의 최대 나열 갯수, 무조건 기입해야 함\n
    `lineSpace`(int)                         : column이 한 개 이상일 때 적용되는 공백의 길이, 무조건 기입해야 함\n
    `menuValues`(list)                       : 각 메뉴의 타입이
        `{menu:values}` <-- 이와 같이 나올 경우 각 key에 할당된 value값들만 모아둔 리스트, 무조건 기입해야 함\n
    `currSelectColumn`, `currSelectRow`(int) : 현재 타겟된 메뉴의 위치, 무조건 기입해야 함\n
    `tag`(str)                               : 상시로 메뉴 맨 아래에 생기는 문자열, 무조건 기입해야 함\n
    `frontTag`(str)                          : 상시로 메뉴 맨 위에 생기는 문자열, 무조건 기입해야 함
    """
    _positionOutput = lambda menu, row, column:(0,column+1)if(row==(len(menu)-1))else(row+1,column)

    menuLen  = list(map(lambda row: list(map(lambda m:actualLen(m[1]), row)), menu))
    Display  = ""
    Display += f"{cc['fg']['G1']}{frontTag}{cc['end']}\n{title}\n\n"

    row, column = -1, 0

    for _ in range(maxLine):
        menuLine = ""
        for _ in range(len(menu)):
            row, column   = _positionOutput(menu, row, column)
            menuLine += f"{arrow[row][column]} {menu[row][column][1]}{' '*(max(menuLen[row])-menuLen[row][column])}{' '*lineSpace}"

        Display += f"{menuLine}\n"

    y, x = map(lambda n: round(n/2), list(stdscr.getmaxyx()))
    y    = y-round(len(list(map(lambda l:len(escapeAnsi(l)), Display.split("\n"))))/2)
    x    = x-round(max(list(map(lambda l:len(escapeAnsi(l)), Display.split("\n"))))/2)
    if menuValues: Display+=f"{cc['fg']['G1']}\n{menuValues[(maxLine*currSelectRow)+currSelectColumn]}{cc['end']}"
    Display+=f"\n\n{cc['fg']['G1']}{tag}{cc['end']}\n\n"

    return Display, y, x

def _system(stdscr,
           title, menu,
           color, icon,
           maxLine, lineSpace,
           tag, frontTag,
           setPos, getPos,
           background,
           useClear, killSound):
    if not isinstance(stdscr, Cusser): stdscr=Cusser(stdscr)

    menuKeys, menuValues = [], []

    if maxLine == 'max'    : maxLine = len(menu)
    if maxLine  > len(menu): raise Exception('최대 세로 배열수는 menu 개수보다 많을 수 없습니다!')

    if isinstance(menu, dict):
        menuKeys  :(list|dict) = list(menu.keys())
        menuValues:list        = list(menu.values())

    else: menuKeys = menu

    arrowColorInit = customColor(*color[1:], color[0]) if isinstance(color, list)else color # type: ignore
    currArrowColor = arrowColorInit
    
    menuKeys = _convert(menuKeys, maxLine)

    if sum(setPos) >= 0:
        currSelectColumn = setPos[0]
        currSelectRow    = setPos[1]

    else:
        growtRate = 0

        while 1:
            if not menuKeys[growtRate]:
                if growtRate == len(menuKeys) - 1:
                    growtRate = 0
                    break

                else: growtRate += 1

            else: break
            
        currSelectColumn = growtRate
        currSelectRow    = 0

    arrow:list = [[' ']*maxLine for _ in range(len(menuKeys))]

    while 1:
        stdscr.clear()

        currArrowColor                        =menuKeys[currSelectRow][currSelectColumn][0]if menuKeys[currSelectRow][currSelectColumn][0]else arrowColorInit
        arrow[currSelectRow][currSelectColumn]=f'{currArrowColor if menuKeys[currSelectRow][currSelectColumn][0] else(currArrowColor:=arrowColorInit)}{icon}'

        if currSelectRow       <len(menuKeys)-1                                : arrow[currSelectRow+1][currSelectColumn] = f"{cc['end']} " # 이 라인 포함 인접한 세 라인 모두 색 전염 방지용
        if currSelectRow       >0              and currSelectColumn<(maxLine-1): arrow[0][currSelectColumn+1]             = f"{cc['end']} "
        if (currSelectColumn+1)<maxLine                                        : arrow[currSelectRow][currSelectColumn+1] = f"{cc['end']} "

        display, y, x = _display(stdscr                         ,
                                 title                          ,
                                 menuKeys, menuValues           ,
                                 arrow                          ,
                                 maxLine, lineSpace             ,
                                 currSelectColumn, currSelectRow,
                                 tag, frontTag                   )
        bgBuffer = copy.deepcopy(background)
        for count, textData in enumerate(bgBuffer):
            if   textData == '[version]': bgBuffer[count] = m.showversion(stdscr)
            elif textData.startswith('[fullSizeBox]'):
                if len(textData) > 13:
                    data = eval(textData[13:])
                    bgBuffer[count] = m.fullSizedBox(stdscr, lineType=data['lineType'], boxColor=data['boxColor'])

                else: bgBuffer[count] = m.fullSizedBox(stdscr)

        stdscr.addstr (''.join(bgBuffer))
        anchor        (stdscr, display, y=y, x=x)
        stdscr.refresh()

        sound                                  = ("")
        SNum, SNum1                            = 1, 0 # column&&row conversion degree
        arrow[currSelectRow][currSelectColumn] = ' '
        key                                    = stdscr.getch()

        if key == curses.KEY_UP:
            sound = ("system", "selector", "move")

            while 1:
                if currSelectColumn==0 and currSelectRow==0:
                    SNum, SNum1 = 0, 0
                    sound       = ("system", "selector", "block")
                    break

                if currSelectColumn-SNum < 0 and currSelectRow > 0:
                    currSelectColumn = maxLine - 1
                    SNum                      = 0
                    currSelectRow             -= 1

                if not menuKeys[currSelectRow - SNum1][currSelectColumn - SNum][1]:
                    if currSelectColumn - (SNum+1)<0:
                        if currSelectRow - (SNum1+1)<0:
                            SNum, SNum1 = 0, 0
                            sound       = ("system", "selector", "block")

                            break

                        else:
                            SNum   = 0
                            SNum1 += 1

                    else: SNum += 1

                else: break

            currSelectRow    -= SNum1
            currSelectColumn -= SNum

        elif key == curses.KEY_DOWN:
            sound = ("system", "selector", "move")

            while 1:
                if currSelectColumn==(maxLine-1) and currSelectRow==(len(menuKeys)-1):
                    SNum, SNum1 = 0, 0
                    sound       = ("system", "selector", "block")
                    break

                if (currSelectColumn+SNum)>(maxLine-1):
                    currSelectColumn = 0
                    SNum            = 0
                    currSelectRow   += 1

                if not menuKeys[currSelectRow+SNum1][currSelectColumn+SNum][1]:
                    if (currSelectColumn+SNum+1)>(maxLine-1):
                        if (currSelectRow+SNum1+1)>(len(menuKeys)-1):
                            SNum, SNum1 = 0, 0
                            sound       = ("system", "selector", "block")

                            break

                        else:
                            SNum   = 0
                            SNum1 += 1

                    else: SNum += 1

                else: break

            currSelectRow    += SNum1
            currSelectColumn += SNum

        elif key == curses.KEY_LEFT:
            sound = ("system", "selector", "move")
            SNum1 = 1

            while 1:
                if currSelectRow == 0:
                    SNum1 = 0
                    sound = ("system", "selector", "block")

                    break

                if not menuKeys[currSelectRow-SNum1][currSelectColumn][1]:
                    if currSelectRow-SNum1 <= 0:
                        SNum1 = 0
                        sound = ("system", "selector", "block")

                        break

                    else: SNum1 += 1

                else: break

            currSelectRow -= SNum1

        elif key == curses.KEY_RIGHT:
            sound = ("system", "selector", "move")
            SNum1 = 1

            while 1:
                if currSelectRow == len(menuKeys)-1:
                    SNum1 = 0
                    sound = ("system", "selector", "block")

                    break

                if not menuKeys[currSelectRow+SNum1][currSelectColumn][1]:
                    if currSelectRow+SNum1 >= len(menuKeys)-1:
                        SNum1 = 0
                        sound = ("system", "selector", "block")

                        break

                    else: SNum1 += 1

                else: break

            currSelectRow += SNum1

        elif key == 10:
            if not killSound[1]: play("system", "selector", "select")
            
            break

        if not killSound[0]: play(*sound)

    if useClear: stdscr.clear(); stdscr.refresh()
    blankD = 0
    for i in range(0, currSelectRow+1):
        blankD += menuKeys[i][:currSelectColumn+1].count((None,'')) if (i==currSelectRow) else menuKeys[i].count((None,''))
    
    # 최대 라인 * 현재 가로줄 위치 + 현재 세로줄 위치 + 1 - 공백 개수
    if  getPos: return (maxLine*currSelectRow)+currSelectColumn+1-blankD, [ currSelectColumn, currSelectRow ]
    else      : return (maxLine*currSelectRow)+currSelectColumn+1-blankD