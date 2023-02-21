import unicodedata
import re

def escapeAnsi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)
def checkActualLen(line):
    Len = 0
    for i in line:
        if unicodedata.east_asian_width(i) in ['F', 'W']: Len += 2
        else: Len += 1
    return Len

def TextBox(Inp, Type="left", maxLine=100, fillChar=" ", inDistance=0, outDistance=0, AMLS=False, endLineBreak=False, LineType="normal"):
        Display  = ""

        Line       = {
                     "normal":{
                              0:["┌", "┐"],
                              1:["└", "┘"],
                              2:["├", "┤"],
                              3:["─", "│"]
                              },
                     "double":{
                              0:["╔", "╗"],
                              1:["╚", "╝"],
                              2:["╠", "╣"],
                              3:["═", "║"]
                              },
                     "bold":{
                              0:["┏", "┓"],
                              1:["┗", "┛"],
                              2:["┣", "┫"],
                              3:["━", "┃"],
                     }
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

# print(TextBox("기본 박스(100칸)"))
# print(TextBox("왼쪽(기본)"))
# print(TextBox("중간", Type="middle"))
# print(TextBox("오른쪽", Type='right'))
# print(TextBox("최대 길이 자동 설정\n아래에 짧은 줄이 있든\n\n존나 긴 줄이 있든 알아서 정해줌\n\n(현재: Type=middle, AMLS=True)", Type="middle", AMLS=True))
# print(TextBox("글상자 안/밖 거리 설정도 가능", inDistance=5, outDistance=3, AMLS=True, Type="middle"))
# print(TextBox("일반"))
# print(TextBox("볼드", LineType="bold"))
# print(TextBox("더블", LineType='double'))