import unicodedata, re
from   math           import ceil
from   itertools      import chain

from Assets.data.color import cColors as cc
from Game.utils.graphics import escapeAnsi, checkActualLen


def TextBox(
        Inp:str,
        Type:str             ="left",
        maxLine:int          =100,
        fillChar:str         =" ",
        inDistance:int       =0,
        outDistance:int      =0,
        addWidth:int         =0,
        AMLS:bool            =False,
        endLineBreak:bool    =False,
        returnSizeyx:bool    =False,
        LineType:str         ="normal",
        alwaysReturnBox:bool =True,
        sideText:str         ="",
        sideTextPos:list[str]=["over", "middle"],
        coverSideText:bool   =False,
        coverColor:str       =""
        ) -> str:
        """
        ``Inp``(str)                                                                : 텍스트박스 내용, 줄바꿈하려면 `\\n`을 사용해야 함\n
        ``Type``(str["left", "middle", "right"])                                    : 위치 설정, 기본적으로 `"left"`로 설정되어 있음\n
        ``maxLine``(int)                                                            : 최대 박스 길이 설정. AMLS를 True로 할거라면 그냥 신경쓰지 않는 게 좋음, 기본적으로 `100`으로 설정되어 있음\n
        ``fillChar``(char)                                                          : 박스 안을 채울 텍스트. 딱 한 개만 허용, 기본적으로 `" "`로 설정되어 있음\n
        ``inDistance``(int>=0)                                                      : 박스 안쪽 텍스트의 위, 아래 공백 크기 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``outDistance``(int>=0)                                                     : 박스 바깥의 공백 크기 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``addWidth``(int>=0)                                                        : 텍스트 양 옆 거리 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``AMLS``(bool)                                                              : 가장 긴 텍스트의 길이에 맞게 설정할지에 대한 여부. 이미 maxLine을 설정했다면 신경쓰지 않는 게 좋음, 기본적으로 `False`로 설정되어 있음\n
        ``endLineBreak``(bool)                                                      : 개행 문자 여부, 기본적으로 `False`로 설정되어 있음\n
        ``returnSizeyx``(bool)                                                      : 박스와 함께 오른쪽 아래 위치 추가 반환 여부, 기본적올 `False`로 설정되어 있음\n
        ``LineType``(str["normal", "double", "bold"])                               : 텍스트박스 테두리 종류 설정, 기본적으로 `"normal"`로 설정되어 있음\n
        ``alwaysReturnBox``(bool)                                                   : 빈 문자열 입력 시 무조건적인 박스 반환 여부, 기본적으로 `True`로 설정되어 있음\n
        ``sideText``(str)                                                           : 텍스트박스의 선 사이에 들어갈 텍스트, 기본적으로 `""`로 설정되어 있음\n
        ``sideTextPos``(list[str("over", "under"), str("left", "middle", "right")]) : sideText가 들어갈 위치, 기본적으로 `["over", "middle"]`로 설정되어 있음\n
        ``coverSideText``(bool)                                                     : sideText 양 옆을 텍스트박스가 감쌀지에 대한 여부, 기본적으로 `False`로 설정되어 있음\n
        ``coverColor``(str)                                                         : 박스와 내부 텍스트를 채울 색. 텍스트에 색이 들어가 있다면 다시 채워지지 않음. 기본적으로 `" "`로 설정되어 있음\n
        """
        if not len(Inp) and alwaysReturnBox:       Inp = "..."
        elif not len(Inp) and not alwaysReturnBox: return ""


        Display:str                        = ""
        Line:dict[str,dict[int,list[str]]] = {
                    "normal" : {0:["┌", "┐"], 1:["└", "┘"], 2:["├", "┤"], 3:["─", "│"]},
                    "double" : {0:["╔", "╗"], 1:["╚", "╝"], 2:["╠", "╣"], 3:["═", "║"]},
                    "bold"   : {0:["┏", "┓"], 1:["┗", "┛"], 2:["┣", "┫"], 3:["━", "┃"]}
                    }
        Texts:list            = Inp.split("\n")
        FrontSpace, BackSpace = "", ""
        endLine:str           = "\n" if endLineBreak else ""
        fullAddWidth:int      = addWidth*2 if Type=='middle'else addWidth
        FixedLine:str         = ""

        if coverSideText: sideText = f"{Line[LineType][2][1]}{sideText}{Line[LineType][2][0]}"
        if AMLS:          maxLine  = max(map(lambda l: checkActualLen(escapeAnsi(l)), chain(Texts,[sideText])))

        if sideText and sideTextPos[0] == "over":
            style = {
                "left"   : f"{sideText}{coverColor}{Line[LineType][3][0]*((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))}",
                "middle" : f"{Line[LineType][3][0]*(ceil(int(((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))/2)))}{sideText}{coverColor}{Line[LineType][3][0]*(ceil(int(((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))/2)))}{Line[LineType][3][0]if(maxLine+fullAddWidth+checkActualLen(escapeAnsi(sideText)))%2 else ''}",
                "right"  : f"{Line[LineType][3][0]*((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))}{sideText}{coverColor}"
                }[sideTextPos[1]]
            FixedLine = f"{coverColor}{Line[LineType][0][0]}{style}{Line[LineType][0][1]}\n"
        else: FixedLine = f"{coverColor}{Line[LineType][0][0]}{Line[LineType][3][0]*(maxLine+fullAddWidth)}{Line[LineType][0][1]}\n"
        Display += "\n"*outDistance+FixedLine+(f"{Line[LineType][3][1]}{fillChar*(maxLine+fullAddWidth)}{Line[LineType][3][1]}\n")*inDistance
        for textLine in Texts:
            space = checkActualLen(escapeAnsi(textLine))

            if textLine.startswith("TextBox."):
                if textLine == "TextBox.Line_": Display += f"{Line[LineType][2][0]}{Line[LineType][3][0]*(maxLine+fullAddWidth)}{Line[LineType][2][1]}\n"
                elif textLine.startswith("TextBox.Middle_"):
                    space   -= 15
                    Display += f"{Line[LineType][3][1]}{fillChar*int((maxLine-space)/2)}{textLine.lstrip('TextBox.Middle_')}{fillChar*(int((maxLine-space)/2) if not (maxLine-space)%2 else int((maxLine-space)/2)+1)}{Line[LineType][3][1]}\n"
                elif textLine.startswith("TextBox.Left_"):
                    space   -= 13
                    Display += f"{Line[LineType][3][1]}{textLine.lstrip('TextBox.Left_')}{fillChar*((maxLine-space)+addWidth)}{Line[LineType][3][1]}\n"
                elif textLine.startswith("TextBox.Right_"):
                    space   -= 14
                    Display += f"{Line[LineType][3][1]}{fillChar*((maxLine-space)+addWidth)}{textLine.lstrip('TextBox.Right_')}{Line[LineType][3][1]}\n"
            else:
                match Type:
                    case "left": BackSpace = fillChar*((maxLine-space)+addWidth)
                    case "middle":
                        FrontSpace = fillChar*(int((maxLine-space)/2)+addWidth)
                        BackSpace  = fillChar*(int((maxLine-space)/2)+addWidth if not (maxLine-space)%2 else int((maxLine-space)/2)+1+addWidth)
                    case "right": FrontSpace = fillChar*((maxLine-space)+addWidth)
                
                Display += f"{Line[LineType][3][1]}{FrontSpace}{textLine}{BackSpace}{Line[LineType][3][1]}\n"

        if sideText and sideTextPos[0] == "under":
            style = {
                "left"   : f"{sideText}{coverColor}{Line[LineType][3][0]*((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))}",
                "middle" : f"{Line[LineType][3][0]*(ceil(int(((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))/2)))}{sideText}{coverColor}{Line[LineType][3][0]*(ceil(int(((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))/2)))}{Line[LineType][3][0]if(maxLine+fullAddWidth+checkActualLen(escapeAnsi(sideText)))%2 else ''}",
                "right"  : f"{Line[LineType][3][0]*((maxLine+fullAddWidth)-checkActualLen(escapeAnsi(sideText)))}{sideText}{coverColor}"
                }[sideTextPos[1]]
            FixedLine = f"{Line[LineType][1][0]}{style}{Line[LineType][1][1]}{endLine}{cc['end']}"
        else: FixedLine = f"{Line[LineType][1][0]}{Line[LineType][3][0]*(maxLine+fullAddWidth)}{Line[LineType][1][1]}{endLine}{cc['end']}"
        Display += (f"{Line[LineType][3][1]}{fillChar*(maxLine+fullAddWidth)}{Line[LineType][3][1]}\n")*inDistance+FixedLine+"\n"*outDistance

        if returnSizeyx: return len(Display.split("\n"))-((outDistance*2)+2), maxLine+2, Display # type: ignore
        else:            return Display


# How to use:
# print(
#     TextBox("기본 박스(100칸)"),
#     TextBox("왼쪽\n(Type=left)", Type="left"),
#     TextBox("중간\n(Type=middle)", Type="middle"),
#     TextBox("오른쪽\n(Type=right)", Type='right'),
#     TextBox("최대 길이 자동 설정\n아래에 짧은 줄이 있든\n\n존나 긴 줄이 있든 알아서 정해줌\n\n(현재: Type=middle, AMLS=True)", Type="middle", AMLS=True),
#     TextBox("글상자 안/밖 거리 설정도 가능\n\n(inDistance=5, outDistance=3, AMLS=True, Type=middle)", inDistance=5, outDistance=3, AMLS=True, Type="middle"),
#     TextBox("일반"),
#     TextBox("볼드 (LineType=bold)", LineType="bold"),
#     TextBox("더블 (LineType=double)", LineType='double'),
#     sep="\n\n"
# )