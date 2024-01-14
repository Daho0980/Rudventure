import unicodedata, re


escapeAnsi     = lambda line: re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('', line)
checkActualLen = lambda line: sum(map(lambda char: 2 if unicodedata.east_asian_width(char) in ['F','W'] else 1, line))

def TextBox(
        Inp:str,
        Type:str         ="left",
        maxLine:int      =100,
        fillChar:str     =" ",
        inDistance:int   =0,
        outDistance:int  =0,
        addWidth:int     =0,
        AMLS:bool        =False,
        endLineBreak:bool=False,
        returnSizeyx:bool=False,
        LineType:str     ="normal"
        ) -> str:
        """
        ``Inp``(str)                                      : 텍스트박스 내용, 줄바꿈하려면 `\\n`을 사용해야 함\n
        ``Type``(str["left", "middle", "right"])          : 위치 설정, 기본적으로 `"left"`로 설정되어 있음\n
        ``maxLine``(int)                                  : 최대 박스 길이 설정. AMLS를 True로 할거라면 그냥 신경쓰지 않는 게 좋음, 기본적으로 `100`으로 설정되어 있음\n
        ``fillChar``(char)                                : 박스 안을 채울 텍스트. 딱 한 개만 허용, 기본적으로 `" "`로 설정되어 있음\n
        ``inDistance``(int>=0)                            : 박스 안쪽 텍스트의 위, 아래 공백 크기 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``outDistance``(int>=0)                           : 박스 바깥의 공백 크기 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``addWidth``(int>=0)                              : 텍스트 양 옆 거리 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``AMLS``(bool)                                    : 가장 긴 텍스트의 길이에 맞게 설정할지에 대한 여부. 이미 maxLine을 설정했다면 신경쓰지 않는 게 좋음, 기본적으로 `False`로 설정되어 있음\n
        ``endLineBreak``(bool)                            : 개행 문자 여부, 기본적으로 `False`로 설정되어 있음\n
        ``LineType``(str["normal", "double", "bold"])     : 텍스트박스 테두리 종류 설정, 기본적으로 `"normal"`로 설정되어 있음\n
        """
        if not len(Inp): Inp = "..."
        Display  = ""

        Line       = {
                    "normal" : {0:["┌", "┐"], 1:["└", "┘"], 2:["├", "┤"], 3:["─", "│"]},
                    "double" : {0:["╔", "╗"], 1:["╚", "╝"], 2:["╠", "╣"], 3:["═", "║"]},
                    "bold"   : {0:["┏", "┓"], 1:["┗", "┛"], 2:["┣", "┫"], 3:["━", "┃"]}
                    }
        Texts                 = Inp.split("\n")
        FrontSpace, BackSpace = "", ""
        endLine               = "\n" if endLineBreak else ""
        fullAddWidth          = addWidth*2 if Type=='middle'else addWidth

        if AMLS: maxLine = max(map(lambda l: checkActualLen(escapeAnsi(l)), Texts))

        Display += "\n"*outDistance+f"{Line[LineType][0][0]}{Line[LineType][3][0]*(maxLine+fullAddWidth)}{Line[LineType][0][1]}\n"+(f"{Line[LineType][3][1]}{fillChar*maxLine}{Line[LineType][3][1]}\n")*inDistance
        for textLine in Texts:
            space = checkActualLen(escapeAnsi(textLine))

            if   textLine == "TextBox.Line": Display += f"{Line[LineType][2][0]}{Line[LineType][3][0]*(maxLine+fullAddWidth)}{Line[LineType][2][1]}\n"
            elif textLine.startswith("TextBox.Middle_"):
                space   -= len("TextBox.Middle_")
                Display += f"{Line[LineType][3][1]}{fillChar*int((maxLine-space)/2)}{textLine.lstrip('TextBox.Middle_')}{fillChar*(int((maxLine-space)/2) if not (maxLine-space)%2 else int((maxLine-space)/2)+1)}{Line[LineType][3][1]}\n"
            else:
                match Type:
                    case "left": BackSpace = fillChar*((maxLine-space)+addWidth)
                    case "middle":
                        FrontSpace = fillChar*(int((maxLine-space)/2)+addWidth)
                        BackSpace  = fillChar*(int((maxLine-space)/2)+addWidth if not (maxLine-space)%2 else int((maxLine-space)/2)+1+addWidth)
                    case "right": FrontSpace = fillChar*((maxLine-space)+addWidth)
                
                Display += f"{Line[LineType][3][1]}{FrontSpace}{textLine}{BackSpace}{Line[LineType][3][1]}\n"
        Display += (f"{Line[LineType][3][1]}{fillChar*maxLine}{Line[LineType][3][1]}\n")*inDistance+f"{Line[LineType][1][0]}{Line[LineType][3][0]*(maxLine+fullAddWidth)}{Line[LineType][1][1]}{endLine}"+"\n"*outDistance
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