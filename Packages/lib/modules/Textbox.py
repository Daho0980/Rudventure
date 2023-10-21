import unicodedata, re

def escapeAnsi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def checkActualLen(line):
    Len = 0
    for i in line:
        if unicodedata.east_asian_width(i) in ['F', 'W']: Len += 2
        else                                            : Len += 1
    return Len

def TextBox(Inp, Type="left", maxLine=100, fillChar=" ", inDistance=0, outDistance=0, AMLS=False, endLineBreak=False, LineType="normal"):
        """
        ``Inp``(str)                                      : 텍스트박스 내용, 줄바꿈하려면 `\\n`을 사용해야 함\n
        ``Type``(str["left", "middle", "right"])          : 위치 설정, 기본적으로 `"left"`로 설정되어 있음\n
        ``maxLine``(int)                                  : 최대 박스 길이 설정. AMLS를 True로 할거라면 그냥 신경쓰지 않는 게 좋음, 기본적으로 `100`으로 설정되어 있음\n
        ``fillChar``(char)                                : 박스 안을 채울 텍스트. 딱 한 개만 허용, 기본적으로 `" "`로 설정되어 있음\n
        ``inDistance``(int>=0)                            : 박스 안쪽 텍스트의 위, 아래 공백 크기 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``outDistance``(int>=0)                           : 박스 바깥의 공백 크기 설정, 기본적으로 `0`으로 설정되어 있음\n
        ``AMLS``(bool)                                    : 가장 긴 텍스트의 길이에 맞게 설정할지에 대한 여부. 이미 maxLine을 설정했다면 신경쓰지 않는 게 좋음, 기본적으로 `False`로 설정되어 있음\n
        ``endLineBreak``(bool)                            : 개행 문자 여부, 기본적으로 `False`로 설정되어 있음\n
        ``LineType``(str["normal", "double", "bold"])     : 텍스트박스 테두리 종류 설정, 기본적으로 `"normal"`로 설정되어 있음\n
        """
        if not len(Inp): Inp = "..."
        Display  = ""

        Line       = {
                    "normal":{0:["┌", "┐"], 1:["└", "┘"], 2:["├", "┤"], 3:["─", "│"]},
                    "double":{0:["╔", "╗"], 1:["╚", "╝"], 2:["╠", "╣"], 3:["═", "║"]},
                    "bold"  :{0:["┏", "┓"], 1:["┗", "┛"], 2:["┣", "┫"], 3:["━", "┃"]}
                    }
        Texts      = Inp.split("\n")
        FrontSpace = ""
        BackSpace  = ""
        endLine    = "\n" if endLineBreak == True else ""
        if AMLS == True:
            maxLine = 0
            for i in Texts:
                if maxLine < checkActualLen(escapeAnsi(i)): maxLine = checkActualLen(escapeAnsi(i))

        Display += "\n"*outDistance
        Display += Line[LineType][0][0]+Line[LineType][3][0]*(maxLine)+Line[LineType][0][1]+"\n"
        Display += (Line[LineType][3][1]+fillChar*maxLine+Line[LineType][3][1]+"\n")*inDistance
        for i in range(len(Texts)):
            space = 0
            if Texts[i] == "TextBox.Line": Display += Line[LineType][2][0]+Line[LineType][3][0]*(maxLine)+Line[LineType][2][1]+"\n"
            else:
                for j in range(len(escapeAnsi(Texts[i]))):
                    if unicodedata.east_asian_width(escapeAnsi(Texts[i])[j]) in ['F', 'W']: space += 2
                    else                                                                  : space += 1
                if Type == "left"    : BackSpace = fillChar*(maxLine-space)
                elif Type == "middle":
                    FrontSpace = fillChar*int((maxLine-space)/2)
                    BackSpace  = fillChar*(int((maxLine-space)/2) if (maxLine-space)%2 == 0 else int((maxLine-space)/2)+1)
                elif Type == "right" : FrontSpace = fillChar*(maxLine-space)
                Display += (Line[LineType][3][1]+FrontSpace)+Texts[i]+(BackSpace+Line[LineType][3][1])+"\n"
        Display += (Line[LineType][3][1]+fillChar*maxLine+Line[LineType][3][1]+"\n")*inDistance
        Display += Line[LineType][1][0]+Line[LineType][3][0]*(maxLine)+Line[LineType][1][1]+endLine
        Display += "\n"*outDistance
        return Display


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