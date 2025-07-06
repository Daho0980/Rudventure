# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! row는 가로, column은 세로입니다 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import copy ; import curses
from   cusser import Cusser

from Game.utils.system.sound  import play
from Game.utils.graphics      import escapeAnsi, anchor
from Game.utils.RSExt.libtext import measure

from . import (
    macros as m
)
from Assets.data.color import (
    cColors as cc,

    customColor
)


def main(title     :str                                               ,
         menu      :list[str|tuple]|dict[str|tuple,str]               ,
         color     :int|list[int]                      =0             ,
         icon      :str                                ='>'           ,
         maxLine   :int|str                            ="max"         ,
         lineSpace :int                                =1             ,
         tag       :str                                =""            ,
         frontTag  :str                                =""            ,
         setPos    :list[int|bool]                     =[-1,-1]       ,
         getPos    :bool                               =False         ,
         background:list[str]                          =[""]          ,
         useClear  :bool                               =False         ,
         killSound :list[bool]                         =[False, False],
         escapeReturn:int|None                         =None           ):
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
                          useClear, killSound,
                          escapeReturn        )

def _convert(menu, maxLine): # 1차원 메뉴를 2차원으로 재배열
    menu = list(map(
        lambda m:(None,m)
                if isinstance(m, str)
            else (
                customColor(*m[0][1:],m[0][0]), # type: ignore
                m[1]
            )
                if isinstance(m[0],(tuple,list))
            else m,
        menu
    ))

    output        = []
    subListColumn = -1
    subListRow    = -1
    
    while 1:
        if subListColumn >= len(menu)-1: break
        else:
            output.append([])
            subListRow += 1

        for _ in range(maxLine):
            subListColumn += 1
            output[subListRow].append((None,'') if subListColumn>=len(menu)else menu[subListColumn])
            
    return output

_positionOutput = lambda menu, row, column:(0,column+1)if(row==(len(menu)-1))else(row+1,column)
def _display(stdscr,
             title, menu,
             menuValues,
             arrow, maxLine,
             lineSpace,
             currSltC, currSltR,
             tag, frontTag      ):

    menuLen  = list(map(lambda row: list(map(lambda m:measure(m[1]), row)), menu))
    Display  = []

    Display.append(f"{cc['fg']['G1']}{frontTag}{cc['end']}\n{title}\n\n")

    row, col = -1, 0

    for _ in range(maxLine):
        menuLine = []
        for _ in range(len(menu)):
            row, col = _positionOutput(menu, row, col)
            menuLine.append(f"{arrow[row][col]} {menu[row][col][1]}{' '*(max(menuLen[row])-menuLen[row][col])}{' '*lineSpace}")

        Display.append(f"{''.join(menuLine)}\n")

    _l = list(map(lambda l:len(escapeAnsi(l)), ''.join(Display).split("\n")))

    if menuValues: Display.append(f"{cc['fg']['G1']}\n{menuValues[(maxLine*currSltR)+currSltC]}{cc['end']}")
    Display.append(f"\n\n{cc['fg']['G1']}{tag}{cc['end']}\n\n")

    return (
        ''.join(Display),\
        *tuple(round(c/2) - round(t/2)
            for c, t in zip(
                stdscr.getmaxyx(),
                (len(_l), max(_l))
            )
        )
    )

def _system(stdscr,
            title, menu,
            color, icon,
            maxLine, lineSpace,
            tag, frontTag,
            setPos, getPos,
            background,
            useClear, killSound,
            escapeReturn        ):
    if not isinstance(stdscr, Cusser): stdscr=Cusser(stdscr)

    menuKeys, menuValues = [], []

    if maxLine == 'max'    : maxLine = len(menu)
    if maxLine  > len(menu): raise Exception('최대 세로 배열수는 menu 개수보다 많을 수 없습니다!')

    if isinstance(menu, dict):
        menuKeys  :list|dict = list(menu.keys())
        menuValues:list      = list(menu.values())

    else: menuKeys = menu

    arrowColorInit = customColor(*color[1:], color[0]) if isinstance(color, list)else color # type: ignore
    currArrowColor = arrowColorInit
    
    menuKeys = _convert(menuKeys, maxLine)

    if sum(setPos) >= 0:
        currSltC = setPos[0]
        currSltR    = setPos[1]

    else:
        growtRate = 0

        while 1:
            if not menuKeys[growtRate]:
                if growtRate == len(menuKeys) - 1:
                    growtRate = 0
                    break

                else: growtRate += 1

            else: break
            
        currSltC = growtRate
        currSltR    = 0

    arrow = [[' ']*maxLine for _ in range(len(menuKeys))]

    while 1:
        stdscr.clear()

        currArrowColor = menuKeys[currSltR][currSltC][0] or arrowColorInit

        arrow[currSltR][currSltC] = f'{currArrowColor}{icon}'

        # 색 전염 방지
        if currSltR < (len(menuKeys)-1):
            arrow[currSltR+1][currSltC] = f"{cc['end']} "

        if currSltR>0 and currSltC<(maxLine-1):
            arrow[0][currSltC+1]  = f"{cc['end']} "

        if (currSltC+1) < maxLine:
            arrow[currSltR][currSltC+1] = f"{cc['end']} "
        # /색 전염 방지

        display, y, x = _display(stdscr,
                                 title, menuKeys,
                                 menuValues, arrow,
                                 maxLine, lineSpace,
                                 currSltC, currSltR,
                                 tag, frontTag      )
        
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

        sound = ()

        SNum, SNum1                            = 1, 0
        arrow[currSltR][currSltC] = ' '

        match stdscr.getch():
            case curses.KEY_UP:
                sound = ("system", "selector", "move")

                while 1:
                    if currSltC==0 and currSltR==0:
                        SNum, SNum1 = 0, 0
                        sound       = ("system", "selector", "block")
                        break

                    if currSltC-SNum < 0 and currSltR > 0:
                        currSltC = maxLine - 1
                        SNum                      = 0
                        currSltR             -= 1

                    if not menuKeys[currSltR - SNum1][currSltC - SNum][1]:
                        if currSltC - (SNum+1)<0:
                            if currSltR - (SNum1+1)<0:
                                SNum, SNum1 = 0, 0
                                sound       = ("system", "selector", "block")

                                break

                            else:
                                SNum   = 0
                                SNum1 += 1

                        else: SNum += 1

                    else: break

                currSltR    -= SNum1
                currSltC -= SNum

            case curses.KEY_DOWN:
                sound = ("system", "selector", "move")

                while 1:
                    if  currSltC==(maxLine-1)\
                    and currSltR   ==(len(menuKeys)-1):
                        SNum, SNum1 = 0, 0
                        sound       = ("system", "selector", "block")
                        break

                    if (currSltC+SNum)>(maxLine-1):
                        currSltC = 0
                        SNum             = 0
                        currSltR   += 1

                    if not menuKeys[currSltR+SNum1][currSltC+SNum][1]:
                        if (currSltC+SNum+1)>(maxLine-1):
                            if (currSltR+SNum1+1)>(len(menuKeys)-1):
                                SNum, SNum1 = 0, 0
                                sound       = ("system", "selector", "block")

                                break

                            else:
                                SNum   = 0
                                SNum1 += 1

                        else: SNum += 1

                    else: break

                currSltR    += SNum1
                currSltC += SNum

            case curses.KEY_LEFT:
                sound = ("system", "selector", "move")
                SNum1 = 1

                while 1:
                    if currSltR == 0:
                        SNum1 = 0
                        sound = ("system", "selector", "block")

                        break

                    if not menuKeys[currSltR-SNum1][currSltC][1]:
                        if currSltR-SNum1 <= 0:
                            SNum1 = 0
                            sound = ("system", "selector", "block")

                            break

                        else: SNum1 += 1

                    else: break

                currSltR -= SNum1

            case curses.KEY_RIGHT:
                sound = ("system", "selector", "move")
                SNum1 = 1

                while 1:
                    if currSltR == len(menuKeys)-1:
                        SNum1 = 0
                        sound = ("system", "selector", "block")

                        break

                    if not menuKeys[currSltR+SNum1][currSltC][1]:
                        if currSltR+SNum1 >= len(menuKeys)-1:
                            SNum1 = 0
                            sound = ("system", "selector", "block")

                            break

                        else: SNum1 += 1

                    else: break

                currSltR += SNum1

            case 10:
                if not killSound[1]: play("system", "selector", "select")
            
                break

            case 47:
                if escapeReturn != None:
                    if not killSound[1]: play("system", "selector", "select")

                    if  getPos: return escapeReturn, ( currSltC, currSltR )
                    else      : return escapeReturn

        if not killSound[0]: play(*sound)

    if useClear: stdscr.clear(); stdscr.refresh()
    blankCount = 0
    for i in range(0, currSltR+1):
        blankCount += menuKeys[i][:currSltC+1].count((None,'')) if (i==currSltR) else menuKeys[i].count((None,''))
    
    # 최대 라인 * 현재 가로줄 위치 + 현재 세로줄 위치 + 1 - 공백 개수
    if  getPos: return (maxLine*currSltR)+currSltC+1-blankCount, ( currSltC, currSltR )
    else      : return (maxLine*currSltR)+currSltC+1-blankCount